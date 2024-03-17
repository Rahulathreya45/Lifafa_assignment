from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text


def input_image_setup(image_path):
    try:
        image = Image.open(image_path)
        image_parts = [{"mime_type": image.format, "data": image.tobytes()}]
        return image_parts
    except FileNotFoundError:
        print("Error: Image file not found!")
        return None


def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


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

st.set_page_config(page_title="Invoice reader")

st.header("Invoice reader")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
    input = st.text_input("Enter your query ", key="input")

submit = st.button("Submit")
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(
        input_prompt,
        image_data,
        input,
    )
    st.subheader("The Response is")
    st.write(response)
