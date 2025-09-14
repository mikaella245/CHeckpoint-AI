import csv
import ast  # to convert string embeddings into lists
import numpy as np
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document
from langchain_openai import ChatOpenAI 
from langchain.chains.retrieval_qa.base import RetrievalQA
import gradio as gr
import json 
from dotenv import load_dotenv
import os 
import faiss

load_dotenv()

csv_file = pd.read_csv("data_CHeckpoint.csv")
csv_file = csv_file.dropna(subset=["raw_embedding2"]).copy()
csv_file["raw_embedding2"] = csv_file["raw_embedding2"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

embeddings = [list(map(float, e)) for e in csv_file["raw_embedding2"].tolist()]

# CSV rows to LangChain Documents
docs = [Document(page_content=row['sentences'], metadata={"title": row["title"]}) 
        for _, row in csv_file.iterrows()]


# Embeddings to float32 numpy arrays converter
embedding_arrays = [np.array(e, dtype=np.float32) for e in embeddings]
embedding_matrix = np.vstack(embedding_arrays) 

# FAISS index
dimension = embedding_matrix.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 distance
index.add(embedding_matrix)

# Embedding function placeholder
embeddings_fn = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))  # you can still use this later if you want to add docs


vectorstore = FAISS.from_documents(
    documents=docs,
    embedding=embeddings_fn
    )


llm = ChatOpenAI(model_name="gpt-3.5-turbo")  
qa_chain = RetrievalQA.from_llm(llm=llm, retriever=vectorstore.as_retriever())


def ask_checkpoint(question):
    try:
        response = qa_chain.invoke({"query": question})
        return response["result"]
    except Exception as e:
        print("Error:", e)
        return "Something went wrong. Check the console for details."


with gr.Blocks(theme="soft") as app:
     
     gr.Markdown(
        """
        ###  ⚖️ CHeckpoint AI - Cheaper than a lawyer. Speaks your language.
       Your Swiss Tenant Rights Assistant. Ask me your questions! Now Mantis AI powered!
        DISCLAIMER: CHeckpoint AI is a proof-of-concept tool intended for informational purposes only. It does not constitute legal advice and should not be relied upon as a substitute for consultation with a qualified legal professional. Always seek professional legal assistance when dealing with tenancy issues or legal disputes.Use of this tool is at your own discretion.

        """)
     
     question = gr.Textbox(label="Your Question", placeholder="Can my landlord enter the house without prior notice?")
     answer = gr.Textbox(label="Answer")

     btn = gr.Button("Ask CHeckpoint")
     btn.click(fn=ask_checkpoint, inputs=question, outputs=answer)

app.launch(share=True)
