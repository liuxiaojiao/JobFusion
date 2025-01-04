


import streamlit as st
from crewai import Crew
import logging
from crewai_tools import ScrapeWebsiteTool, DOCXSearchTool, SeleniumScrapingTool, MDXSearchTool, JSONSearchTool
from langchain.chat_models import ChatOpenAI
from textwrap import dedent
from config import configure as cfg
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew, Task, Agent, Process
from crewai_tools import ScrapeWebsiteTool
from langchain.chat_models import ChatOpenAI
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
llm_35_turbo = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo', temperature=0.7)
manager_llm_35_turbo = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo')

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f'log/resume_enhancement_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logger.addHandler(file_handler)

class ResumeAgents:
    def __init__(self, openai_api_key, jd_url, resume_input, valid_resume):
        self.llm = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo', temperature=0.7)
        # self.llm = ChatOpenAI(api_key=openai_api_key, model='gpt-4o-mini', temperature=0.7)
        self.jd_url = jd_url
        self.resume_input = resume_input
        self.valid_resume = valid_resume
        logger.info("Initializing ResumeAgents")

    def create_info_extractor(self) -> Agent:
        try:
            return Agent(
                role=cfg.resume_info_extract_role,
                goal=cfg.resume_info_extract_agent_goal,
                backstory=cfg.resume_info_extract_agent_bkground,
                llm=self.llm,
                verbose=True,
                tools=[DOCXSearchTool(docx=self.resume_input)],
            )
        except Exception as e:
            logger.error(f"Error creating info extractor agent: {str(e)}")
            raise

    def resume_info_reviewer(self) -> Agent:
        try:
            return Agent(
                role='Information Extract Reviewer',
                goal='Review and validate extracted information from resume to make sure everything is correct, and make the correction if needed',
                backstory='Expert in reviewing and validating information extracted from resumes',
                llm=self.llm,
                verbose=True,
                tools=[DOCXSearchTool(docx=self.resume_input), JSONSearchTool(json_path=self.valid_resume)],
            )
        except Exception as e:
            logger.error(f"Error creating info extractor agent: {str(e)}")
            raise   

    def create_job_analyzer(self) -> Agent:
        try:
            return Agent(
                role='Job Description Analyzer',
                goal='Extract key requirements and qualifications from job postings',
                backstory='Specialist in analyzing job descriptions and identifying key requirements',
                llm=self.llm,
                verbose=True,
                tools=[ScrapeWebsiteTool(website_url=self.jd_url)]
            )
        except Exception as e:
            logger.error(f"Error creating job analyzer agent: {str(e)}")
            raise
    # def create_resume_optimizer(self) -> Agent:
    #     try:
    #         return Agent(
    #             role='Resume Optimizer',
    #             goal='Enhance resume content based on job requirements',
    #             backstory='Expert at aligning resumes with job requirements',
    #             llm=self.llm,
    #             verbose=True,
    #             # tools=['content_optimizer', 'keyword_matcher']
    #         )
    #     except Exception as e:
    #         logger.error(f"Error creating resume optimizer agent: {str(e)}")
    #         raise

class EnhancementAgents:
    def __init__(self, openai_api_key, resume_input, jd_input):
        self.llm = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo', temperature=0.7)
        self.jd_input = jd_input
        self.resume_input = resume_input
        logger.info("Initializing Enhancement Agents")

    def create_resume_modifier(self) -> Agent:
        try:
            return Agent(
                role='Resume Modifier',
                goal=f'''Enhance resume content with missing keywords and skills from job description. Keep the schema of the JSON file:
    {cfg.RESUME_SCHEMA}
                  only change the last layer for each section.''',
                backstory='''Expert at analyzing job requirements and modifying resumes to highlight 
                            relevant experience while maintaining authenticity''',
                llm=self.llm,
                tools=[JSONSearchTool(json_path=self.resume_input), JSONSearchTool(json_path=self.jd_input)],
                verbose=True
            )
        except Exception as e:
            logger.error(f"Error creating resume modifier agent: {str(e)}")
            raise

    def create_review_agent(self) -> Agent:
        try:
            return Agent(
                role='Resume Reviewer',
                goal=f'''Review and validate resume modifications for accuracy and relevance from create_resume_modifier. Keep the schema of the JSON file:\
    {cfg.RESUME_SCHEMA}
                  only change the last layer for each section.''',
                backstory='''Experienced resume reviewer with expertise in ensuring 
                            modifications maintain authenticity while maximizing impact''',
                llm=self.llm,
                # tools=['content_validator', 'consistency_checker'],
                verbose=True
            )
        except Exception as e:
            logger.error(f"Error creating review agent: {str(e)}")
            raise

    def create_critic_agent(self) -> Agent:
        try:
            return Agent(
                role='Resume Critic',
                goal=f'''Critically analyze resume for improvements and optimization opportunities. Keep the schema of the JSON file:\
    {cfg.RESUME_SCHEMA}
                  only change the last layer for each section.''',
                backstory='''Critical thinking expert specializing in identifying areas 
                            for resume enhancement and optimization''',
                llm=self.llm,
                # tools=['content_analyzer', 'improvement_suggester'],
                verbose=True
            )
        except Exception as e:
            logger.error(f"Error creating critic agent: {str(e)}")
            raise

    def create_cover_letter_strategist(self) -> Agent:
        try:
            return Agent(
                role='Cover Letter Strategist',
                goal='Create compelling, tailored cover letters that highlight relevant experience',
                backstory='''Professional writer specialized in crafting engaging cover letters 
                            that effectively communicate candidate qualifications''',
                llm=self.llm,
                # tools=['content_generator', 'tone_analyzer'],
                verbose=True
            )
        except Exception as e:
            logger.error(f"Error creating cover letter strategist: {str(e)}")
            raise

    def create_interview_prep_agent(self) -> Agent:
        try:
            return Agent(
                role='Interview Preparation Specialist',
                goal='Prepare comprehensive interview materials and talking points',
                backstory='''Interview preparation expert skilled at creating targeted questions 
                            and effective talking points''',
                llm=self.llm,
                # tools=['question_generator', 'talking_points_creator'],
                verbose=True
            )
        except Exception as e:
            logger.error(f"Error creating interview prep agent: {str(e)}")
            raise