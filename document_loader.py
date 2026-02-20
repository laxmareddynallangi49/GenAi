# # # app/document_loader.py

# # import os
# # import tempfile
# # from langchain_community.document_loaders import TextLoader
# # from langchain_text_splitters import RecursiveCharacterTextSplitter

# # def process_uploaded_files(uploaded_files):
# #     all_docs = []

# #     for uploaded_file in uploaded_files:
# #         with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
# #             tmp.write(uploaded_file.getvalue())
# #             tmp_path = tmp.name

# #         loader = TextLoader(tmp_path)
# #         docs = loader.load()

# #         for d in docs:
# #             d.metadata["source"] = uploaded_file.name

# #         non_empty_docs = [d for d in docs if d.page_content.strip()]
# #         all_docs.extend(non_empty_docs)
# #         os.remove(tmp_path)

# #     if not all_docs:
# #         return []

# #     splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
# #     chunks = splitter.split_documents(all_docs)

# #     return [c for c in chunks if c.page_content.strip()]




# # app/document_loader.py

# import os
# import tempfile
# import pandas as pd

# from langchain_community.document_loaders import (
#     TextLoader,
#     PyPDFLoader,
#     CSVLoader,
#     UnstructuredExcelLoader
# )
# from langchain_text_splitters import RecursiveCharacterTextSplitter


# def load_single_file(uploaded_file):
#     suffix = uploaded_file.name.split(".")[-1].lower()

#     with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
#         tmp.write(uploaded_file.getvalue())
#         tmp_path = tmp.name

#     try:
#         if suffix == "txt":
#             loader = TextLoader(tmp_path)

#         elif suffix == "pdf":
#             loader = PyPDFLoader(tmp_path)

#         elif suffix == "csv":
#             loader = CSVLoader(tmp_path)

#         elif suffix in ["xlsx", "xls"]:
#             loader = UnstructuredExcelLoader(tmp_path)

#         else:
#             return []

#         docs = loader.load()

#         for d in docs:
#             d.metadata["source"] = uploaded_file.name

#         return docs

#     finally:
#         os.remove(tmp_path)


# # kuber/document_loader.py

# import pandas as pd
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document


# def process_uploaded_files(uploaded_files):
#     all_docs = []
#     customer_df = None

#     for file in uploaded_files:
#         if file.name.endswith(".csv"):
#             df = pd.read_csv(file)
#             customer_df = df

#             # Convert rows into documents for optional RAG search
#             for _, row in df.iterrows():
#                 content = ", ".join(f"{col}: {row[col]}" for col in df.columns)
#                 all_docs.append(Document(page_content=content))

#     if not all_docs:
#         return None, None

#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     chunks = splitter.split_documents(all_docs)

#     return chunks, customer_df


# # def process_uploaded_files(uploaded_files):
# #     all_docs = []

# #     for uploaded_file in uploaded_files:
# #         docs = load_single_file(uploaded_file)

# #         for d in docs:
# #             lines = d.page_content.split("\n")

# #             for line in lines:
# #                 if line.strip():
# #                     from langchain_core.documents import Document
# #                     all_docs.append(
# #                         Document(
# #                             page_content=line.strip(),
# #                             metadata=d.metadata
# #                         )
# #                     )

# #     return all_docs

# # def process_uploaded_files(uploaded_files):
# #     all_docs = []

# #     for uploaded_file in uploaded_files:
# #         docs = load_single_file(uploaded_file)
# #         non_empty_docs = [d for d in docs if d.page_content.strip()]
# #         all_docs.extend(non_empty_docs)

# #     if not all_docs:
# #         return []

# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=800,
# #         chunk_overlap=80
# #     )

# #     chunks = splitter.split_documents(all_docs)
# #     return [c for c in chunks if c.page_content.strip()]



# kuber/document_loader.py

# import pandas as pd
# from langchain_core.documents import Document
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import PyPDFLoader
# import tempfile


# def process_uploaded_files(uploaded_files):
#     all_docs = []
#     customer_df = None

#     for file in uploaded_files:

#         # ---------------- CSV ----------------
#         if file.name.endswith(".csv"):
#             df = pd.read_csv(file)
#             customer_df = df

#             for _, row in df.iterrows():
#                 content = ", ".join(f"{col}: {row[col]}" for col in df.columns)
#                 all_docs.append(Document(page_content=content))

#         # ---------------- XLSX ----------------
#         elif file.name.endswith(".xlsx"):
#             df = pd.read_excel(file)
#             customer_df = df

#             for _, row in df.iterrows():
#                 content = ", ".join(f"{col}: {row[col]}" for col in df.columns)
#                 all_docs.append(Document(page_content=content))

#         # ---------------- TXT ----------------
#         elif file.name.endswith(".txt"):
#             text = file.read().decode("utf-8")
#             all_docs.append(Document(page_content=text))

#         # ---------------- PDF ----------------
#         elif file.name.endswith(".pdf"):
#             with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#                 tmp.write(file.read())
#                 tmp_path = tmp.name

#             loader = PyPDFLoader(tmp_path)
#             pdf_docs = loader.load()
#             all_docs.extend(pdf_docs)

#     if not all_docs:
#         return None, None

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=100
#     )

#     chunks = splitter.split_documents(all_docs)

#     return chunks, customer_df

# kuber/document_loader.py

import pandas as pd
import tempfile
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


def process_uploaded_files(uploaded_files):
    """
    Processes uploaded CSV, XLSX, TXT, PDF files.
    Returns:
        chunks (for vector DB)
        customer_df (structured dataframe if CSV/XLSX found)
    """

    all_docs = []
    customer_df = None

    for file in uploaded_files:

        filename = file.name.lower()

        # ===============================
        # CSV FILE
        # ===============================
        if filename.endswith(".csv"):
            df = pd.read_csv(file)

            # Clean column names
            df.columns = df.columns.str.strip()

            customer_df = df

            # Convert each row into a document
            for _, row in df.iterrows():
                content = ", ".join(
                    f"{col}: {row[col]}" for col in df.columns
                )
                all_docs.append(Document(page_content=content))

        # ===============================
        # XLSX FILE
        # ===============================
        elif filename.endswith(".xlsx"):
            df = pd.read_excel(file)

            df.columns = df.columns.str.strip()

            customer_df = df

            for _, row in df.iterrows():
                content = ", ".join(
                    f"{col}: {row[col]}" for col in df.columns
                )
                all_docs.append(Document(page_content=content))

        # ===============================
        # TXT FILE
        # ===============================
        elif filename.endswith(".txt"):
            text = file.read().decode("utf-8", errors="ignore")
            all_docs.append(Document(page_content=text))

        # ===============================
        # PDF FILE
        # ===============================
        elif filename.endswith(".pdf"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(file.read())
                tmp_path = tmp.name

            loader = PyPDFLoader(tmp_path)
            pdf_docs = loader.load()
            all_docs.extend(pdf_docs)

    # ===============================
    # If nothing processed
    # ===============================
    if not all_docs:
        return None, None

    # ===============================
    # Split for vectorization
    # ===============================
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(all_docs)

    return chunks, customer_df