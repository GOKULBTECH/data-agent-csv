import streamlit as st
from agent.basic_data_agent import CSVDataAgent

st.title("CSV Data Agent")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    with open("temp.csv", "wb") as f:
        f.write(uploaded_file.read())
    agent = CSVDataAgent("temp.csv")
    query = st.text_input("Ask a question about the data")
    if query:
        st.write("Answer:")
        st.write(agent.handle_query(query))
