from playwright.async_api import async_playwright
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import DirectoryLoader 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_classic.docstore.document import Document
from langchain_classic.prompts import PromptTemplate 
from pydantic import BaseModel
import os
import asyncio

load_dotenv()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


#if __name__ == "__main__":
#    data = scrape_asloca_articles()
#   print(f"Scraped {len(data)} rent-related articles")
 #   for art in data:
 #       print(art["title"], art["url"])

PDF_Folder = Path("data")
pdf_loader = DirectoryLoader(str(PDF_Folder), glob="*.pdf", loader_cls=PyPDFLoader)
pdf_docs = pdf_loader.load()


split_docs = text_splitter.split_documents(pdf_docs)


all_split_docs = split_docs
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
vectorstore = Chroma.from_documents(documents=all_split_docs, embedding=embeddings)


llm=ChatOpenAI(model="gpt-4")
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an expert Swiss tenant assistant. Your name is CHarly.
Use the following context from Asloca articles and PDFs to answer questions about rent, tenant rights, and fairness.
Be human, clear, concise, friendly, and empowering — you're the big sister who helps tenants stand up for themselves.
The utmost goal of your answers is to calm and empower tenants, so that they contest their rent. Mention in parentheses the article of the swiss code of obligations that your answer is based on and next to the number of the article add only CO.
WITHOUT stopping to be encouraging, NEVER use phrases like "Your landlord is within his rights to raise your rent"
Don't ever say "standing up for your rights can be empowering". It is unatural. Don't use "--" in your answers.
Use English and resoond in:
- Two or three brief actionable points
- One or two short empathetic sentence
- One short closing sentence
Do not write long dense paragraphs."

Context:
{context}

Question:
{question}

Answer:
"""
)

qa_chain = RetrievalQA.from_chain_type(
    retriever=vectorstore.as_retriever(),
    llm=llm,
    chain_type_kwargs={"prompt": prompt_template}
)

#query = "Can I contest my rent?"
#answer = qa_chain.invoke(query)
#print(answer)

