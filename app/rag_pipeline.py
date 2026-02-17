from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP, TOP_K
from app.embeddings import create_vectorstore
from app.llm_service import generate_answer

class RAGPipeline:

    def __init__(self, documents):
        self.documents = documents
        self.vectorstore = self._build_vectorstore()

    def _build_vectorstore(self):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(self.documents)
        return create_vectorstore(chunks)

    def query(self, question: str):
        docs = self.vectorstore.similarity_search(question, k=TOP_K)

        context = "\n".join([doc.page_content for doc in docs])

        answer = generate_answer(context, question)

        return answer, context
