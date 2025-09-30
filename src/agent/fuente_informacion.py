from langchain.docstore.document import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


docs =[]
embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")
vectorstore = InMemoryVectorStore.from_documents(documents=docs,
                                    embedding=embed_model)

documents = []
for filename in os.listdir("./tut-docs"):
    if filename.endswith(".txt"):
        with open(os.path.join("./tut-docs", filename), "r") as file:
            text = file.read()
            documents.append({"content": text, "filename": filename})
store_docs = [
    Document(page_content=doc["content"], metadata={"filename": doc["filename"]})
    for doc in documents
]
# Split the documents into chunks for vector store
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(store_docs)

this_retriever = vectorstore.as_retriever(search_kwargs={"k":2})