import streamlit as st
import requests
import json

st.title("Survey Analysis with CrewAI")

# Input for the survey question
survey_question = st.text_area("Enter the Survey Question:", "")

# File uploader for q1_data
q1_data_file = st.file_uploader("Upload q1_data JSON File:", type="json")

# File uploader for q1_reasons
q1_reasons_file = st.file_uploader("Upload q1_reasons JSON File:", type="json")

# API URL
API_URL = "http://ritualstestfastapi-production.up.railway.app"

# Process Data Button
if st.button("Run Analysis"):
    try:
        # Validate the survey question
        if not survey_question.strip():
            st.error("Survey question cannot be empty.")
            st.stop()

        # Validate file uploads
        if not q1_data_file or not q1_reasons_file:
            st.error("Please upload both q1_data and q1_reasons JSON files.")
            st.stop()

        # Read and parse JSON files
        q1_data = json.load(q1_data_file)
        q1_reasons = json.load(q1_reasons_file)

        # Send data to API
        response = requests.post(API_URL, json={
            "q1_data": q1_data,
            "q1_reasons": q1_reasons,
            "q1_question_text": survey_question
        })

        # Handle API response
        if response.status_code == 200:
            result = response.json().get("result")
            st.success("Analysis Complete!")
            st.markdown(result)
        else:
            st.error(f"API Error: {response.status_code} - {response.json().get('detail')}")
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON format in one of the uploaded files: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
