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

# JobFusionCrew class to create an updated version of the resume and cover letter
class JobFusionCrew:
    def __init__(self, resume_input, personal_writeup_input, jd_url_input):
        self.resume_input = resume_input
        self.personal_writeup_input = personal_writeup_input  
        self.jd_url = jd_url_input 

    def run(self):
        # Initialize agents and tasks
        agents = JobFusion_Agents(self.resume_input, self.jd_url)
        tasks = JobFusion_Tasks(self.resume_input, self.personal_writeup_input, self.jd_url)

        crew = Crew(
            agents=[
                agents.researcher(), 
                agents.profiler(), 
                agents.resume_strategist(),
                agents.cover_letter_strategist(),
                agents.interview_preparer()
            ],
            tasks=[
                tasks.research_task(agents.researcher()),
                tasks.profile_task(agents.profiler()),
                tasks.resume_strategy_task(agents.resume_strategist()),
                tasks.cover_letter_strategy_task(agents.cover_letter_strategist()),
                tasks.interview_preparation_task(agents.interview_preparer())
            ],
            verbose=True
        )

        # Kickoff the process and return results
        results = crew.kickoff()
        return results

# JobFusionCrew 2 Class to modify the resume and cover letter based on users feedback
class JobFusionCrew2:
    def __init__(self, ori_resume_input, ori_personal_writeup_input, latest_resume_input, jd_qualifications_input, users_feedback):
        self.original_resume_input = ori_resume_input
        self.original_personal_writeup_input = ori_personal_writeup_input
        self.latest_resume_input = latest_resume_input
        self.jd_qualifications_input = jd_qualifications_input
        self.users_feedback = users_feedback

    def run(self):
        agents = JobFusion2_Agents(self.original_resume_input, self.original_personal_writeup_input, self.latest_resume_input)
        tasks = JobFusion2_Tasks(self.original_resume_input, self.original_personal_writeup_input, self.jd_qualifications_input, self.latest_resume_input, self.users_feedback)

        # Define the crew and hierarchical process
        crew = Crew(
            agents=[
                agents.resume_strategist(),
                agents.cover_letter_strategist(),
                agents.document_validation_manager()
            ],
            tasks=[
                tasks.resume_strategy_task(agents.resume_strategist()),
                tasks.cover_letter_strategy_task(agents.cover_letter_strategist()),
                tasks.document_validation_task(agents.document_validation_manager())
            ],
            process = Process.hierarchical, # Hierarchical process to manage delegation
            manager_llm = manager_llm_35_turbo,  # Assign the manager_llm to the Crew
            verbose=True
        )

        # Kickoff the process and return results
        results = crew.kickoff()
        return results