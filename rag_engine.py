from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma 
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os 

#Environment Variables
load_dotenv()

loader = DirectoryLoader('./data', glob='**/*.txt')
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(chunks, embedding, persist_directory='./vectorstore')
#vectordb.persist()

retriever = vectordb.as_retriever()
llm = OpenAI(temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, chain_type="stuff")

#Test query
query = "Can my landlord enter my house without notice?"
result = qa_chain.invoke(query)
print(result)