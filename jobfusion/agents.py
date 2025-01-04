from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from config import configure as conf
from crewai import Crew, Task, Agent, Process
# from tavily import TavilyClient

# from tools.browser_tools import BrowserTools
from crewai_tools import ScrapeWebsiteTool, DOCXSearchTool, SeleniumScrapingTool, MDXSearchTool
import docx2txt
import streamlit as st
# os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"] 

# openai_api_key = st.secrets["OPENAI_API_KEY"]

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

llm_35_turbo = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo')

class JobFusion_Agents():
    def __init__(self, resume_input, jd_url_input):
        self.resume_input = resume_input
        self.jd_url = jd_url_input

    def researcher(self):
        return Agent(
            role='Data Scientist Job Researcher',
            goal='Do amazing analysis and extraction on job posting to help job applicants',
            backstory=('As a Job Researcher, your prowess in navigating and extracting critical infomation from \
                job postings is unmatched. Your skills help pinpoint the necessary qualifications and skills \
                sought by employers, forming the foundation for effective application tailoring.'),
            llm=llm_35_turbo,
            tools=[ScrapeWebsiteTool(website_url=self.jd_url)],
            allow_delegation=False,
            verbose=True,
            max_iter=5)

    def profiler(self):
        return Agent(
                role='Personal Profiler for Data Scientist',
                goal='Do incredible research on job applicants to help them stand out in the job market',
                backstory=('Equipped with analytical prowess, you dissect and synthesize infomration from diverse \
                    sources to craft comprehensive personal and professional profiles, laying the groundwork \
                    for personalized resume enhancements.'),
                llm=llm_35_turbo,
                tools=[DOCXSearchTool(docx=self.resume_input)],
                allow_delegation=False,
                verbose=True,
                max_iter=5)

    def resume_strategist(self):
        return Agent(
                role='Resume Strategist for Data Scientist',
                goal='Find all the best ways to make a resume stand out in the job market.',
                backstory=('''With a strategic mind and an eye for detail, you excel at refining resumes to highlight the \
                    most relevant skills and experiences, ensuring they resonate perfectly with the job's requirements.'''),
                llm=llm_35_turbo,
                tools=[DOCXSearchTool(docx=self.resume_input)],
                allow_delegation=False,
                verbose=True,
                max_iter=5)
    
    def cover_letter_strategist(self):
        return Agent(
                role='Cover Letter Strategist for Data Scientist',
                goal='Find all the best ways to write a cover letter stand out in the job market.',
                backstory=('''With a strategic mind and an eye for detail, you excel at highlight the \
                    most relevant skills and experiences, ensuring they resonate perfectly with the job's requirements.'''),
                llm=llm_35_turbo,
                tools=[DOCXSearchTool(docx=self.resume_input)],
                allow_delegation=False,
                verbose=True,
                max_iter=5)
    
    def interview_preparer(self):
        return Agent(
                role='Data Scientist Interview Preparer',
                goal='Create interview quetions and talking points based on the resume and job requirements',
                backstory=("""Your role is crucial in anticipanting the dynamics of interviews. With your ability to formulate \
                    key questions and talking points, you prepare candidates for success, ensuring they can confidently \
                    address all aspects of the job they are applying for."""),
                llm=llm_35_turbo,
                allow_delegation=False,
                verbose=True,
                max_iter=5)

