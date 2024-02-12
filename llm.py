import streamlit as st
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model=os.environ["OPENAI_MODEL"],
    temperature=0.0
)

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    openai_api_key=os.environ["OPENAI_API_KEY"]
)