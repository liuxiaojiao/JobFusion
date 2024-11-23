import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListItem, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
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

import os
import requests
from crewai import Agent, Task, Crew, Process
from langchain.llms import OpenAI
import markdown
import PyPDF2
from fpdf import FPDF

from crewai_tools import MDXSearchTool, PDFSearchTool

from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
llm_35_turbo = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo', temperature=0.7)
manager_llm_35_turbo = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo')

# Define standard resume format schema
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

def validate_resume_format(data):
    """Validate if the input data matches the schema"""
    try:
        for key, value_type in RESUME_SCHEMA.items():
            if key not in data:
                raise ValueError(f"Missing required section: {key}")
            
            if isinstance(value_type, list):
                if not isinstance(data[key], list):
                    raise ValueError(f"{key} must be a list")
                
                for item in data[key]:
                    for subkey, subtype in value_type[0].items():
                        if subkey not in item:
                            raise ValueError(f"Missing required field {subkey} in {key}")
                        if not isinstance(item[subkey], subtype):
                            raise ValueError(f"Invalid type for {subkey} in {key}")
            
            elif isinstance(value_type, dict):
                for subkey, subtype in value_type.items():
                    if subkey not in data[key]:
                        raise ValueError(f"Missing required field {subkey} in {key}")
                    if not isinstance(data[key][subkey], subtype):
                        raise ValueError(f"Invalid type for {subkey} in {key}")
        
        return True
    except Exception as e:
        print(f"Validation error: {str(e)}")
        return False
    

def create_pdf_from_json(json_data, output_filename):
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    story = []
    
    styles.add(ParagraphStyle(name='Name',
                            fontSize=24,
                            spaceAfter=12))  # Increased space after name
    styles.add(ParagraphStyle(name='Contact',
                            fontSize=12,
                            spaceAfter=20))
    styles.add(ParagraphStyle(name='Section',
                            fontSize=16,
                            spaceBefore=20,
                            spaceAfter=12))
    
    # Personal Info
    if isinstance(json_data.get("personal_info"), dict):
        person = json_data["personal_info"]
        story.append(Paragraph(person.get("name", "No Name Provided"), styles["Name"]))
        
        if isinstance(person.get("contact"), dict):
            contact = person["contact"]
            contact_items = []
            if contact.get('email'): contact_items.append(contact['email'])
            if contact.get('phone'): contact_items.append(contact['phone'])
            if contact.get('location'): contact_items.append(contact['location'])
            if contact.get('linkedin'): contact_items.append(contact['linkedin'])
            
            contact_text = " | ".join(contact_items) if contact_items else "No Contact Information Provided"
            story.append(Paragraph(contact_text, styles["Contact"]))
        
        # story.append(Paragraph(person.get("title", "No Title Provided"), styles["Heading2"]))
        story.append(Paragraph('Summary', styles["Heading2"]))
        story.append(Paragraph(person.get("summary", "No Summary Provided"), styles["Normal"]))
    
    story.append(Spacer(1, 20))
    
    # Work Experience
    story.append(Paragraph("Work Experience", styles["Section"]))
    if isinstance(json_data.get("work_experience"), list) and json_data["work_experience"]:
        for job in json_data["work_experience"]:
            job_title = []
            if job.get('position'): job_title.append(f"<b>{job['position']}</b>")
            if job.get('company'): job_title.append(job['company'])
            job_title_text = " - ".join(job_title) if job_title else "Position Details Not Available"
            story.append(Paragraph(job_title_text, styles["Normal"]))
            
            location_info = []
            if job.get('duration'): location_info.append(job['duration'])
            if job.get('location'): location_info.append(job['location'])
            location_text = " | ".join(location_info) if location_info else "Location/Duration Not Available"
            story.append(Paragraph(location_text, styles["Normal"]))
            
            if isinstance(job.get("achievements"), list) and job["achievements"]:
                achievements = [ListItem(Paragraph(item, styles["Normal"])) 
                              for item in job["achievements"] if item]
                if achievements:
                    story.append(ListFlowable(achievements, bulletType='bullet'))
            story.append(Spacer(1, 12))
    else:
        story.append(Paragraph("No work experience provided", styles["Normal"]))
    
    # Education with reordered fields
    story.append(Paragraph("Education", styles["Section"]))
    if isinstance(json_data.get("education"), list) and json_data["education"]:
        for edu in json_data["education"]:
            # First line: Degree
            if edu.get('degree'):
                story.append(Paragraph(f"<b>{edu['degree']}</b>", styles["Normal"]))
            
            # Second line: Duration, School, Location
            edu_details = []
            if edu.get('duration'): edu_details.append(edu['duration'])
            if edu.get('school'): edu_details.append(edu['school'])
            if edu.get('location'): edu_details.append(edu['location'])
            
            details_text = " | ".join(edu_details) if edu_details else "Education Details Not Available"
            story.append(Paragraph(details_text, styles["Normal"]))
            story.append(Spacer(1, 8))
    else:
        story.append(Paragraph("No education information provided", styles["Normal"]))
    
    # Skills
    story.append(Paragraph("Skills", styles["Section"]))
    if isinstance(json_data.get("skills"), list) and json_data["skills"]:
        skills = [skill for skill in json_data["skills"] if skill]
        skills_text = "; ".join(skills) if skills else "No specific skills listed"
        story.append(Paragraph(skills_text, styles["Normal"]))
    else:
        story.append(Paragraph("No skills provided", styles["Normal"]))
    
    doc.build(story)

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

if __name__  == "__main__":
    # if __name__ == "main":
    resume_output_md_path = 'output/updated_resume.md'
    resume_json_path = 'output/updated_resumev7.json'
    create_resume_review_agent(resume_output_md_path, llm_35_turbo,manager_llm_35_turbo,resume_json_path).kickoff()
    with open(resume_json_path, 'r') as f:
        resume_json = f.read()
    create_pdf_from_json(resume_json, output_filename="output/resume_v7.pdf")