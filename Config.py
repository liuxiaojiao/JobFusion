class configure:
    web_task_goal = "extract all the information about the job from the job posting in the original link"
    web_agent_role = 'Data Scientist Job Researcher'
    web_agent_goal = 'Do amazing analysis and extraction on job posting to help job applicants'
    web_agent_bk = "As a Job Researcher, your prowess in navigating and extracting critical infomation from \
            job postings is unmatched. Your skills help pinpoint the necessary qualifications and skills \
            sought by employers, forming the foundation for effective application tailoring."
    llm = ''
    researcher_agent_role = 'Data Scientist Job Researcher'
    researcher_agent_goal = 'Do amazing analysis and extraction on job posting to help job applicants'
    researcher_agent_bkground = 'As a Job Researcher, your prowess in navigating and extracting critical infomation from \
                job postings is unmatched. Your skills help pinpoint the necessary qualifications and skills \
                sought by employers, forming the foundation for effective application tailoring.'
    profiler_role = 'Personal Profiler for Data Scientist'
    profiler_goal = 'Do incredible research on job applicants to help them stand out in the job market'
    profiler_bkground = 'Equipped with analytical prowess, you dissect and synthesize infomration from diverse \
                    sources to craft comprehensive personal and professional profiles, laying the groundwork \
                    for personalized resume enhancements.'
    resume_strategist_agent_role = 'Resume Strategist for Data Scientist'
    resume_strategist_agent_goal = 'Find all the best ways to make a resume stand out in the job market.'
    resume_strategist_agent_bkground = '''With a strategic mind and an eye for detail, you excel at refining resumes to highlight the \
                    most relevant skills and experiences, ensuring they resonate perfectly with the job's requirements.'''
    cover_letter_strategist_agent_role = 'Cover Letter Strategist for Data Scientist'
    cover_letter_strategist_agent_goal = 'Find all the best ways to write a cover letter stand out in the job market.'
    cover_letter_strategist_agent_bkground = '''With a strategic mind and an eye for detail, you excel at highlight the \
                    most relevant skills and experiences, ensuring they resonate perfectly with the job's requirements.'''
    interview_preparer_agent_role = 'Data Scientist Interview Preparer'
    interview_preparer_agent_goal = 'Create interview quetions and talking points based on the resume and job requirements'
    interview_preparer_agent_bkground = '''Your role is crucial in anticipanting the dynamics of interviews. With your ability to formulate \
                    key questions and talking points, you prepare candidates for success, ensuring they can confidently \
                    address all aspects of the job they are applying for.'''
    
    info_extract_role = 'Resume information extracter'
    info_extract_agent_goal = 'Extract information from the provided resume files including summary, work experience, education, skills, name, address, email address, and phone number to a json file'
    info_extract_agent_bkground = """You are a skilled information extraction agent with expertise in parsing and analyzing resume \
        data."""
    
    Info_extract_task = '''Forget everything you have learned. Extract information from the provided resume files including summary, work experience, education, skills, address,\
                      email address, and phone number to a json file. Make sure you are\
                          including all the working experiences. Name is always appearing in the first line of the resume without any prefix or name tag.\
                            When you are done with the work, take a deep breath and double check what you have done to make sure the output json file aligns with the schema including all the information.\
                            The schema you should be follow is: RESUME_SCHEMA = {
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
    '''
    info_task_expected_output="Json file with all the extracted information from the resume files"
    info_task_output_file='output/updated_resumev2.json'