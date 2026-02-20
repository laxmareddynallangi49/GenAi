
import streamlit as st
from kuber.document_loader import process_uploaded_files
from kuber.embeddings import create_vector_db
from kuber.decision_engine import evaluate_loan
from kuber.tts_service import speak

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Kuber - Loan Assistant", layout="centered")

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "customer_row" not in st.session_state:
    st.session_state.customer_row = None

# -------------------------------
# TITLE
# -------------------------------
st.markdown("<h2 style='color:#003366'>🏦 Kuber - Loan Eligibility Assistant</h2>", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR: Upload + Vectorize
# -------------------------------
with st.sidebar:
    st.header("📂 Upload Documents (CSV, XLSX, TXT, PDF)")

    uploaded_files = st.file_uploader(
        "Select files",
        type=["csv", "xlsx", "txt", "pdf"],
        accept_multiple_files=True
    )

    if st.button("Process Files"):
        if not uploaded_files:
            st.warning("Please upload at least one file.")
        else:
            chunks, df = process_uploaded_files(uploaded_files)

            if df is not None:
                df.columns = df.columns.str.strip()
                st.session_state.customer_df = df
                st.success("Customer data loaded successfully!")

            if chunks:
                st.session_state.vector_db = create_vector_db(chunks)
                st.success("Vector database created successfully!")

# -------------------------------
# DISPLAY CHAT HISTORY
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# CHAT INPUT FLOW
# -------------------------------
if prompt := st.chat_input("Type here..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    lower_prompt = prompt.lower()

    # -----------------------------------
    # GREETING
    # -----------------------------------
    if any(word in lower_prompt for word in ["hi", "hello", "hey"]):
        response = "Hi, my name is Kuber. How may I assist you today? Please provide your account number."
        st.session_state.stage = "account"

    # -----------------------------------
    # ACCOUNT NUMBER STAGE
    # -----------------------------------
    elif st.session_state.stage == "account":
        if st.session_state.vector_db is None:
            response = "Please upload and process documents first."
        else:
            try:
                account_number = str(prompt).strip()
                retriever = st.session_state.vector_db.as_retriever(search_kwargs={"k": 1})

                # FAISS retrieval
                try:
                    docs = retriever.vectorstore.similarity_search(
                        f"Account_Number: {account_number}", k=1
                    )
                except AttributeError:
                    docs = retriever.get_relevant_documents(f"Account_Number: {account_number}")

                if not docs:
                    response = "Account number not found. Please try again."
                    st.session_state.stage = "account"
                else:
                    doc_text = docs[0].page_content

                    # store customer_row as dict
                    customer_row = {}
                    for line in doc_text.split(","):
                        if ":" in line:
                            k, v = line.split(":", 1)
                            customer_row[k.strip()] = v.strip()

                    for col in ["Annual_Income", "Credit_Score", "Years_of_Employment"]:
                        if col in customer_row:
                            customer_row[col] = float(customer_row[col])

                    st.session_state.customer_row = customer_row

                    # --------------------------
                    # Friendly verified message
                    # --------------------------
                    if not account_number.isdigit():
                        response = "Sorry, I can only help with loan-related queries. Please provide your account number."
                        st.session_state.stage = "account"
                    else:
                        response = (
                            f"Kuber has successfully verified your account number {account_number}.\n\n"
                            "Please provide Loan Type, Loan Amount, and Tenure.\n"
                            "Example: Personal, 500000, 60"
                        )
                        st.session_state.stage = "loan_details"

            except Exception as e:
                response = f"Error processing account number: {e}"

    # -----------------------------------
    # LOAN DETAILS STAGE
    # -----------------------------------
    elif st.session_state.stage == "loan_details":
        try:
            parts = [p.strip() for p in prompt.split(",")]
            if len(parts) != 3:
                raise ValueError
            loan_type, amount, tenure = parts

            # Ensure numeric values
            if not amount.replace(".", "", 1).isdigit() or not tenure.isdigit():
                raise ValueError

            requested_amount = float(amount)
            requested_tenure = int(tenure)

            # Apply decision engine
            status, reason = evaluate_loan(
                st.session_state.customer_row,
                requested_amount,
                requested_tenure
            )

            response = f"Loan Status: {status}\nReason: {reason}"
            st.session_state.stage = "start"

        except:
            response = "Sorry, I can only process loan details in the format: LoanType, Amount, Tenure. Example: Personal, 500000, 60"

    else:
        response = "Please say Hi to start the loan process."

    # -----------------------------------
    # ASSISTANT RESPONSE + SPEECH
    # -----------------------------------
    with st.chat_message("assistant"):
        st.markdown(response)
        speak(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })