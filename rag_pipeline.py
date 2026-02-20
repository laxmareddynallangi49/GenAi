# app/rag_pipeline.py

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

def build_rag_chain(vector_db, llm, chat_history):

    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Loan Assistant. Use the context to answer. If unknown, say so.\n\nContext:\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = RunnableParallel({
        "context": retriever | format_docs,
        "input": RunnablePassthrough(),
        "chat_history": lambda x: [
            HumanMessage(content=m["content"]) if m["role"] == "user"
            else AIMessage(content=m["content"])
            for m in chat_history[-5:]
        ],
        "raw_docs": retriever
    }) | {
        "answer": qa_prompt | llm | StrOutputParser(),
        "sources": lambda x: x["raw_docs"]
    }

    return rag_chain