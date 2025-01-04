


from dotenv import load_dotenv
from crewai import Crew, Task, Agent, Process
from crewai_tools import ScrapeWebsiteTool
from langchain.chat_models import ChatOpenAI
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
from config import configure as cfg
from mock_interview_chatbot import *
import streamlit as st
import logging
from datetime import datetime

from agents import ResumeAgents, EnhancementAgents
from tasks import ResumeTasks, EnhancementTasks
from .utils import create_pdf_from_json, ResumeCrew, ResumeEnhanceCrew

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f'log/resume_enhancement_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logger.addHandler(file_handler)

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
                ResumeAgents(resume_path, personal_writeup_path, jd_url_input).run()
                
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
            
            resume_file = '/Users/frankwei/Documents/Side_Project/jobfusion_subj/JobFusion/jobfusion_production/inputs/resume_AI.docx'
            job_url = 'https://www.amazon.jobs/en/jobs/2846094/principal-applied-scientist-amazon-prime'
            valid_resume = '/Users/frankwei/Documents/Side_Project/jobfusion_subj/JobFusion/jobfusion_production/output/resume.json'


            resume_file = '/Users/frankwei/Documents/Side_Project/jobfusion_subj/JobFusion/jobfusion_production/output/resume.json'
            job_file = '/Users/frankwei/Documents/Side_Project/jobfusion_subj/JobFusion/jobfusion_production/output/job.json'
            modified_resume_file = '/Users/frankwei/Documents/Side_Project/jobfusion_subj/JobFusion/jobfusion_production/output/enhanced_resume.json'
            reviewed_resume_file = '/Users/frankwei/Documents/Side_Project/jobfusion_subj/JobFusion/jobfusion_production/output/reviewed_resume.json'
            final_resume_file = '/Users/frankwei/Documents/Side_Project/jobfusion_subj/JobFusion/jobfusion_production/output/final_resume.json'

            # Run the JobFusionCrew2 process
            ResumeCrew(openai_api_key, job_url, resume_file,valid_resume).run()
            ResumeEnhanceCrew(openai_api_key, resume_file, job_file, modified_resume_file, reviewed_resume_file, final_resume_file).run()
            # JobFusionCrew2(ori_resume_input, ori_personal_writeup_input, latest_resume_input, jd_qualifications_input, users_feedback).run()
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

    # Tab 3: Career Advice/Mock Interview Chatbot
    with tab3:
        st.subheader('Career Advice Chatbot')
        st.write('You can chat with Career Adviser.')
        chat_container = st.container(height=300)

        # Ensure the necessary documents are uploaded
        if uploaded_resume and uploaded_personal_writeup and jd_url_input:
            logger.debug('Starting Career Advice Chatbot')

            # Load files and prepare vector database for chatbot
            files = file_loading("inputs/contents/")
            docs = doc_load_split(files)
            db = build_vectordb(docs)
            
            # Process user documents for chatbot context
            resume_path = os.path.join("streamlit/", uploaded_resume.name)
            personal_writeup_path = os.path.join("streamlit/", uploaded_personal_writeup.name)
            user_resume = docx2txt.process(resume_path)
            user_personal_writeup = docx2txt.process(personal_writeup_path)
            job_qualifications = []
            with open("output/jd.txt", 'r', encoding='utf-8') as file:
                content = file.read()
                job_qualifications.append(content)
            logger.debug("Resume and personal writeup loaded successfully.")

            # Initialize chat history if not already set
            if 'chat_history' in st.session_state:
                chat_history = st.session_state['chat_history']
            else:
                chat_history = []

            # Store generated responses
            if "messages" not in st.session_state.keys():
                st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

            # Display chat messages
            for message in st.session_state.messages:
                with chat_container.chat_message(message["role"]):
                    st.write(message["content"])
            
            # If vector database is ready, initialize the QA chain
            if db:
                chat_history = st.session_state.get('chat_history', [])
                qa_chain = get_qa_chain(
                    db, k=3, chain_type="stuff", user_resume=user_resume, 
                    user_personal_writeup=user_personal_writeup, job_qualifications=job_qualifications,
                    openai_api_key=openai_api_key, chat_history=chat_history
                )

                # Handle user input in the chat
                if prompt := st.chat_input("How can I help you?"):
                    if prompt is not None:
                        st.session_state.messages.append({'role': 'user', 'content': prompt})
                        with chat_container.chat_message('user'):
                            st.write(f'{prompt}')
                        with chat_container.chat_message('assistant'):
                            message_placeholder = st.empty()
                            full_response = ""
                            bot_response = qa_chain.run({"question": prompt, "chat_history": chat_history})
                            for chunk in re.findall(r'\S+|\n', bot_response):
                                full_response += chunk + " "
                                time.sleep(0.05)
                                message_placeholder.markdown(full_response + "▌")
                            message_placeholder.markdown(full_response)
                            chat_history = update_chat_history(chat_history, prompt, bot_response)

                            # Update chat history in session state
                            st.session_state['chat_history'] = chat_history
                            st.session_state.messages.append({'role': 'assistant', 'content': bot_response})
            else:
                st.error("Failed to build vector database.")
                logger.error("Failed to build vector database.")

            # End chat and collect feedback
            if 'chat_history' in st.session_state and st.button('Finish the Chat'):
                st.write("Thank you for using the Career Advisor chatbot! Have a great day!")
                feedback_text = st.text_area("Please provide feedback on your experience with the chatbot:")
                if st.button("Submit Feedback"):
                    st.write("Feedback submitted. Thank you!")
                    st.stop()

if __name__ == "__main__":
    main()

