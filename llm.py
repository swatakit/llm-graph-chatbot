import streamlit as st
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL


llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model=OPENAI_MODEL,
    temperature=0.0
)

from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    openai_api_key=OPENAI_API_KEY
)