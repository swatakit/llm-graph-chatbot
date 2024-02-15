import sys
import os
import streamlit as st
from langchain_community.graphs import Neo4jGraph

# Insert the parent directory into the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
graph = Neo4jGraph(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
)