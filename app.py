
import streamlit  as st
import google.generativeai as genai
import os
import PyPDF2 as pdf

from dotenv import load_dotenv

load_dotenv() ##load all the enviourmanet vairables

genai.configure(api_key =os.getenv("GOOGLE_API_KEY"))

## Gemini pro response
def get_gemini_response(input):
  model = genai.GenerativeModel('gemini-pro')
  response=model.generate_content(input)
  return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_number in range(len(reader.pages)):  # Iterate through the page numbers
        page = reader.pages[page_number]  # Access the page using indexing
        text += str(page.extract_text())
    return text


##prompt Template
input_prompt ="""
hey act like a skilled or very experience ATS (Apllication Tracking System) with deep understanding of tech field, Softwarre Engineering,Data Science, Data Analyst, and big data engineer. Your task is to evaluate the resume based on the given job description you must consider the job market is very competitive and you should provide best assistance for improving the resume. assign the percentage Matching based on Job Description and the missing keywords with high accuracy
resume:{text}
Description:{jd}
I Want the response in one single String having structure
{{"JD Match":"%",
  "Missing keywords:[]", 
  "Profile Summary":""}}
"""

### Streamlit app
st.title("Smart ATS")
st.text("Improving your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload your Resume",type="pdf", help= "Please Upload the pdf")

submit= st.button("Submit")



if submit:
  if uploaded_file is not None:
    text=input_pdf_text(uploaded_file)
    response=get_gemini_response(input_prompt)
    st.subheader(response)

