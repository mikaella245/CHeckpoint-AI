from playwright.sync_api import sync_playwright
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
import time
import os

load_dotenv()

BASE_URL = "https://www.asloca.ch"
RENT_KEYWORDS = ["loyer", "bail", "augmentation", "révision", "loyers", "resiliation","resilier", "taux","ICP", "loyer echelonné", "loyer indexé", "contestation", "contester"]  # can expand later

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

def scrape_asloca_articles():
    articles = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"{BASE_URL}/actualites")
        time.sleep(2)

        # Grab all article links under /actualites/
        links = page.query_selector_all("a[href^='/actualites/']")
        article_urls = set()
        for link in links:
            href = link.get_attribute("href")
            if href != "/actualites":
                article_urls.add(BASE_URL + href)

        # Visit each article
        for url in article_urls:
            page.goto(url)
            time.sleep(1)
            title = page.query_selector("h1").inner_text() if page.query_selector("h1") else ""
            paragraphs = page.query_selector_all("article p")
            content = "\n".join([p.inner_text() for p in paragraphs])

            # Minimal filter: keep only if title or content has rent keywords
            if any(keyword.lower() in title.lower() or keyword.lower() in content.lower() for keyword in RENT_KEYWORDS):
                articles.append({
                    "url": url,
                    "title": title,
                    "content": content
                })

        browser.close()
        
    return articles
   
articles = scrape_asloca_articles()
def process_scraped_articles(articles, text_splitter):
    scraped_docs = [
        Document(
            page_content=a["content"],
            metadata={"title": a["title"], "url": a["url"]}
        ) 
        for a in articles
    ]

    return text_splitter.split_documents(scraped_docs)

split_scraped_docs = process_scraped_articles(articles, text_splitter)

#if __name__ == "__main__":
#    data = scrape_asloca_articles()
#   print(f"Scraped {len(data)} rent-related articles")
 #   for art in data:
 #       print(art["title"], art["url"])

PDF_Folder = Path("data")
pdf_loader = DirectoryLoader(str(PDF_Folder), glob="*.pdf", loader_cls=PyPDFLoader)
pdf_docs = pdf_loader.load()


split_docs = text_splitter.split_documents(pdf_docs)


all_split_docs = split_docs + split_scraped_docs
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
vectorstore = Chroma.from_documents(documents=all_split_docs, embedding=embeddings)


llm=ChatOpenAI(model="gpt-4")
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an expert Swiss tenant assistant. Your name is CHarly.
Use the following context from Asloca articles and PDFs to answer questions about rent, tenant rights, and fairness.
Be human, clear, concise, friendly, and empowering — you're the big sister who helps tenants stand up for themselves.
The utmost goal of your answers is to calm and empower tenants, so that they contest their rent.
Answer in English.

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

query = "Can I contest my rent?"
answer = qa_chain.invoke(query)
print(answer)