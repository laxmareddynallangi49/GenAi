import os
import certifi
import tempfile
from dotenv import load_dotenv
import streamlit as st
import httpx
import pandas as pd

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader, PDFMinerLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

# -------------------------------
# 0. SESSION STATE GETTERS
# -------------------------------
def get_messages():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    return st.session_state["messages"]

def get_vector_db():
    if "vector_db" not in st.session_state:
        st.session_state["vector_db"] = None
    return st.session_state["vector_db"]

def get_customer_df():
    if "customer_df" not in st.session_state:
        st.session_state["customer_df"] = None
    return st.session_state["customer_df"]

# -------------------------------
# 1. STREAMLIT CONFIG
# -------------------------------
st.set_page_config(page_title="Knowledge-driven Underwriting AI chat bot for loan Eligibility & Reasons (KUBER)", layout="centered")

# -------------------------------
# 2. ENV + SSL
# -------------------------------
load_dotenv()
API_KEY = "sk-MUzlSmAC4By-e_bfkFWcHQ"
BASE_URL = "https://genailab.tcs.in"

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()
os.environ["TIKTOKEN_CACHE_DIR"] = "./token"

# -------------------------------
# 3. HTTP CLIENT
# -------------------------------
client = httpx.Client(verify=False)

# -------------------------------
# 4. LLM / EMBEDDINGS
# -------------------------------
llm = ChatOpenAI(
    base_url=BASE_URL,
    model="azure_ai/genailab-maas-DeepSeek-V3-0324",
    api_key=API_KEY,
    http_client=client,
    temperature=0
)

embedding_model = OpenAIEmbeddings(
    base_url=BASE_URL,
    model="azure/genailab-maas-text-embedding-3-large",
    api_key=API_KEY,
    http_client=client
)

# -------------------------------
# 5. CHROMA PERSISTENCE
# -------------------------------
PERSIST_DIR = "./chroma_db"
if os.path.exists(PERSIST_DIR):
    st.session_state["vector_db"] = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding_model
    )

