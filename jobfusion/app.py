import os
import sys
import logging
import streamlit as st
import docx2txt
from crewai import Crew, Task, Agent, Process
from crewai_tools import ScrapeWebsiteTool
from jobfusion_agents import JobFusion_Agents
from jobfusion_tasks import JobFusion_Tasks
from jobfusion2_agents import JobFusion2_Agents
from jobfusion2_tasks import JobFusion2_Tasks
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from Config import configure as cfg
from mock_interview_chatbot import *
import streamlit as st
from jobcrew import JobFusionCrew, JobFusionCrew2
# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# os.environ["OPENAI_API_KEY"] = ''

# # Load OpenAI API key from local env -- use ONLY for LOCAL development and streamlit deployment
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Load OpenAI API key from streamlit -- uncomment and use ONLY for streamlit cloud deployment
# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"] 
# openai_api_key = st.secrets["OPENAI_API_KEY"]

# Initialize OpenAI API models for use in the application
llm_35_turbo = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo', temperature=0.7)
manager_llm_35_turbo = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo')

def setup_streamlit_ui():
    st.write('Please upload your personal write-up, resume, and job description link.')
    st.text('')

    uploaded_resume = st.file_uploader('Step 1: Upload your resume:', type=['txt', 'docx', 'pdf'])
    uploaded_personal_writeup = st.file_uploader('Step 2: Upload your personal writeup:', type=['txt', 'docx', 'pdf'])
    jd_url_input = st.text_area(label='Step 3: Enter the URL of the job you are applying for:', placeholder='Paste the job description link/URL here...')

    return uploaded_resume, uploaded_personal_writeup, jd_url_input

# Main function to handle the application logic
def main():
    st.subheader('Welcome to JobFusion Crew !')
    st.write('**An AI-powered career advisory service with an agentic workflow to help you secure job interviews.**')
    
    tab1, tab2, tab3 = st.tabs(["Build Docs", "Edit Docs", "Career Chat"])

    # Tab 1: Build Documents (Resume and Cover Letter Creation)
    with tab1:
        uploaded_resume, uploaded_personal_writeup, jd_url_input = setup_streamlit_ui()
        if st.button('Start Processing'):
            if uploaded_resume and uploaded_personal_writeup and jd_url_input:
                st.write('Processing now....')
                logger.debug('Starting Agentic Workflow')

                # create output directory to store angent outputs
                os.makedirs("output/", exist_ok=True)

                # Save uploaded files
                resume_path = os.path.join("streamlit/", uploaded_resume.name)
                os.makedirs(os.path.dirname(resume_path), exist_ok=True)
                with open(resume_path, "wb") as f:
                    f.write(uploaded_resume.getbuffer())

                personal_writeup_path = os.path.join("streamlit/", uploaded_personal_writeup.name)
                os.makedirs(os.path.dirname(personal_writeup_path), exist_ok=True)
                with open(personal_writeup_path, "wb") as f:
                    f.write(uploaded_personal_writeup.getbuffer())

                # Run the JobFusionCrew process
                JobFusionCrew(resume_path, personal_writeup_path, jd_url_input).run()
                logger.debug('Agentic Workflow finished')
            else:
                st.error("Please upload both resume and personal writeup.")
                logger.error("Both resume and personal writeup are required.")

        col1, col2, col3 = st.columns([1, 1, 1])

        # Generate and download updated documents
        if col1.button('1 - Generate Resume'):
            with open('output/updated_resume.md', 'r') as file:
                resume_output = file.read()
            st.download_button('Download Resume', resume_output, file_name='updated_resume.txt', mime='text/plain')

        if col2.button('2 - Generate Cover Letter'):
            with open('output/coverletter.md', 'r') as file:
                cover_letter_output = file.read()
            st.download_button('Download Cover Letter', cover_letter_output, file_name='coverletter.txt', mime='text/plain')

        if col3.button('3 - Generate Interview Preparation Materials'):
            with open('output/interview_preparation_materials.txt', 'r') as file:
                interview_preparation_output = file.read()
            st.download_button('Download Interview Preparation', interview_preparation_output, file_name='interview_preparation_materials.txt', mime='text/plain')
    

    # Tab 2: Edit Documents (Resume and Cover Letter Modification based on Feedback)
    with tab2:
        st.subheader('Resume and Cover Letter Modification based on Your Feedback')

        # Gather user feedback for document modifications from four aspects
        missing_info = st.text_area(label='1. Which experiences or skills from your original resume do you believe were missed in the updated version?',
                                    placeholder="Please provide details here...")
        new_additions = st.text_area(label='2. Are there any additional achievements or project experiences that you would like to include in your resume?',
                                    placeholder="Please provide details here...")
        correct_inaccuracies = st.text_area(label='3. Do any parts of the updated resume or cover letter inaccurately represent your professional experience?',
                                    placeholder="Please provide details here...")
        general_suggestions = st.text_area(label='4. What additional suggestions do you have for improving the next version of your resume or cover letter?',
                                    placeholder="Please provide details here...")
        users_feedback = {
            'missing_info': missing_info,
            'new_additions': new_additions,
            'correct_inaccuracies': correct_inaccuracies,
            'general_suggestions': general_suggestions
        }
        
        if st.button('Start Modifying Documents Now'):
            st.write('Processing now....')
            logger.debug('Starting JobFusion2 Crew Agentic Workflow')

            # inputs paths for the modification process
            ori_resume_input = os.path.join("streamlit/", uploaded_resume.name)
            ori_personal_writeup_input = os.path.join("streamlit/", uploaded_personal_writeup.name)
            latest_resume_input = 'output/updated_resume.md'
            jd_qualifications_input = 'output/jd.txt'
            
            # Run the JobFusionCrew2 process
            JobFusionCrew2(ori_resume_input, ori_personal_writeup_input, latest_resume_input, jd_qualifications_input, users_feedback).run()
            logger.debug('Agentic Workflow JobFusionCrew2 finished')

        col1, col2 = st.columns([1, 1])

        # Generate and download revised documents
        if col1.button('1 - Generate Revised Resume'):
            with open('output/latest_resume.md', 'r') as file:
                resume_output = file.read()
            st.download_button('Download Revised Resume', resume_output, file_name='revised_resume.txt', mime='text/plain')

        if col2.button('2 - Generate Revised Cover Letter'):
            with open('output/latest_coverletter.md', 'r') as file:
                cover_letter_output = file.read()
            st.download_button('Download Revised Cover Letter', cover_letter_output, file_name='revised_coverletter.txt', mime='text/plain')
