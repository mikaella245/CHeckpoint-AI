from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma 
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import gradio as gr
import os 

#Environment Variables
load_dotenv()

loader = DirectoryLoader('./data', glob='**/*.txt')
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embedding = OpenAIEmbeddings(model="text-embedding-3-small")
vectordb = Chroma.from_documents(chunks, embedding, persist_directory='./vectorstore')
#vectordb.persist()

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
retriever = vectordb.as_retriever()

qa_chain = RetrievalQA.from_llm(llm=llm, retriever=retriever)

def ask_checkpoint(question):
    response = qa_chain.invoke({"query": question})
    return response["result"]


with gr.Blocks(theme="soft") as app:
     
     gr.Markdown(
        """
        ###  ⚖️ CHeckpoint AI - Cheaper than a lawyer. Speaks your language.
       Your Swiss Tenant Rights Assistant. Ask me your questions! 
        DISCLAIMER: CHeckpoint AI is a proof-of-concept tool intended for informational purposes only. It does not constitute legal advice and should not be relied upon as a substitute for consultation with a qualified legal professional. Always seek professional legal assistance when dealing with tenancy issues or legal disputes.Use of this tool is at your own discretion.

        """)
     
     question = gr.Textbox(label="Your Question", placeholder="Can my landlord enter the house without prior notice?")
     answer = gr.Textbox(label="Answer")

     btn = gr.Button("Ask CHeckpoint")
     btn.click(fn=ask_checkpoint, inputs=question, outputs=answer)

app.launch(share=True)

#Test query
#print(qa_chain.invoke("Can a landlord enter without prior notice?"))