# -------------------------------
# 6. SINGLE FILE UPLOAD
# -------------------------------
st.sidebar.header("Upload Customer / Loan Documents")
uploaded_file = st.sidebar.file_uploader("Upload .txt, .pdf, .csv, or .xlsx", type=["txt", "pdf", "csv", "xlsx"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    ext = uploaded_file.name.split('.')[-1].lower()
    try:
        if ext == "txt":
            df = pd.read_csv(tmp_path, sep=",")
        elif ext == "csv":
            df = pd.read_csv(tmp_path)
        elif ext == "xlsx":
            df = pd.read_excel(tmp_path)
        elif ext == "pdf":
            loader = PDFMinerLoader(tmp_path)
            docs = loader.load()
            df = pd.DataFrame([d.page_content.split(",") for d in docs[1:]], columns=docs[0].page_content.split(","))
        else:
            st.error("Unsupported file type")
            df = pd.DataFrame()
    finally:
        os.remove(tmp_path)

    if not df.empty:
        st.session_state["customer_df"] = df
        st.success(f"File loaded: {uploaded_file.name} with {len(df)} records")

# -------------------------------
# 7. PROMPT TEMPLATE FOR DOCUMENT QA
# -------------------------------
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are Kuber, a Loan Assistant. "
     "Answer questions **only using the uploaded documents (context)**. "
     "If the user asks something that is not in the documents, "
     "respond: 'I am sorry, I can only answer questions related to the uploaded documents.' "
     "For greetings like 'hi', 'hello', respond politely introducing yourself: "
     "'Hi, this is Kuber. How can I help you?'\n\n"
     "Context:\n{context}"
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# -------------------------------
# 8. ELIGIBILITY FUNCTION
# -------------------------------
def calculate_eligibility(row, loan_type):
    try: age = int(row.get("Age", 0))
    except: age = 0
    try: employment_years = int(row.get("Years_of_Employment", 0))
    except: employment_years = 0
    try: income = float(row.get("Annual_Income", 0))
    except: income = 0
    try: credit = int(row.get("Credit_Score", 0))
    except: credit = 0
    dependents = int(row.get("Dependents", 0))
    previous_loans = str(row.get("Previous_Loan_Status", "")).lower()

    status = "Approved"
    reason = ""
    loan_type_lower = loan_type.lower()

    if loan_type_lower != "study" and (age + 10) > 70:
        return "Reject", "Age + tenure exceeds retirement age"

    if loan_type_lower == "home":
        if credit < 700:
            return "Reject", "Credit score below 700"
        if income < 25000:
            return "Reject", "Income below ₹25,000"
        if employment_years < 2:
            return "Reject", "Employment less than 2 years"
    elif loan_type_lower == "personal":
        if credit < 650:
            return "Reject", "Credit score below 650"
        if income < 20000:
            return "Reject", "Income below ₹20,000"
        if employment_years < 1:
            return "Reject", "Employment less than 1 year"
        if previous_loans.count("active") > 3:
            return "Reject", "More than 3 active loans"
    elif loan_type_lower == "auto":
        if credit < 700:
            return "Reject", "Credit score below 700"
        if income < 15000:
            return "Reject", "Income below ₹15,000"
    elif loan_type_lower == "study":
        if credit < 650:
            return "Reject", "Credit score below 650"
        if income <= 0:
            return "Conditional Approval", "Require co-applicant/guarantor"
    else:
        return "Unknown", "Unknown loan type"

    if 650 <= credit < 700 and loan_type_lower in ["home", "personal"]:
        status = "Conditional Approval"
        reason = "High risk due to moderate credit score"

    return status, reason or "Meets KUBER policy requirements"

# -------------------------------
# 9. CHAT UI LOGIC
# -------------------------------
st.title("🏦 KUBER: Knowledge-driven Loan Eligibility Chatbot")

# Display previous messages
for message in get_messages():
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "references" in message:
            with st.expander("References"):
                st.write(message["references"])

# Chat input
if prompt_input := st.chat_input("Say hi to start..."):
    get_messages().append({"role": "user", "content": prompt_input})
    with st.chat_message("user"):
        st.markdown(prompt_input)

    user_input = prompt_input.strip().lower()
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]

    if user_input in greetings:
        response_text = "Hi, this is Kuber. Please provide your Account Number to check loan eligibility."
        with st.chat_message("assistant"):
            st.markdown(response_text)
        get_messages().append({"role": "assistant", "content": response_text})

    elif user_input.isdigit() and get_customer_df() is not None:
        account_number = int(user_input)
        df = get_customer_df()
        customer_row = df[df["Account_Number"].astype(str) == str(account_number)]
        if customer_row.empty:
            response_text = "Account number not found. Please check and try again."
        else:
            # Ask which loan type
            response_text = f"Account found. Which loan type would you like to check? (Home / Personal / Auto / Study)"
            st.session_state["current_account"] = account_number

        with st.chat_message("assistant"):
            st.markdown(response_text)
        get_messages().append({"role": "assistant", "content": response_text})

    elif "current_account" in st.session_state and user_input in ["home", "personal", "auto", "study"]:
        account_number = st.session_state["current_account"]
        df = get_customer_df()
        customer_row = df[df["Account_Number"].astype(str) == str(account_number)].iloc[0]
        status, reason = calculate_eligibility(customer_row, user_input)
        response_text = f"Loan Type: {user_input.title()}\nEligibility: {status}\nReason: {reason}"
        with st.chat_message("assistant"):
            st.markdown(response_text)
        get_messages().append({"role": "assistant", "content": response_text})
        del st.session_state["current_account"]

    else:
        response_text = "Please start by saying hi or provide a valid account number."
        with st.chat_message("assistant"):
            st.markdown(response_text)
        get_messages().append({"role": "assistant", "content": response_text})