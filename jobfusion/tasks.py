from textwrap import dedent
from datetime import date
import docx2txt
from crewai import Agent, Task, Crew, Process
from mock_interview_chatbot import read_txt_files

class JobFusion_Tasks():
    def __init__(self, resume_input, personal_writeup_input, jd_url_input):
        # self.personal_writeup = textract.process(personal_writeup_input)
        # self.resume = textract.process(resume_input)
        self.jd_url = jd_url_input 
        self.personal_writeup = docx2txt.process(personal_writeup_input)
        self.resume = docx2txt.process(resume_input)

    def research_task(self, agent):
        return Task(description=dedent(f'''
            Analyze the provided job description to extract key skills, experiences and qualifications required, based on 
            the following given job descriptions URL.
            {self.__tip_section()}

            Job description URL: {self.jd_url}
            '''),
            expected_output=("A structured list of job requirements, including necessay skills, qualifications and experiences."),
            output_file='output/jd.txt',
            agent=agent)
  
    def profile_task(self, agent):
        return Task(description=dedent(f'''
            Compile a detailed personal and professional profile by combining the personal write-up and resume below. 
            Utilize tools to extract and synthesize information from these sources on personal education, previous profressional experiences and skills.
            {self.__tip_section()}

            Personal writeup: {self.personal_writeup}
            Resume: {self.resume}
            '''),
            expected_output=("A comprehensive profile document that includes skills, project experiences, contributions, \
                                and capabilities to solve business problems."),
            agent=agent)

    def resume_strategy_task(self, agent):
        return Task(description=dedent(f'''
            Using the profile and job requirements obtained from previous tasks, tailor the resume to highlight the most relevant areas. 
            Employ tools to adjust and enhance the resume content. Make sure this is the best resume even but 
            don't make up any information. Update the work experience, skills and education. All to better reflect the 
            candidates abilities and how it matches the job posting.
            {self.__tip_section()}
            '''),
            expected_output=("An updated resume that effectively highlights the candidate's qualifications and experiences relevant to the job."),
            output_file='output/updated_resume.md',
            agent=agent) 
    
    def cover_letter_strategy_task(self, agent):
        return Task(description=dedent(f'''
            Using the profile, job requirements obtained from previous tasks, and the udpated resume to write a cover letter to apply the position within 4 paragraphs. 
            Make sure to emphasize the candidate's strengths but don't make up any information, and reflect the candidates abilities and how it matches the job posting.
            {self.__tip_section()}
            '''),
            expected_output=("A cover letter that effectively highlights the candidate's qualifications and experiences relevant to the job."),
            output_file='output/coverletter.md',
            agent=agent) 
  
    def interview_preparation_task(self, agent):
        return Task(description=dedent(f'''
            Create a set of potential interview questions and talking points based on the latest updated resume and job requirements. 
            Utilize tools to generate relevant questions and discussion points. Make sure to use these question and talking points to help 
            the candidate highlight the main points of the resume and how it matches the job posting. 
            {self.__tip_section()}
            '''),
            expected_output=("A document containing key questions and talking points that the candidate should prepare for the interview."),
            output_file='output/interview_preparation_materials.txt',
            agent=agent) 

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"



