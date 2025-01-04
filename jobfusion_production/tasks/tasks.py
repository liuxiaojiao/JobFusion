import streamlit as st
from crewai import Crew
import logging
from crewai_tools import ScrapeWebsiteTool, DOCXSearchTool, SeleniumScrapingTool, MDXSearchTool
from langchain.chat_models import ChatOpenAI
from textwrap import dedent
from config import configure as cfg
from datetime import datetime

from dotenv import load_dotenv
from crewai import Crew, Task, Agent, Process
from crewai_tools import ScrapeWebsiteTool
from langchain.chat_models import ChatOpenAI
import os
from crewai import Task
from typing import Dict, Any
import json

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
llm_35_turbo = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo', temperature=0.7)
manager_llm_35_turbo = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo')
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(f'log/resume_enhancement_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logger.addHandler(file_handler)

class ResumeTasks:
    @staticmethod
    def create_extraction_task(agent, resume_file: str) -> Task:
        try:
            return Task(
                description=cfg.resume_Info_extract_task,
                agent=agent,
                expected_output=cfg.resume_info_task_expected_output,
                output_format="JSON",
                output_file='output/resume.json',
            )
        except Exception as e:
            logger.error(f"Error creating extraction task: {str(e)}")
            raise

    @staticmethod
    def extraction_valid_task(agent, resume_file: str, valid_resume:str) -> Task:
        try:
            return Task(
                description=f'valid extracted information from {valid_resume} and compare to {resume_file}',
                agent=agent,
                expected_output='A new JSON file',
                output_format="JSON",
                output_file='output/valid_resume.json',
            )
        except Exception as e:
            logger.error(f"Error creating extraction task: {str(e)}")
            raise

    @staticmethod
    def create_job_analysis_task(agent, job_url: str) -> Task:
        try:
            return Task(
                description=f"Analyze job posting from URL: {job_url}",
                agent=agent,
                expected_output="JSON formatted job requirements",
                output_format="JSON",
                output_file='output/job.json',
            )
        except Exception as e:
            logger.error(f"Error creating job analysis task: {str(e)}")
            raise



class EnhancementTasks:
    @staticmethod
    def create_modification_task(agent, resume_json: Dict, job_json: Dict) -> Task:
        try:
            logger.info("Creating resume modification task")
            return Task(
                description='''Analyze job requirements and modify resume to include relevant 
                              keywords, responsibilities, and skills while maintaining authenticity''',
                agent=agent,
                # context={
                #     "resume_data": resume_json,
                #     "job_data": job_json
                # },
                expected_output="Enhanced JSON resume with incorporated keywords and skills",
                output_format="json",
                output_file='output/enhanced_resume.json'
            )
        except Exception as e:
            logger.error(f"Error creating modification task: {str(e)}")
            raise

    @staticmethod
    def create_review_task(agent, modified_resume: Dict) -> Task:
        try:
            logger.info("Creating resume review task")
            return Task(
                description='''Review modified resume for accuracy, relevance, and authenticity. 
                              Suggest and implement necessary improvements''',
                agent=agent,
                # context={"modified_resume": modified_resume},
                expected_output="Reviewed and validated JSON resume",
                output_format="json",
                output_file='output/reviewed_resume.json'
            )
        except Exception as e:
            logger.error(f"Error creating review task: {str(e)}")
            raise

    @staticmethod
    def create_critique_task(agent, reviewed_resume: Dict) -> Task:
        try:
            logger.info("Creating resume critique task")
            return Task(
                description='''Critically analyze the resume for potential improvements 
                              and optimization opportunities''',
                agent=agent,
                # context={"reviewed_resume": reviewed_resume},
                expected_output="Critiqued and optimized JSON resume with improvement suggestions",
                output_format="json",
                output_file='output/final_update_resume.json'
            )
        except Exception as e:
            logger.error(f"Error creating critique task: {str(e)}")
            raise

    @staticmethod
    def create_cover_letter_task(agent, final_resume: Dict, job_json: Dict) -> Task:
        try:
            logger.info("Creating cover letter task")
            return Task(
                description='''Create a compelling 4-paragraph cover letter that highlights relevant 
                              experience and matches job requirements. Maintain authenticity while 
                              emphasizing candidate strengths''',
                agent=agent,
                # context={
                #     "final_resume": final_resume,
                #     "job_requirements": job_json
                # },
                expected_output="Professional cover letter in markdown format",
                output_format="markdown",
                output_file='output/cover_letter.md'
            )
        except Exception as e:
            logger.error(f"Error creating cover letter task: {str(e)}")
            raise

    @staticmethod
    def create_interview_prep_task(agent, final_resume: Dict, job_json: Dict) -> Task:
        try:
            logger.info("Creating interview preparation task")
            return Task(
                description='''Generate relevant interview questions and talking points based on 
                              resume and job requirements. Focus on highlighting key experiences 
                              and qualifications''',
                agent=agent,
                # context={
                #     "final_resume": final_resume,
                #     "job_requirements": job_json
                # },
                expected_output="Interview preparation guide with questions and talking points",
                output_format="markdown",
                output_file='output/interview_prep.md'
            )
        except Exception as e:
            logger.error(f"Error creating interview prep task: {str(e)}")
            raise

def save_outputs(results: Dict[str, Any], filename: str = "enhancement_outputs.json"):
    try:
        logger.info(f"Saving outputs to {filename}")
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving outputs: {str(e)}")
        raise