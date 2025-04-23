import streamlit as st
import pdfplumber
import tabula
import pandas as pd
import plotly.express as px

# Function to extract data from the PDF
def extract_document_data(pdf_file):
    text = ""
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    tables = tabula.read_pdf(pdf_file, pages="all", multiple_tables=True)
    return text, tables

# Function to clean the extracted data
def clean_data(tables):
    # Assuming the second table is the one with transaction data
    table_1 = tables[1]  # You can modify this based on your needs
    table_1['Transaction Date'] = pd.to_datetime(table_1['Transaction Date'], errors='coerce')
    table_1['Withdrawal'] = pd.to_numeric(table_1['Withdrawal'], errors='coerce')
    table_1['Deposit'] = pd.to_numeric(table_1['Deposit'], errors='coerce')
    table_1['Balance'] = pd.to_numeric(table_1['Balance'], errors='coerce')
    table_1 = table_1.dropna(subset=['Transaction Date', 'Balance'])
    return table_1

# Streamlit app interface
st.title("Financial Document Analyzer")

st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Extract data from the uploaded PDF
    st.subheader("Extracted Text")
    text, tables = extract_document_data(uploaded_file)
    st.text(text[:1000])  # Display the first 1000 characters of the extracted text
    
    # Clean data and show table preview
    st.subheader("Transaction Data")
    cleaned_data = clean_data(tables)
    st.write(cleaned_data.head())  # Show a preview of the cleaned data
    
    # Visualize the data (Account balance over time)
    st.subheader("Account Balance Over Time")
    fig = px.line(cleaned_data, x='Transaction Date', y='Balance', title='Account Balance Over Time')
    st.plotly_chart(fig)