class JobFusion2_Tasks():
    def __init__(self, ori_resume_input, ori_personal_writeup_input, jd_qualifications_input, latest_resume_input, users_feedback):
        self.original_resume = docx2txt.process(ori_resume_input)
        self.original_personal_writeup = docx2txt.process(ori_personal_writeup_input)
        self.jd_qualifications = read_txt_files(jd_qualifications_input)
        self.latest_resume = read_txt_files(latest_resume_input)
        self.users_feedback = users_feedback

    def resume_strategy_task(self, agent):
        return Task(description=dedent(f'''
            Please carefully review the Original Resume and the Latest Resume in light of the user’s feedback. 
            Your goal is to create a new version of the resume that both aligns with the Job Qualifications and incorporates the user’s input across the following four areas:
            1. Missing Information: Identify and include any information that was overlooked in previous resume modifications. Ensure that this information is accurately represented in the new version.
            2. New Additions: Incorporate the new achievements, skills, or experiences that the user has provided. These should be seamlessly integrated into the resume to enhance the overall presentation.
            3. Correct Inaccuracies: Address any inaccuracies or errors identified by the user in the updated resumes. Cross-check with the original resume to ensure that all details in the new version are correct and accurately reflect the user’s professional background.
            4. General Suggestions: Reflect the user’s general suggestions for improvement in the new version of the resume. Adjust the format, style, or content as needed to better align with the user’s preferences.
            Create a final version of the resume that is tailored to the job qualifications while fully incorporating the user’s feedback.                         
            {self.__tip_section()}

            Job Qualifications: {self.jd_qualifications}
            Original Resume: {self.original_resume}
            Latest Resume: {self.latest_resume}
            Missing Information: {self.users_feedback['missing_info']}
            New Additions: {self.users_feedback['new_additions']}
            Correct Inaccuracies: {self.users_feedback['correct_inaccuracies']}
            General Suggestions: {self.users_feedback['general_suggestions']}
            '''),
            expected_output=("An updated resume that effectively highlights the candidate's qualifications to the job qualifications while fully incorporating the user’s feedback."),
            output_file='output/latest_resume.md',
            agent=agent) 
    
    def document_validation_task(self, agent):
        return Task(description=dedent(f'''
            Review and validate the updated resume from the previous step to ensure it has been fully aligned with the Job Qualifications and incorporates all user feedback including missing information, new additions, inaccuracies and general suggestions. Your task includes:

            1. Verification: Carefully cross-check the updated resume against the Original Resume, job qualifications, and the feedback provided by the user. Ensure that all qualifications, skills, and experiences required for the job have been accurately reflected in the resume.
            2. Alignment with Feedback: Confirm that the user's feedback regarding missing information, new additions, corrections, and general suggestions have been thoroughly addressed and incorporated into the updated resume.
            3. Error Detection: Identify any discrepancies or potential errors that may have been overlooked or incorrectly implemented during the resume updating process. These include inaccuracies, missing details, or elements that do not align with the overall resume strategy.
            4. Revision and Finalization: If any issues are found, make the necessary corrections to ensure that the resume not only meets the job qualifications but also fully aligns with the user's feedback and the overall strategy. Generate the latest, most accurate version of the resume.

            {self.__tip_section()}

            Job Qualifications: {self.jd_qualifications}
            Missing Information: {self.users_feedback['missing_info']}
            New Additions: {self.users_feedback['new_additions']}
            Correct Inaccuracies: {self.users_feedback['correct_inaccuracies']}
            General Suggestions: {self.users_feedback['general_suggestions']}       
            '''),
            expected_output=("An final error-free, fully revised resume that aligns with both the job qualifications and the user’s feedback, ready for submission."),
            tasks=[self.resume_strategy_task, self.cover_letter_strategy_task],  # Subordinate tasks
            process=Process.sequential, # Ensures the resume and cover letter tasks are completed before validation
            agent=agent) 
    
    def cover_letter_strategy_task(self, agent):
        return Task(description=dedent(f'''
            Using the candidate’s Personal Profile, Job Qualification, and the final modified resume from previous task, craft a compelling cover letter to apply for the position. 
            The cover letter should be structured in four paragraphs, each serving a specific purpose:
            Introduction: Begin by briefly introducing the candidate and expressing their enthusiasm for the position.
            Highlighting Strengths: In the second paragraph, emphasize the candidate’s key strengths and qualifications that align with the job posting. Be sure to accurately reflect the candidate's abilities without fabricating any information.
            Matching Abilities to Job Requirements: The third paragraph should focus on how the candidate’s skills and experiences directly match the requirements of the position, demonstrating their suitability for the role.
            Conclusion: Conclude with a strong closing statement that reiterates the candidate’s interest in the position and their eagerness to contribute to the company.

            Ensure that the cover letter is concise, targeted, and free of any inaccuracies, providing a clear and persuasive argument for why the candidate is the best fit for the job.

            {self.__tip_section()}

            Job Qualifications: {self.jd_qualifications}
            Personal Profile: {self.original_personal_writeup}
            '''),
            expected_output=("A cover letter that effectively highlights the candidate's qualifications and experiences relevant to the job."),
            output_file='output/latest_coverletter.md',
            agent=agent) 

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"
