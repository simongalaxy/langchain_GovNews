from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_ollama.embeddings import OllamaEmbeddings
from tools.markdownProcesser import markdown_to_text

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
        self.logger.info("Class - ChromaDBHanlder initiated.")

    
    # add a new document to chromaDB.
    def add_document_to_chromaDB(self, jobAd, keyword:str) -> None:
        chunks = self.text_splitter.split_text(text=markdown_to_text(result=jobAd))
        self.logger.info(f"chunks done - {jobAd.url}.")
        
        documents = []
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk,
                metadata={
                    "keyword": keyword,
                    "source_url": jobAd.url,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                },
                id=f"{jobAd.url}#chunk={i}"
            )
            documents.append(doc)
        
        self.vectorstore.add_documents(documents=documents, ids=[doc.id for doc in documents])
        self.logger.info(f"Added a Job Ad to ChromaDB - url: {jobAd.url}")

        return
    
    
    
    # add new documents to chromaDB.
    def add_jobAds_to_chromaDB(self, jobAds, keyword:str) -> None:
        
        count = 0
        for i, jobAd in enumerate(jobAds[1:], start=1):
            existing = self.vectorstore.get(where={"source_url": jobAd.url}) # check any existing job ad.
            if not existing["ids"]:
                self.add_document_to_chromaDB(
                    jobAd=jobAd, 
                    keyword=keyword
                )
                count += 1
        self.logger.info(f"total {count} jobAds added to ChromaDB.")        
        
        return
    
    # retrieve documents from chromaDB.
    def get_documents_from_chromaDB(self, keyword:str) -> List[Document]:
        return self.vectorstore.similarity_search(
            "", 
            k=10000, 
            filter={
                "keyword": keyword
                }
            )
    
    # retrieve chunks from chromaDB by keyword.
    def retrieve_chunks_by_keyword(self, keyword: str, max_docs: int = 10000) -> List[Document]:
        """Retrieve all chunks filtered by keyword (no similarity needed for full corpus analysis)."""
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": max_docs, "filter": {"keyword": keyword}}
        )
        chunks = retriever.invoke("")  # Empty query to get all filtered
        
        return chunks