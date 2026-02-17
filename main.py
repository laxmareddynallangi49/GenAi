# import streamlit as st
# from app.document_loader import load_pdf
# from app.rag_pipeline import RAGPipeline
# from app.speech_service import SpeechService
# from app.tts_service import TTSService
# from app.config import TTS_RATE, TTS_VOLUME

# st.set_page_config(page_title="Jarvis RAG Assistant")
# st.title("🤖 Jarvis RAG Assistant")

# # Load services once
# @st.cache_resource
# def load_speech():
#     return SpeechService()

# @st.cache_resource
# def load_tts():
#     return TTSService(rate=TTS_RATE, volume=TTS_VOLUME)

# speech_service = load_speech()
# tts_service = load_tts()

# uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

# if uploaded_file:

#     with open("temp.pdf", "wb") as f:
#         f.write(uploaded_file.read())

#     documents = load_pdf("temp.pdf")

#     @st.cache_resource
#     def initialize_rag(docs):
#         return RAGPipeline(docs)

#     rag = initialize_rag(documents)

#     st.divider()

#     typed_input = st.text_input("Type your question")

#     audio_input = st.audio_input("Or say: 'Jarvis ...'")

#     user_query = None

#     # Manual input
#     if typed_input:
#         user_query = typed_input

#     # Voice input
#     if audio_input:
#         spoken_text = speech_service.transcribe(audio_input)
#         st.write("🎤 You said:", spoken_text)

#         activated, cleaned_query = speech_service.check_wake_word(spoken_text)

#         if activated:
#             st.success("🟢 Wake word detected")
#             user_query = cleaned_query
#         else:
#             st.warning("Wake word not detected. Say 'Jarvis ...'")

#     if user_query:
#         answer, context = rag.query(user_query)

#         st.subheader("🤖 Answer")
#         st.write(answer)

#         with st.expander("🔍 Retrieved Context"):
#             st.write(context)

#         # Speak response
#         if st.toggle("🔊 Enable Voice Response", value=True):
#             tts_service.speak(answer)


#### above is the working #########


# import streamlit as st

# st.set_page_config(page_title="Jarvis RAG Assistant", layout="wide")

# st.title("🤖 Jarvis RAG Assistant")
# st.caption("Upload document → Ask question → Get answer")

# st.divider()

# # 🔑 API Key Input (Visible in UI)
# api_key = st.text_input(
#     "Enter OpenAI API Key",
#     type="password",
#     placeholder="sk-...",
# )

# st.divider()

# # 📄 File Upload
# uploaded_file = st.file_uploader("Upload PDF Document", type=["pdf"])

# # 💬 Question Input
# question = st.text_input("Ask a question about the document")

# st.divider()

# # 🔊 Voice Toggle (UI Only)
# enable_voice = st.toggle("Enable Voice Response", value=False)

# st.divider()

# # 🚀 Submit Button
# if st.button("Generate Answer"):

#     if not api_key:
#         st.warning("Please enter your OpenAI API Key.")
    
#     elif not uploaded_file:
#         st.warning("Please upload a PDF file.")

#     elif not question:
#         st.warning("Please enter a question.")

#     else:
#         # Placeholder response (so no backend error)
#         st.success("System Ready ✅ (Backend not connected yet)")
        
#         st.subheader("🤖 Answer")
#         st.write("This is a placeholder answer. Connect your backend logic here.")

#         with st.expander("🔍 Retrieved Context"):
#             st.write("Document chunks will appear here after RAG integration.")

#         if enable_voice:
#             st.info("Voice output will trigger here.")




import streamlit as st
import tempfile
from openai import OpenAI

from app.document_loader import load_pdf
from app.rag_pipeline import RAGPipeline
from app.speech_service import SpeechService
from app.tts_service import TTSService
from app.config import TTS_RATE, TTS_VOLUME


# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="Jarvis RAG Assistant", layout="wide")
st.title("🤖 Jarvis RAG Assistant")

st.divider()

# -------------------------------------------------
# API KEY INPUT (UI based)
# -------------------------------------------------
api_key = st.text_input("Enter OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

st.divider()

# -------------------------------------------------
# Load Services Once
# -------------------------------------------------
@st.cache_resource
def load_speech():
    return SpeechService()

@st.cache_resource
def load_tts():
    return TTSService(rate=TTS_RATE, volume=TTS_VOLUME)

speech_service = load_speech()
tts_service = load_tts()

# -------------------------------------------------
# Upload PDF
# -------------------------------------------------
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file and api_key:

    # Save PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    documents = load_pdf(pdf_path)

    @st.cache_resource
    def initialize_rag(docs):
        return RAGPipeline(docs)

    rag = initialize_rag(documents)

    st.divider()

    # -------------------------------------------------
    # Input Section
    # -------------------------------------------------
    typed_input = st.text_input("Type your question")

    audio_input = st.audio_input("Or say: 'Jarvis ...'")

    user_query = None

    # Text input
    if typed_input:
        user_query = typed_input

    # Voice input
    if audio_input:
        spoken_text = speech_service.transcribe(audio_input)
        st.write("🎤 You said:", spoken_text)

        activated, cleaned_query = speech_service.check_wake_word(spoken_text)

        if activated:
            st.success("🟢 Wake word detected")
            user_query = cleaned_query
        else:
            st.warning("Wake word not detected. Say 'Jarvis ...'")

    # -------------------------------------------------
    # RAG Execution
    # -------------------------------------------------
    if user_query and client:

        answer, context = rag.query(user_query, client=client)

        st.subheader("🤖 Answer")
        st.write(answer)

        with st.expander("🔍 Retrieved Context"):
            st.write(context)

        # -------------------------------------------------
        # Voice Output
        # -------------------------------------------------
        if st.toggle("🔊 Enable Voice Response", value=True):
            tts_service.speak(answer)

elif uploaded_file and not api_key:
    st.warning("Please enter your OpenAI API Key.")

