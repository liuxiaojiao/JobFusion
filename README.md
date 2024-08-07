# JobFusion

The JobFusion, an AI career enhancer, aims to revolutionize the job application and recruitment process through AI-driven customization and preparation tools. By serving both job seekers and hiring professionals, it promises to enhance efficiency, accuracy, and success rates in securing job opportunities and finding ideal candidates.


## Product Goal:

Provide comprehensive AI assistance for updating resumes, crafting cover letters, and preparing for interviews based on specific job descriptions. 


## Main function:
- Extract Key Skills and Qualifications:
  - Utilize advanced AI to analyze job descriptions and identify the essential skills, experiences, and qualifications required.
- Tailor Resumes:
  - Customize the candidate's work experience, skills, and education on their resume to align with the job posting, highlighting their most relevant abilities.
- Create Customized Cover Letters:
  - Generate personalized cover letters that emphasize the candidate’s strengths, qualifications, and experiences pertinent to the job.
- Interview Preparation:
  - Develop a set of potential interview questions and key talking points based on the candidate's resume, cover letter, and job qualifications.
  - Provide a mock interview experience with an AI Avatar, offering realistic practice sessions and feedback.


## Competitive Advantages:
- Dual Market Leverage:
  - To Consumers (B2C): Assist students, recent graduates, and professionals in optimizing their resumes and cover letters to better match job qualifications, offering valuable insights and progress through AI-driven mock interviews.
  - To Businesses (B2B): Enable hiring managers and recruiters to enhance their service offerings by improving candidates' interview success rates, extending beyond traditional recruitment processes.
- Efficiency and Precision:
  - Leveraging AI to quickly and accurately tailor application materials, saving time for both candidates and recruiters while increasing the likelihood of interview success.
- Comprehensive Preparation:
  - Providing a holistic approach to job applications by not only refining documents but also preparing candidates for the interview process through AI simulations.


## Future Development:
- LinkedIn Integration:
  - Expand the product’s capabilities to include searching for potential candidates on LinkedIn, further streamlining the recruitment process and identifying top talent efficiently.


## Milestones:
- [x] MVP draft: Jul 23, 2024
- [ ] MVP development timeline: Jul 24, 2024 -- Aug 31, 2024
   

## Run JobFusion Application:
- Local hosting through streamlit:

env: python==3.10; 
Change .env.example.txt to .env with valid API keys

```pip install -r requirements.txt``` 

```streamlit run jobfusion_app.py```

or
```poetry install```/```poetry update```; ```peotry shell```

```poetry run streamlit run jobfusion_app.py```

- This MVP is available for a public URL on Streamlit Cloud
