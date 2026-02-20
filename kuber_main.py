# # main.py

# import streamlit as st
# from kuber.document_loader import process_uploaded_files
# from kuber.embeddings import load_vector_db, create_vector_db
# from kuber.llm_service import get_llm
# from kuber.rag_pipeline import build_rag_chain

# st.set_page_config(page_title="Loan Assistant Chatbot", layout="centered")

# # Session State Init
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "vector_db" not in st.session_state:
#     st.session_state.vector_db = load_vector_db()

# st.title("🏦 Loan Support Chatbot")

# # Sidebar
# with st.sidebar:
#     st.header("Setup")
#     uploaded_files = st.file_uploader(
#     "Upload Loan Docs",
#     type=["txt", "pdf", "csv", "xlsx"],
#     accept_multiple_files=True
# )
#     #uploaded_files = st.file_uploader("Upload Loan Docs (.txt)", type="txt", accept_multiple_files=True)

#     if st.button("Process Documents") and uploaded_files:
#         chunks = process_uploaded_files(uploaded_files)

#         if not chunks:
#             st.error("No valid content found.")
#         else:
#             st.session_state.vector_db = create_vector_db(chunks)
#             st.success("Indexing complete!")

# # Display Messages
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # Chat Input
# if prompt := st.chat_input("How can I help you today?"):
#     if st.session_state.vector_db is None:
#         st.error("Please upload and process documents first!")
#     else:
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message("user"):
#             st.markdown(prompt)

#         llm = get_llm()
#         rag_chain = build_rag_chain(
#             st.session_state.vector_db,
#             llm,
#             st.session_state.messages
#         )

#         with st.chat_message("assistant"):
#             output = rag_chain.invoke(prompt)

#             response = output["answer"]
#             sources = list(set(doc.metadata["source"] for doc in output["sources"]))

#             st.markdown(response)

#             with st.expander("References"):
#                 st.write(", ".join(sources))

#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": response
#             })


# main.py

# import streamlit as st
# from kuber.document_loader import process_uploaded_files
# from kuber.embeddings import load_vector_db, create_vector_db
# from kuber.llm_service import get_llm
# from kuber.rag_pipeline import build_rag_chain
# from kuber.tts_service import speak

# # -------------------------------
# # 1️⃣ PAGE CONFIG
# # -------------------------------
# st.set_page_config(page_title="Loan Assistant - Kuber", layout="centered")

# # -------------------------------
# # 2️⃣ SESSION STATE INIT
# # -------------------------------
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "vector_db" not in st.session_state:
#     st.session_state.vector_db = load_vector_db()

# # -------------------------------
# # 3️⃣ TITLE
# # -------------------------------
# st.title("🏦 Kuber - Loan Support Assistant")

# # -------------------------------
# # 4️⃣ SIDEBAR - DOCUMENT UPLOAD
# # -------------------------------
# with st.sidebar:
#     st.header("📂 Upload Documents")

#     uploaded_files = st.file_uploader(
#         "Upload Loan Documents",
#         type=["txt", "pdf", "csv", "xlsx"],
#         accept_multiple_files=True
#     )

#     if st.button("Process Documents") and uploaded_files:
#         chunks = process_uploaded_files(uploaded_files)

#         if not chunks:
#             st.error("No valid content found.")
#         else:
#             st.session_state.vector_db = create_vector_db(chunks)
#             st.success("Documents processed successfully!")

# # -------------------------------
# # 5️⃣ DISPLAY CHAT HISTORY
# # -------------------------------
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # -------------------------------
# # 6️⃣ CHAT INPUT
# # -------------------------------
# if prompt := st.chat_input("How can I help you today?"):

#     # Save user message
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # ---------------------------------------
#     # 🎯 GREETING DETECTION
#     # ---------------------------------------
#     if any(greet in prompt.lower() for greet in ["hi", "hello", "hey"]):
#         response = "Hi, my name is Kuber. How can I assist you?"

#         with st.chat_message("assistant"):
#             st.markdown(response)

#         speak(response)  # 🔊 Voice Output

#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": response
#         })

#     # ---------------------------------------
#     # 🧠 RAG FLOW
#     # ---------------------------------------
#     else:
#         if st.session_state.vector_db is None:
#             response = "Please upload and process documents first."

#             with st.chat_message("assistant"):
#                 st.markdown(response)

#             speak(response)

#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": response
#             })

#         else:
#             llm = get_llm()

#             rag_chain = build_rag_chain(
#                 st.session_state.vector_db,
#                 llm,
#                 st.session_state.messages
#             )

#             with st.chat_message("assistant"):
#                 try:
#                     output = rag_chain.invoke(prompt)
#                     response = output["answer"]

