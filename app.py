from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
from google import genai

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def get_gemini_response(input_prompt, pdf_content, additional_prompt):
    combined_prompt = f"""
    You are a resume‑ranking assistant.
    {input_prompt}
    {pdf_content}
    {additional_prompt}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=combined_prompt
    )
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read PDF bytes
        pdf_bytes = uploaded_file.read()
        
        # Encode PDF as base64
        pdf_base64 = base64.b64encode(pdf_bytes).decode()
        
        return pdf_base64
    else:
        raise FileNotFoundError("No file Uploaded")

    
# Streamlit App

st.set_page_config(page_title="ATS Scoring")
st.header("Application Tracking System")
input_text = st.text_area("Job Description: ",key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)",type=["pdf"])

if uploaded_file is not None:
    st.write("Successfully Uploaded Resume!")

submit1 = st.button("Tell me about Resume") 

submit2 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR with tech Experience in the field of any one of the job role from Data Science, Data Analytics, Big Data Engineer,web development 
your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate profile aligns with the role.
Highlight the strength and weakness of the applicant in relation to the specified role.
"""

input_prompt2 = """
You are an skilled ATS(Application Tracking System) scanner with deep understanding of any one of the job role from Data Science, Data Analytics, 
Big Data Engineer,web development and deep ATS functionality.
your task is to evaluate the resume against the job description. give me the percentage match if the resume matches the job description.
First the ouput come as percentage and then keyword missing.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response= get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please Upload resume!")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response= get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please Upload resume!")
