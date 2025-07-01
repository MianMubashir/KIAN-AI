import streamlit as st
import requests
import chardet
import pypandoc
from docx import Document  # For .docx files

API_URL = "http://127.0.0.1:5000"

st.title("📧 Meeting Minutes Draft Generator and Editor")

# Function to extract text from .docx files
def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to extract text from .doc files (using pypandoc)
def extract_text_from_doc(doc_file):
    output = pypandoc.convert_file(doc_file, 'plain')
    return output

# Step 1: Upload meeting minutes
uploaded_file = st.file_uploader("Upload Meeting Minutes (Text file)", type=["txt", "docx", "doc"])

# To store the generated draft
draft = None

if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == "docx":
        meeting_minutes = extract_text_from_docx(uploaded_file)
    elif file_extension == "doc":
        meeting_minutes = extract_text_from_doc(uploaded_file)
    else:
        # Handling text files
        raw_data = uploaded_file.read()
        encoding_info = chardet.detect(raw_data)
        encoding = encoding_info['encoding'] if encoding_info['encoding'] else 'utf-8'
        
        try:
            meeting_minutes = raw_data.decode(encoding)
        except UnicodeDecodeError:
            st.error("The file could not be decoded. Please try uploading a different file.")
            st.stop()  # Stop further execution if decoding fails

    # Display the uploaded content in a text area
    st.text_area("Meeting Minutes", value=meeting_minutes, height=300)

    # Step 2: Button to generate the draft
    if st.button("Generate Draft"):
        # Send meeting minutes to Flask backend for draft generation
        with st.spinner("Generating draft..."):
            response = requests.post(f"{API_URL}/generate-email", json={
                "transcript": meeting_minutes,
                "scenario": "Generated Draft"  # Passing scenario as part of the request
            })
            if response.status_code == 200:
                draft_email = response.json().get("email")
                st.success("Draft generated successfully!")
                st.text_area("Generated Draft", value=draft_email, height=300)
                draft = draft_email  # Store the generated draft
            else:
                st.error("Failed to generate draft.")

    # Step 3: Chatbox for improving the draft
    if draft:
        st.subheader("Improve Draft")

        # User input for feedback or changes to the draft
        chat_input = st.text_area("Input your changes here:", height=100)

        if st.button("Improve Draft"):
            if chat_input:
                with st.spinner("Improving draft..."):
                    # Log the data being sent to the backend
                    st.write("Sending feedback to backend:", chat_input)

                    # Send improvement request to OpenAI API with user input (feedback)
                    response = requests.post(f"{API_URL}/generate-email", json={
                        "transcript": draft,  # Send current draft for improvement
                        "scenario": chat_input  # Send user feedback as "scenario"
                    })

                    # Debugging: Check the response from the backend
                    st.write(response.json())  # Check the backend response

                    if response.status_code == 200:
                        improved_draft = response.json().get("email")
                        st.success("Draft improved successfully!")
                        st.text_area("Improved Draft", value=improved_draft, height=300)
                    else:
                        st.error("Failed to improve draft.")
            else:
                st.warning("Please enter feedback or changes to improve the draft.")