#                     st.markdown(response)

#                     # 🔊 Speak the response
#                     speak(response)

#                     st.session_state.messages.append({
#                         "role": "assistant",
#                         "content": response
#                     })

#                 except Exception as e:
#                     error_msg = f"Error: {str(e)}"
#                     st.error(error_msg)
#                     speak("Sorry, I encountered an error.")

# import streamlit as st
# from kuber.document_loader import process_uploaded_files
# from kuber.embeddings import load_vector_db, create_vector_db
# from kuber.llm_service import get_llm
# from kuber.rag_pipeline import build_rag_chain
# from kuber.tts_service import speak

# # -------------------------------
# # 🎨 PAGE CONFIG
# # -------------------------------
# st.set_page_config(
#     page_title="Kuber - AI Loan Assistant",
#     layout="centered",
#     initial_sidebar_state="expanded"
# )

# # -------------------------------
# # 🎨 CUSTOM DARK THEME + ANIMATION
# # -------------------------------


# st.markdown("""
# <style>

# /* ------------------ */
# /* MAIN BACKGROUND */
# /* ------------------ */
# .stApp {
#     background-color: #f4f7fb;
# }

# /* ------------------ */
# /* GLOBAL TEXT */
# /* ------------------ */
# html, body, p, span, div, label {
#     color: #1f2937 !important;
#     font-weight: 500;
# }

# /* ------------------ */
# /* TITLE */
# /* ------------------ */
# .kuber-title {
#     font-size: 32px;
#     font-weight: 700;
#     text-align: center;
#     color: #0f172a;
#     margin-bottom: 15px;
#     animation: fadeInTitle 0.8s ease-in-out;
# }

# /* ------------------ */
# /* CHAT MESSAGE BOX */
# /* ------------------ */
# [data-testid="stChatMessage"] {
#     padding: 14px;
#     border-radius: 12px;
#     margin-bottom: 12px;
#     font-size: 16px;
#     line-height: 1.6;
#     animation: fadeSlideUp 0.4s ease-in-out;
#     transition: transform 0.2s ease;
# }

# /* Slight hover lift */
# [data-testid="stChatMessage"]:hover {
#     transform: translateY(-2px);
# }

# /* USER MESSAGE */
# [data-testid="stChatMessage"][aria-label="user message"] {
#     background: #e8f0fe;
#     border-left: 4px solid #2563eb;
# }

# /* ASSISTANT MESSAGE */
# [data-testid="stChatMessage"][aria-label="assistant message"] {
#     background: #ffffff;
#     border-left: 4px solid #10b981;
# }

# /* ------------------ */
# /* CHAT INPUT */
# /* ------------------ */
# div[data-testid="stChatInput"] textarea {
#     background-color: #ffffff !important;
#     color: #111827 !important;
#     border-radius: 10px;
#     border: 1px solid #d1d5db;
#     font-size: 15px;
#     transition: border 0.3s ease;
# }

# div[data-testid="stChatInput"] textarea:focus {
#     border: 1px solid #2563eb;
# }

# /* ------------------ */
# /* SIDEBAR */
# /* ------------------ */
# section[data-testid="stSidebar"] {
#     background-color: #ffffff !important;
#     border-right: 1px solid #e5e7eb;
# }

# /* ------------------ */
# /* BUTTON */
# /* ------------------ */
# .stButton button {
#     background-color: #2563eb;
#     color: white !important;
#     font-weight: 600;
#     border-radius: 8px;
#     border: none;
#     transition: all 0.3s ease;
# }

# .stButton button:hover {
#     background-color: #1e40af;
#     transform: scale(1.03);
# }

# /* ------------------ */
# /* ANIMATIONS */
# /* ------------------ */
# @keyframes fadeSlideUp {
#     from {
#         opacity: 0;
#         transform: translateY(10px);
#     }
#     to {
#         opacity: 1;
#         transform: translateY(0);
#     }
# }

# @keyframes fadeInTitle {
#     from { opacity: 0; }
#     to { opacity: 1; }
# }

# </style>
# """, unsafe_allow_html=True)
# # st.markdown("""
# # <style>
# # /* Dark Background Gradient */
# # .stApp {
# #     background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
# #     color: white;
# # }

# # /* Glass effect chat container */
# # [data-testid="stChatMessage"] {
# #     background: rgba(255,255,255,0.05);
# #     padding: 12px;
# #     border-radius: 12px;
# #     backdrop-filter: blur(10px);
# #     animation: fadeIn 0.5s ease-in-out;
# # }

# # /* Sidebar styling */
# # section[data-testid="stSidebar"] {
# #     background: linear-gradient(180deg, #141e30, #243b55);
# # }

