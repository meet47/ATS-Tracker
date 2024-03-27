from dotenv import load_dotenv
load_dotenv()
# To load all the environment variables

import json
import streamlit as st
import os
from PIL import Image
import PyPDF2
import google.generativeai as genai

import vertexai
from vertexai import generative_models
from vertexai.generative_models import GenerativeModel
from google.oauth2.service_account import Credentials

service_account_json_string = os.getenv('GCP_SERVICE_ACCOUNT_JSON')
service_account_info = json.loads(service_account_json_string)
google_credentials = Credentials.from_service_account_info(service_account_info)

PROJECT = "ats-tracker-418520"
LOCATION = "us-central1"

vertexai.init(project=PROJECT, location=LOCATION, credentials=google_credentials)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model=GenerativeModel('gemini-pro')
    reponse = model.generate_content(input)
    return reponse.text

def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text+=str(page.extract_text())
    return text

##Prompt Template
input_prompt = """
Het Act Like a skilled or very experience ATS(Application Tracking System) wth a deep understanding of tech fields, software engineering,
data science, data analyst, machine learning engineer, big data engineer, cloud architecture, cyber security analyst, IT support analyst.
Your task is to evaluate the resume based on the given job description. You must consider the job market is very competitive and you should
provide best assistance for improving the resumes. Assign the percentage matching based on job description and the missing keywords with
high accuracy
resume: {text}
description: {jd}

I want the response in one single string having the structure
{{"Job Description Match":"%", "Missing Keywords: []", "Profile Summary":""}}
"""

#Creating Streamlit App
st.title("Meet's Application Tracking System")
st.text("Make your resume ATS Friendly")
jd=st.text_area("Paste you Job Description Here")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload your resume in .pdf format")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)

