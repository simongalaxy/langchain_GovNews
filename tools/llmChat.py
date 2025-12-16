# chat_with_news_chroma_ollama.py
# Run this file → you can now ask questions about your news articles


from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_classic.schema.runnable import RunnableParallel, RunnablePassthrough
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

import os
from dotenv import load_dotenv
load_dotenv()

from tools.ChromaDBHandler import ChromaDBHandler

class NewsChat:
    def __init__(self, logger, DBHandler: ChromaDBHandler):
        self.logger = logger
        self.model_name = os.getenv("OLLAMA_LLM_MODEL")
        self.llm = ChatOllama(
            model= self.model_name,             # or "mistral", "phi3", "gemma2:9b", whatever you have
            temperature=0.3                                  # low = factual summaries
        )
        self.prompt_template = """
            You are a smart news assistant.
            Use only the following news articles to answer the question.
            If you don't know, say "I don't have enough information".
            always say "Thank you for asking !" at the end of the answer.

            News articles:
            {context}

            Question: 
            {question}

            Answer naturally and concisely:
            """
        self.retriever = DBHandler.retrieve_documents_from_chromadb()
        
        self.PROMPT = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "question"]
        )
        
        self.doc_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=self.PROMPT
        )
        
        self.rag_chain = RunnableParallel({
            "context": self.retriever,
            "question": RunnablePassthrough()
        }) | self.doc_chain
        
        self.logger.info("Class - NewsChat initiated.")
    
    # 6. Chat loop – just run this file!
    def run_chat_loop(self) -> None:
        print("Ready! Ask anything about the news (type 'q' to quit)\n")
        while True:
            question = input("You: ")
            if question.lower() == 'q':
                print("Bye!")
                break
            
            print("\nThinking...\n")
            try:
                answer = self.rag_chain.invoke(question)
                print("News Bot:", answer)
                print("-" * 100)
            except Exception as e:
                print(f"Error: {e}\n")
            
        return