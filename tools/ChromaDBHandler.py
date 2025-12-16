from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_ollama.embeddings import OllamaEmbeddings
# from tools.markdownProcesser import markdown_to_text

from typing import List
import json
import os

from dotenv import load_dotenv
load_dotenv()


class ChromaDBHandler:
    def __init__(self, logger):
        """
        Setup ChromaDB with Ollama embeddings and persistence.
        """
        self.logger = logger
        self.embeddings = OllamaEmbeddings(model=os.getenv("OLLAMA_EMBEDDINGS_MODEL"))
        self.vectorstore = Chroma(
            collection_name=os.getenv("COLLECTION_NAME"),
            embedding_function=self.embeddings,
            persist_directory=os.getenv("chromaDB_PATH"),
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=10
        )
        self.review_nos = 10
        self.logger.info("Class - ChromaDBHanlder initiated.")
    
    
    # add a new document to chromaDB.
    def add_document_to_chromaDB(self, result) -> None:
        chunks = self.text_splitter.split_text(text=result.markdown)
        self.logger.info(f"chunks done - {result.url}.")
        
        documents = []
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "title": result.metadata["title"],
                    "source_url": result.url,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                },
                id=f"{result.url}#chunk={i}"
            )
            documents.append(doc)
        
        self.vectorstore.add_documents(documents=documents, ids=[doc.id for doc in documents])
        self.logger.info(f"Added a news title: {result.metadata["title"]} to ChromaDB, url: {result.url}")

        return
    
    
    # add new documents to chromaDB.
    def add_News_to_chromaDB(self, results) -> None:
        
        count = 0
        for i, result in enumerate(results[1:], start=1):
            existing = self.vectorstore.get(where={"source_url": result.url}) # check any existing job ad.
            if not existing["ids"]:
                self.add_document_to_chromaDB(
                    result=result
                )
                count += 1
        
        self.logger.info(f"total {count} jobAds added to ChromaDB.")        
        
        return
    
    
    # retrieve documents from chromaDB.
    def retrieve_documents_from_chromadb(self):
        return self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": self.review_nos,
                "fetch_k": 20
            }
        )