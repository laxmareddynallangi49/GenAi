import streamlit as st
#from pdfminer.high_level import extract_text
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import tempfile
import os
import httpx
import tiktoken
import json
import pandas as pd
import re

# Set up token cache directory
tiktoken_cache_dir = "./token"
os.environ["TIKTOKEN_CACHE_DIR"] = tiktoken_cache_dir

# Disable SSL verification for httpx client
client = httpx.Client(verify=False)

# LLM and Embedding setup
llm = ChatOpenAI(
    base_url="https://genailab.tcs.in",
    model="azure/genailab-maas-gpt-4o",
    api_key="sk-Q2w4ANxRsk9dDm4Z7WovVw",
    http_client=client
)


# Streamlit UI setup
st.set_page_config(page_title="Test Data generation")
st.title("Test Data generation")

upload_file = st.file_uploader("Upload a text file")

if upload_file:
    _,file_extension = os.path.splitext(upload_file.name)
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(upload_file.read())
        temp_file_path = temp_file.name
    
    if file_extension == ".json":
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            file_content = json.dumps(json.load(f), indent=2)

    elif file_extension == ".txt":
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

    elif file_extension == ".csv":
        df = pd.read_csv(temp_file_path)
        file_content = df.to_csv(index=False)

    # Step 1: Extract text
    #raw_text = temp_file.read()
    #with open("sample_log.txt", "r", encoding="utf-8") as file:
    #    raw_text = file.read()

    # Step 5: Ask summarization prompt
    #summary_prompt = st.text_input("Enter the prompt")
    #print(schema_data)
    output_type = st.selectbox(
    "Choose Format:",
    ["Json", "CSV"])
    if output_type:
    
        summary_prompt = f"""
    Generate test data based on the database schema and data constraints.
    Database Schema: {file_content}
"""

    
        with st.spinner("Creating test data..."):
            result = llm.invoke(summary_prompt)
        result_text = result.content
        match = re.search(r"```json\n(.*?)\n```", result_text, re.DOTALL)
        if match:
            embedded_json_str = match.group(1)
        else:
            embedded_json_str = result_text  # fallback if no wrapping

        # Parse JSON
        try:
            parsed_data = json.loads(embedded_json_str)
            st.success("Test data generated and parsed successfully!")
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON: {e}")
            parsed_data = None
        if output_type == "JSON":
            json_data = json.dumps(parsed_data, indent=4)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name="test_data.json",
                mime="application/json"
            )

        elif output_type == "CSV":
            # Let user choose which table to export
            table_names = list(parsed_data.keys())
            selected_table = st.selectbox("Select table to export:", table_names)

            df = pd.DataFrame(parsed_data[selected_table])
            csv_data = df.to_csv(index=False)

            st.download_button(
                label=f"Download CSV ({selected_table})",
                data=csv_data,
                file_name=f"{selected_table}.csv",
                mime="text/csv"
            )

