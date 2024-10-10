import json
import os
import shutil
import time
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from dotenv import load_dotenv


load_dotenv()
OPENAI_KEY = os.getenv("API_KEY")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
if not OPENAI_KEY or not OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT:
    raise ValueError("API_KEY or OPENAI_API_VERSION or AZURE_OPENAI_ENDPOINT is missing from environment variables")


# return chunks of documents
def get_chunks(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    print("fetching data from the json file...")
    documents = []

    for video in data:
        video_url = video["url"]
        video_title = video["title"]
        # conver each chapter into a document
        for chapter in video["chapters"]:
            chapter_title = chapter["title"]
            metadata = {
                "video_title": video_title,
                "video_url": video_url,
                "chapter_title": chapter_title
            }
            document = Document(
                page_content= chapter["statements"],
                metadata=metadata
            )
            documents.append(document)

    print("splitting documents into chunks...")
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=0, length_function=get_token_count)
    chunks_of_documents = text_splitter.split_documents(documents)
    print(f"Splitting done. Number of chunks: {len(chunks_of_documents)}")
    return chunks_of_documents


# return token count of text
def get_token_count(text):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)


# Initialize the vector store for given chunks
def init_vector_store(chunks):
    print("Initializing the vector store...")

    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_version=OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=OPENAI_KEY
    )

    batch_size = 10
    db = None

    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i+batch_size]
        
        if db is None:
            db = FAISS.from_documents(batch_chunks, embeddings)
        else:
            db.add_documents(batch_chunks)
        
        print("---------------------")
        print(f"Processed batch {i // batch_size + 1}/{(len(chunks) + batch_size - 1) // batch_size}")
        print("Sleeping for 20 seconds...")
        time.sleep(20)
        print("Resuming...")
        print("---------------------\n")

    if os.path.exists("local_vector_store"):
        shutil.rmtree("local_vector_store")
        print("Deleted existing vector store")

    # Save the complete vector store after processing all batches
    db.save_local("local_vector_store")
    print("Initialized and saved the vector store")


def main():
    chunk_list = get_chunks("data/data.json")
    init_vector_store(chunk_list)


if __name__ == "__main__":
    main()