# # /* Animated Header */
# # .kuber-title {
# #     font-size: 32px;
# #     font-weight: bold;
# #     text-align: center;
# #     color: #00e6e6;
# #     animation: glow 2s infinite alternate;
# # }

# # /* Glow animation */
# # @keyframes glow {
# #     from { text-shadow: 0 0 10px #00e6e6; }
# #     to { text-shadow: 0 0 25px #00ffff; }
# # }

# # /* Fade animation */
# # @keyframes fadeIn {
# #     from { opacity: 0; transform: translateY(10px); }
# #     to { opacity: 1; transform: translateY(0); }
# # }

# # /* Button styling */
# # .stButton button {
# #     background: linear-gradient(90deg, #00c6ff, #0072ff);
# #     color: white;
# #     border-radius: 10px;
# #     border: none;
# # }

# # /* Chat input styling */
# # div[data-testid="stChatInput"] textarea {
# #     background-color: rgba(255,255,255,0.1);
# #     color: white;
# #     border-radius: 10px;
# # }
# # </style>
# # """, unsafe_allow_html=True)

# # -------------------------------
# # 🏦 TITLE
# # -------------------------------
# st.markdown('<div class="kuber-title">🏦 Kuber(Knowledge-driven Underwriting AI Chat Bot for Loan Eligibility & Reasons) - AI Loan Assistant</div>', unsafe_allow_html=True)
# st.markdown("<hr>", unsafe_allow_html=True)

# # -------------------------------
# # SESSION STATE INIT
# # -------------------------------
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "vector_db" not in st.session_state:
#     st.session_state.vector_db = load_vector_db()

# # -------------------------------
# # 📂 SIDEBAR
# # -------------------------------
# with st.sidebar:
#     st.header("📂 Document Processing")

#     uploaded_files = st.file_uploader(
#         "Upload Loan Documents",
#         type=["txt", "pdf", "csv", "xlsx"],
#         accept_multiple_files=True
#     )

#     if st.button("Process Documents"):
#         if uploaded_files:
#             with st.spinner("Indexing documents..."):
#                 chunks = process_uploaded_files(uploaded_files)

#                 if not chunks:
#                     st.error("No valid content found.")
#                 else:
#                     st.session_state.vector_db = create_vector_db(chunks)
#                     st.success("Documents processed successfully!")
#         else:
#             st.warning("Please upload files first.")

# # -------------------------------
# # DISPLAY CHAT HISTORY
# # -------------------------------
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # -------------------------------
# # CHAT INPUT
# # -------------------------------
# if prompt := st.chat_input("Ask Kuber anything about your loan..."):

#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # -----------------------
#     # Greeting
#     # -----------------------
#     if any(greet in prompt.lower() for greet in ["hi", "hello", "hey"]):
#         response = (
#             "Hi My name is Kuber, how may i assist you ?"
#         )

#         with st.chat_message("assistant"):
#             st.markdown(response)

#         speak(response)

#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": response
#         })

#     # -----------------------
#     # RAG FLOW
#     # -----------------------
#     else:
#         if st.session_state.vector_db is None:
#             response = "Please upload and process documents first."

#             with st.chat_message("assistant"):
#                 st.markdown(response)

#             speak(response)

#             st.session_state.messages.append({
#                 "role": "assistant",
#                 "content": response
#             })

#         else:
#             llm = get_llm()
#             rag_chain = build_rag_chain(
#                 st.session_state.vector_db,
#                 llm,
#                 st.session_state.messages
#             )

#             with st.chat_message("assistant"):
#                 with st.spinner("Kuber is analyzing..."):
#                     try:
#                         output = rag_chain.invoke(prompt)
#                         response = output["answer"]

#                         st.markdown(response)
#                         speak(response)

#                         st.session_state.messages.append({
#                             "role": "assistant",
#                             "content": response
#                         })

#                     except Exception as e:
#                         error_msg = f"Error: {str(e)}"
#                         st.error(error_msg)
#                         speak("Sorry, I encountered an error.")



#####latest working ####

# import streamlit as st
# from kuber.document_loader import process_uploaded_files
# from kuber.embeddings import create_vector_db
# from kuber.decision_engine import evaluate_loan
# from kuber.tts_service import speak

# # -------------------------------
# # PAGE CONFIG
# # -------------------------------
# st.set_page_config(page_title="Kuber - Loan Assistant", layout="centered")

# # -------------------------------
# # SESSION STATE INIT
# # -------------------------------
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "vector_db" not in st.session_state:
#     st.session_state.vector_db = None

# if "stage" not in st.session_state:
#     st.session_state.stage = "start"

# if "customer_row" not in st.session_state:
#     st.session_state.customer_row = None

