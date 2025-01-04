# jobfusion/
# ├── __init__.py
# ├── agents/
# │   ├── __init__.py
# │   ├── resume_agents.py
# │   └── job_agents.py
# ├── tasks/
# │   ├── __init__.py
# │   ├── resume_tasks.py
# │   └── job_tasks.py
# ├── utils/
# │   ├── __init__.py
# │   ├── parsers.py
# │   ├── generators.py
# │   └── scrapers.py
# ├── config/
# │   ├── __init__.py
# │   └── settings.py
# ├── exceptions/
# │   ├── __init__.py
# │   └── custom_exceptions.py
# ├── app.py
# └── requirements.txt


you are a prompt expert, please optimize the prompt in the double quote to optimize your python code "you are an AI expert. you want to create an ai tool using crewai to help modify the user's resume so that the resume are better aligned and would be selected for the interview. First you need to need to extract the incoming resume as the json format, and then you need to scrape the job description to extract key words and identify inportant information, after that you need to make the modifications of the incoming resume based on the key words and inportant information from the job link, finally you need to output a pdf file. I have several code files in the attachment, agents.py lists all the agents we used in the program; taskes.py includes all the tasks for the agent; utils.py includes all the util functions; jobcrew.py includes workable agents combines agents from agents.py and tasks.py; app.py runs the program using streamlit; make an improvement for the code. please add logs and error handlers to the script that makes the code could run into production directly. Also make the change to the code so that they could handles input resumes in different formats. The higher level architecture of the entire file is listed below:

Agent 1:
Agents architectures:
  1. info extractor to json. pdf, txt, and doc
  2. job link info extractor to json
Task architectures:
  1. extract the incoming resume (text, pdf, or docx) to json format
  2. extract key job information including job description, job requirement, job preference, and etc...


Agent 2:
Agents architectures:
  1. modify resume json output to json
  2. review agent
  3. critic agent
  4. cover_letter_strategy
  5. Interview preparation material: A document containing key questions and talking points that the candidate should prepare for the interview.

Task architectures:
  1. modify resume json output to json based on the job information extraction json file
  2. review the modified json output
  3. criticize the modified json output
  4. create a cover letter based on the resume and jd
  5. prepare interview questions based on the resume information

Agent 3:
Agents architectures:
1. Resume Strategist: To create a new version of a resume that effectively aligns with job qualifications and fully incorporates the user’s feedback across multiple areas, ensuring a polished and tailored final document.
2. Document Validation Manager: To review and validate updated resumes, ensuring they fully align with job qualifications and incorporate all user feedback. Your objective is to produce a final error-free resume that is ready for submission.
3. Cover Letter Strategist for Data Scientist: To craft a compelling, targeted cover letter that effectively aligns the candidate’s qualifications with the job requirements, enhancing their chances of securing the position.

Task architectures:
1. Please carefully review the Original Resume and the Latest Resume in light of the user’s feedback. 
2. Review and validate the updated resume from the previous step to ensure it has been fully aligned with the Job Qualifications and incorporates all user feedback including missing information, new additions, inaccuracies and general suggestions. 
3. Using the candidate’s Personal Profile, Job Qualification, and the final modified resume from previous task, craft a compelling cover letter to apply for the position. 


utils: 
pdf converter: convert json to pdf.
RAG optimizer: optimizing RAG architecture.

Output the code in different files in a structural way"









AI Resume Enhancement System Using CrewAI
System Overview
Create an AI-powered resume enhancement system using CrewAI that optimizes resumes for specific job applications. The system should:

Process resumes in multiple formats (PDF, DOCX, TXT)
Analyze job descriptions
Generate tailored resume modifications
Provide supporting materials (cover letter, interview prep)

Technical Requirements

Implement comprehensive logging
Include error handling for production deployment
Support multiple input formats
Follow best practices for code organization
Implement RAG optimization for document processing

Component Architecture
class ResumeParser:
    """
    Handle incoming resumes in various formats (PDF, DOCX, TXT)
    Output standardized JSON format
    Include error handling for corrupt files
    Log parsing steps and outcomes
    """

class JobDescriptionAnalyzer:
    """
    Extract and analyze job postings
    Identify key requirements and qualifications
    Generate structured JSON output
    Handle network errors and invalid URLs
    Log analysis process
    """

Resume Enhancement Pipeline
class ResumeEnhancer:
    """
    Compare resume against job requirements
    Generate targeted modifications
    Maintain original content integrity
    Log enhancement decisions
    """

class QualityAssurance:
    """
    Review modified resumes
    Validate against requirements
    Ensure professional standards
    Log validation results
    """
Document Generation Pipeline
class DocumentGenerator:
    """
    Create final resume versions
    Generate cover letters
    Prepare interview materials
    Log document creation process
    """




Agent 1:
Agents architectures:
  1. info extractor to json. pdf, txt, and doc
  2. job link info extractor to json
Task architectures:
  1. extract the incoming resume (text, pdf, or docx) to json format
  2. extract key job information including job description, job requirement, job preference, and etc...


Agent 2:
Agents architectures:
  1. modify resume json output to json
  2. review agent
  3. critic agent
  4. cover_letter_strategy
  5. Interview preparation material: A document containing key questions and talking points that the candidate should prepare for the interview.

Task architectures:
  1. modify resume json output to json based on the job information extraction json file
  2. review the modified json output
  3. criticize the modified json output
  4. create a cover letter based on the resume and jd
  5. prepare interview questions based on the resume information

Agent 3:
Agents architectures:
1. Resume Strategist: To create a new version of a resume 
2. Document Validation Manager: To review and validate updated resumes。
3. Cover Letter Strategist for Data Scientist: To craft a compelling, targeted cover letter。

Task architectures:
1. Please carefully review the Original Resume and the Latest Resume in light of the user’s feedback. 
2. Review and validate the updated resume from the previous step。
3. Using the candidate’s Personal Profile, Job Qualification, and the final modified resume from previous task。

utils: 
pdf converter: convert json to pdf.
RAG optimizer: optimizing RAG architecture.



Production Considerations

Implement comprehensive logging

Application events
Error tracking
Performance metrics
User actions


Error Handling

Input validation
Process monitoring
Recovery procedures
Error reporting


Performance Optimization

Caching strategies
Resource management
Scalability considerations
Monitoring systems

Take a deep breath and work on this problem step-by-step

version 2:
optimize agents.