class JobFusion2_Agents():
    def __init__(self, ori_resume_input, ori_personal_writeup_input, latest_resume_input):
        self.original_resume_input = ori_resume_input
        self.original_personal_writeup_input = ori_personal_writeup_input
        self.latest_resume_input = latest_resume_input

    def resume_strategist(self):
        return Agent(
                role='Resume Strategist for Data Scientist',
                goal='To create a new version of a resume that effectively aligns with job qualifications and fully incorporates the user’s feedback across multiple areas, ensuring a polished and tailored final document.',
                backstory=('''You are a seasoned resume strategist with years of experience in transforming resumes into compelling narratives that reflect the true potential of candidates. \
                           Your expertise lies in not only highlighting the strengths and achievements of an individual but also in carefully revising resumes to incorporate detailed feedback from users. \
                           Whether it's adding new information, correcting errors, or adjusting the style and format, you ensure that the final resume fully aligns with both the job qualifications and the user’s preferences..'''),
                llm=llm_35_turbo,
                tools=[DOCXSearchTool()],
                allow_delegation=False,
                verbose=True,
                max_iter=5)
    
    def document_validation_manager(self):
        return Agent(
                role='Document Validation Manager',
                goal='To review and validate updated resumes, ensuring they fully align with job qualifications and incorporate all user feedback. Your objective is to produce a final error-free resume that is ready for submission.',
                backstory=('''You are a seasoned document validation expert with a sharp eye for detail and precision. Your expertise ensures that resumes are error-free, fully incorporate user feedback, \
                           and align with strategic goals. You understand the crucial role a resume plays in the job search process and are committed to delivering flawless, submission-ready documents.'''),
                manager_llm=manager_llm_35_turbo,
                allow_delegation=True,  # Enabling delegation
                agents=[self.resume_strategist, self.cover_letter_strategist],  # Subordinate agents
                verbose=True,
                max_iter=5)
    
    def cover_letter_strategist(self):
        return Agent(
                role='Cover Letter Strategist for Data Scientist',
                goal='To craft a compelling, targeted cover letter that effectively aligns the candidate’s qualifications with the job requirements, enhancing their chances of securing the position.',
                backstory=('''You are a skilled cover letter strategist who crafts persuasive narratives that resonate with hiring managers. \
                           You excel at transforming a candidate’s resume and profile into a compelling argument, \
                           clearly demonstrating their strengths and fit for the job. Your talent lies in making candidates stand out as the ideal choice for the position.'''),
                llm=llm_35_turbo,
                tools=[DOCXSearchTool(docx=self.original_personal_writeup_input)],
                allow_delegation=False,
                verbose=True,
                max_iter=5)
    


def create_resume_review_agent(resume_output_md_path, llm_35_turbo, manager_llm_35_turbo,resume_json_path):

    Info_extract_agent = Agent(
        role='Resume information extracter',
        goal='Extract information from the provided resume files including summary, work experience, education, skills, name, address, email address, and phone number to a json file',
        backstory="""You are a skilled information extraction agent with expertise in parsing and analyzing resume data.""",
        verbose=True,
        allow_delegation=False,
        tools=[MDXSearchTool(mdx=resume_output_md_path)],
        llm=llm_35_turbo,
        )
    Info_extract_task = Task(
                description= '''Forget everything you have learned. Extract information from the provided resume files including summary, work experience, education, skills, address,\
                      email address, and phone number to a json file. Make sure you are\
                          including all the working experiences. Name is always appearing in the first line of the resume without any prefix or name tag.\
                            When you are done with the work, take a deep breath and double check what you have done to make sure the output json file aligns with the schema including all the information.\
                            The schema you should be follow is: 
    RESUME_SCHEMA = {
    "personal_info": {
        "name": str,
        "title": str,
        "summary": str,
        "contact": {
            "email": str,
            "phone": str,
            "location": str,
            "linkedin": str
        }
    },
    "work_experience": [{
        "company": str,
        "position": str,
        "duration": str,
        "location": str,
        "achievements": [str]
    }],
    "education": [{
        "school": str,
        "degree": str,
        "duration": str,
        "location": str
    }],
    "skills": [str]
    }
    When you are done with the work, go back to the md file again and check if you have missed anything. If you have missed anything, go back to the resume files and extract the missing information.\
        ''',
                agent=Info_extract_agent,
                expected_output="Json file with all the extracted information from the resume files",
                output_file=resume_json_path)
    resume_review_crew = Crew(
            agents=[Info_extract_agent],
            tasks=[Info_extract_task],
            process=Process.sequential,
            manager_llm = manager_llm_35_turbo, # Assign the manager_llm to the Crew
            verbose=True
    )
    return resume_review_crew