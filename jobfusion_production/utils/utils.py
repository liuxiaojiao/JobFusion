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
from dotenv import load_dotenv
from config import configure as cfg

import os
import requests
from crewai import Agent, Task, Crew, Process
from langchain.llms import OpenAI
import markdown
import PyPDF2
from fpdf import FPDF

from agents import ResumeAgents, EnhancementAgents
from tasks import ResumeTasks, EnhancementTasks


from dotenv import load_dotenv
from crewai import Crew, Task, Agent, Process
from crewai_tools import ScrapeWebsiteTool
from langchain.chat_models import ChatOpenAI

def create_pdf_from_json(json_data, output_filename):
    '''
    TO DO: 
    1. Adding different format corresponding to different input resumes
    2. 
    '''
    if isinstance(json_data, str):
        with open(json_data, 'r') as file:
            json_data = json.load(file)

    # if isinstance(json_data, str):
    #     json_data = json.loads(json_data)
    
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



class ResumeCrew():
    def __init__(self,openai_api_key, job_url, resume_file,valid_resume):
        self.openai_api_key = openai_api_key
        self.job_url = job_url
        self.resume_file = resume_file
        self.valid_resume = valid_resume
    def run(self):
        resume_agents = ResumeAgents(self.openai_api_key, self.job_url, self.resume_file, self.valid_resume)
        crew = Crew(
            agents=[
                resume_agents.create_info_extractor(),
                resume_agents.resume_info_reviewer(),
                resume_agents.create_job_analyzer(),
                # resume_agents.create_resume_optimizer()
            ],
            tasks=[
                ResumeTasks.create_extraction_task(resume_agents.create_info_extractor(), self.resume_file),
                ResumeTasks.extraction_valid_task(resume_agents.resume_info_reviewer(), self.resume_file, self.valid_resume),
                ResumeTasks.create_job_analysis_task(resume_agents.create_job_analyzer(), self.job_url)
            ],
            verbose=True
        )
        # Execute tasks
        result = crew.kickoff()
        return result
    

class ResumeEnhanceCrew():
    def __init__(self, openai_api_key, resume_file, job_file, modified_resume_file, reviewed_resume_file, final_resume_file):
        self.openai_api_key = openai_api_key
        self.resume_file = resume_file
        self.job_file = job_file
        self.modified_resume_file = modified_resume_file
        self.reviewed_resume_file = reviewed_resume_file
        self.final_resume_file = final_resume_file

    def run(self):
        resume_agents = EnhancementAgents(self.openai_api_key, self.resume_file, self.job_file)
                        # Create crew
        crew = Crew(
            agents=[
                resume_agents.create_resume_modifier(),
                resume_agents.create_review_agent(),
                resume_agents.create_critic_agent(),
                resume_agents.create_cover_letter_strategist(),
                resume_agents.create_interview_prep_agent()
            ],
            tasks=[
                EnhancementTasks.create_modification_task(resume_agents.create_resume_modifier(), resume_file, job_file),
                EnhancementTasks.create_review_task(resume_agents.create_review_agent(), modified_resume_file),
                EnhancementTasks.create_critique_task(resume_agents.create_critic_agent(), reviewed_resume_file),
                EnhancementTasks.create_cover_letter_task(resume_agents.create_cover_letter_strategist(), final_resume_file, job_file),
                EnhancementTasks.create_interview_prep_task(resume_agents.create_interview_prep_agent(), final_resume_file, job_file)
            ],
            verbose=True
        )

        # Execute tasks
        result = crew.kickoff()
        return result