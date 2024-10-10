from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureOpenAIEmbeddings
from langchain.memory import ConversationBufferWindowMemory
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
OPENAI_KEY = os.getenv("API_KEY")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
if not OPENAI_KEY or not OPENAI_API_VERSION or not AZURE_OPENAI_ENDPOINT:
    raise ValueError("API_KEY or OPENAI_API_VERSION or AZURE_OPENAI_ENDPOINT is missing from environment variables")

embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_version=OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=OPENAI_KEY
)

vector_store = FAISS.load_local("local_vector_store", embeddings, allow_dangerous_deserialization=True)

llm = AzureChatOpenAI(model="gpt-35-turbo", temperature=0, api_key=OPENAI_KEY, azure_endpoint=AZURE_OPENAI_ENDPOINT, api_version=OPENAI_API_VERSION)

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5)

chat_template = """
You are an AI assistant named "PodQuery," designed to answer user questions based on podcast transcript snippets. You will be provided with multiple snippets as "Context," each relating to a specific chapter of the podcast.

### Instructions:

1. **Context Structure**:
    - Each snippet is separated by two newlines (`\n\n`).
    - Snippets are formatted as:
      ```
      (video_title: [Title of the video]
      video_url: [URL of the video]
      chapter_title: [Chapter or subtopic title]
      contents: [Time stamp][Speaker][Transcript]...)
      ```
    - Example:
      ```
      (video_title: Talking Tech and AI with Tim Cook!
      video_url: https://youtu.be/pMX2cQdPubk?si=2GoNXRAKT4co1X0Q
      chapter_title: AI vs Apple Intelligence
      contents: [00:03:00][mkbhd][All right, Tim]
                [00:04:00][tim][Great to see you])
      ```

2. **User Query Understanding**:
    - Analyze the user's question and identify the relevant snippet or chapter from the context to answer it.

3. **Response Construction**:
    - Provide a well-structured answer using the information from the transcript snippets.
    - Reference specific excerpts from the transcript to support your answer.

4. **Citation Requirement**:
    - At the end of every response, cite the video and chapter using this format(strating time stamp is enough):
      ```
      Video title: [Video title] | Video URL: [Video URL] | Chapter title: [Chapter title] | Time stamp: [strating time stamp]
      ```

### CONTEXT:
{context}

### CHAT HISTORY:
{chat_history}

### User Question:
{question}

### AI Assistant Response:
"""

chat_prompt = PromptTemplate(
    input_variables=["context", "chat_history", "question"],
    template=chat_template
)

chat_chain = chat_prompt | llm | StrOutputParser()


def format_docs(docs):
    formatted_docs = []
    for doc, score in docs:
        metadata = doc.metadata
        video_title = metadata.get("video_title", "")
        video_url = metadata.get("video_url", "")
        chapter_title = metadata.get("chapter_title", "")
        formatted_text = f"(video_title: {video_title}\nvideo_url: {video_url}\nchapter_title: {chapter_title}\n\contents: {doc.page_content})"
        formatted_docs.append(formatted_text)
    return "\n\n".join(formatted_docs)


def chat(message):
    if not os.path.exists("local_vector_store"):
        return "Error: No local vector store found in /local_vector_store"
    
    context_docs = vector_store.similarity_search_with_score(message, k=4)
    if not context_docs:
        return "Sorry, I couldn't find any relevant information."
    
    context = format_docs(context_docs)
    # print(context)
    chat_history = memory.load_memory_variables({})['chat_history']
    
    response = chat_chain.invoke({
        "question": message,
        "context": context,
        "chat_history": chat_history
    })
    
    memory.save_context({"input": message}, {"output": response})
    
    return response


def main():
    print("Welcome to the chatbot! (Type 'exit' to quit)\n")
    while True:
        user_input = input("\nQuestion: ").strip()

        if not user_input:
            print("Error: Input is empty")
            continue

        if user_input.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break

        response = chat(user_input)
        print("\nResponse: ", response)


if __name__ == "__main__":
    main()
