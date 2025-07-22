from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma 
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
import os 

#Environment Variables
load_dotenv()

def ask_checkpoint(query):
    return qa_chain.invoke(query)


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
