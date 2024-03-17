from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
from langchain_google_genai import GoogleGenerativeAI
import PyPDF2 as pdf
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from streamlit import session_state as ss
from streamlit_pdf_viewer import pdf_viewer

model = genai.GenerativeModel("gemini-pro")


def get_gemini_response(query, text, user_prompt):
    response = model.generate_content([query, text, user_prompt])
    return response.text


input_prompt = """
You are an invoice analysis specialist with exceptional skills in extracting information from various invoice formats. You will be presented with digital images of invoices and asked comprehensive questions to test your understanding of the invoice content.

Here are some examples of the questions you might be asked:

What is the total amount due on the invoice?
What is the description of the most expensive item listed?
Who issued the invoice?
When is the payment due?
Are there any discounts or taxes applied?
To perform well, 
you should be able to identify key invoice elements like:

* Seller and buyer information
* Date of invoice
* Description of goods or services provided
* Quantity and unit price
* Total amount due
* Payment terms (due date, discounts, penalties)
* Taxes
* names of the person and the bank
Do your best to answer all questions accurately and comprehensively based on the information presented in the invoice image.
"""


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


st.set_page_config(page_title="Invoice reader")

st.header("Invoice reader")


if "pdf_ref" not in ss:
    ss.pdf_ref = None


uploaded_file = st.file_uploader("Upload PDF file", type=("pdf"), key="pdf")

if ss.pdf:
    ss.pdf_ref = ss.pdf


if ss.pdf_ref:
    binary_data = ss.pdf_ref.getvalue()
    pdf_viewer(input=binary_data, width=700)
if uploaded_file is not None:
    input = st.text_input("Enter your query ", key="input")
submit = st.button("Submit")
if submit:
    pdf_data = input_pdf_text(uploaded_file)
    response = get_gemini_response(input, pdf_data, input_prompt)
    st.subheader("The Response is")
    st.write(response)