# # -------------------------------
# # TITLE
# # -------------------------------
# st.markdown("<h2 style='color:#003366'>🏦 Kuber - Loan Eligibility Assistant</h2>", unsafe_allow_html=True)

# # -------------------------------
# # SIDEBAR: Upload + Vectorize
# # -------------------------------
# with st.sidebar:
#     st.header("📂 Upload Documents (CSV, XLSX, TXT, PDF)")

#     uploaded_files = st.file_uploader(
#         "Select files",
#         type=["csv", "xlsx", "txt", "pdf"],
#         accept_multiple_files=True
#     )

#     if st.button("Process Files"):
#         if not uploaded_files:
#             st.warning("Please upload at least one file.")
#         else:
#             chunks, df = process_uploaded_files(uploaded_files)

#             if df is not None:
#                 df.columns = df.columns.str.strip()
#                 st.session_state.customer_df = df
#                 st.success("Customer data loaded successfully!")

#             if chunks:
#                 st.session_state.vector_db = create_vector_db(chunks)
#                 st.success("Vector database created successfully!")

# # -------------------------------
# # DISPLAY CHAT HISTORY
# # -------------------------------
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # -------------------------------
# # CHAT INPUT FLOW
# # -------------------------------
# if prompt := st.chat_input("Type here..."):

#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     lower_prompt = prompt.lower()

#     # -----------------------------------
#     # GREETING
#     # -----------------------------------
#     if any(word in lower_prompt for word in ["hi", "hello", "hey"]):
#         response = "Hi, my name is Kuber. How may I assist you today? Please provide your account number."
#         st.session_state.stage = "account"

#     # -----------------------------------
#     # ACCOUNT NUMBER STAGE (FAISS SEARCH)
#     # -----------------------------------
#     elif st.session_state.stage == "account":
#         if st.session_state.vector_db is None:
#             response = "Please upload and process documents first."
#         else:
#             try:
#                 account_number = str(prompt).strip()
#                 retriever = st.session_state.vector_db.as_retriever(search_kwargs={"k": 1})

#                 # 🔹 SAFEST retrieval method for FAISS
#                 try:
#                     docs = retriever.vectorstore.similarity_search(
#                         f"Account_Number: {account_number}", k=1
#                     )
#                 except AttributeError:
#                     docs = retriever.get_relevant_documents(f"Account_Number: {account_number}")

#                 if not docs:
#                     response = "Account number not found. Please try again."
#                     st.session_state.stage = "account"
#                 else:
#                     doc_text = docs[0].page_content

#                     # store customer_row as dict
#                     customer_row = {}
#                     for line in doc_text.split(","):
#                         if ":" in line:
#                             k, v = line.split(":", 1)
#                             customer_row[k.strip()] = v.strip()

#                     # convert numeric fields
#                     for col in ["Annual_Income", "Credit_Score", "Years_of_Employment"]:
#                         if col in customer_row:
#                             customer_row[col] = float(customer_row[col])

#                     st.session_state.customer_row = customer_row
#                     st.session_state.stage = "loan_details"

#                     response = (
#                         "Account verified successfully from FAISS.\n\n"
#                         "Please provide Loan Type, Loan Amount and Tenure.\n"
#                         "Example: Personal, 500000, 60"
#                     )
#             except Exception as e:
#                 response = f"Error processing account number: {e}"

#     # -----------------------------------
#     # LOAN DETAILS STAGE
#     # -----------------------------------
#     elif st.session_state.stage == "loan_details":
#         try:
#             parts = [p.strip() for p in prompt.split(",")]
#             if len(parts) != 3:
#                 raise ValueError("Invalid input format")
#             loan_type, amount, tenure = parts
#             requested_amount = float(amount)
#             requested_tenure = int(tenure)

#             # Apply decision engine
#             status, reason = evaluate_loan(
#                 st.session_state.customer_row,
#                 requested_amount,
#                 requested_tenure
#             )

#             response = f"Loan Status: {status}\nReason: {reason}"
#             st.session_state.stage = "start"  # reset for next query

#         except:
#             response = "Invalid format. Please enter like: Personal, 500000, 60"

#     else:
#         response = "Please say Hi to start the loan process."

#     # -----------------------------------
#     # ASSISTANT RESPONSE + SPEECH
#     # -----------------------------------
#     with st.chat_message("assistant"):
#         st.markdown(response)
#         speak(response)

#     st.session_state.messages.append({
#         "role": "assistant",
#         "content": response
#     })




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

                    # convert numeric fields safely
                    for col in ["Annual_Income", "Credit_Score", "Years_of_Employment"]:
                        if col in customer_row:
                            customer_row[col] = float(customer_row[col].replace(",", "").strip())

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