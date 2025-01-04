We are going to have 3 versions for the chatbot 
    1. Chatbot for communicating in words
    2. Voice
    3. Real character


1.1 Plain chat based on resume and jd to make it work

1.2 add feature: 
    1. able to be given a question from a pdf (try argentic retrieval)
    2. The answer will be evaluated based on an evaluator for a score from 1 to 10. Give the right answer afterwards.



def generate_qa_pairs(book_content):
    """
    You are an expert data science interviewer. Your task is to:
    1. Read through the provided book content carefully
    2. Generate question-answer pairs that test key data science concepts from the book
    3. For each pair:
        - Create a challenging but fair interview question
        - Provide a detailed model answer that demonstrates mastery
        - Include relevant code examples or mathematical formulas where appropriate
        
    Format each QA pair as:
    {
        'question': 'Clear, concise question text',
        'answer': 'Comprehensive answer with examples',
        'category': 'Topic category (e.g., ML, Statistics, Programming)',
        'difficulty': 'Easy/Medium/Hard'
    }
    
    Consider:
    - Focus on practical applications and real-world scenarios
    - Include both theoretical understanding and implementation details
    - Vary question types (conceptual, coding, mathematical)
    - Ensure questions are unambiguous and well-defined
    """
    # Implementation here
    pass

def score_question_quality(question_data):
    """
    You are a data science interview question evaluator. Your task is to:
    1. Analyze the given question for quality on a scale of 0-100
    2. Consider these criteria:
        - Relevance to data science (0-25 points)
        - Clarity and specificity (0-25 points)
        - Technical depth (0-25 points)
        - Practical applicability (0-25 points)
    
    For each criterion, consider:
    Relevance:
    - Does it test essential data science knowledge?
    - Is it aligned with industry requirements?
    
    Clarity:
    - Is the question unambiguous?
    - Are all necessary context and constraints provided?
    
    Technical Depth:
    - Does it require deep understanding?
    - Does it test multiple related concepts?
    
    Practical Applicability:
    - Can the knowledge be applied in real scenarios?
    - Does it reflect actual job responsibilities?
    
    Return a detailed scoring breakdown and final score.
    """
    # Implementation here
    pass

def evaluate_candidate_answer(candidate_response, model_answer):
    """
    You are an expert data science interviewer evaluating candidate responses.
    Score the candidate's answer from 1-10 based on:
    
    1. Technical Accuracy (40% weight):
    - Correctness of concepts and terminology
    - Proper understanding of underlying principles
    - Accurate use of formulas or algorithms
    
    2. Completeness (30% weight):
    - Coverage of all key points from the model answer
    - Depth of explanation
    - Inclusion of relevant examples
    
    3. Communication (30% weight):
    - Clarity of explanation
    - Logical structure
    - Appropriate use of technical language
    
    Provide:
    1. Numerical score (1-10)
    2. Detailed feedback with:
        - Strengths
        - Areas for improvement
        - Missing key points
        - Suggestions for better articulation
    
    Consider:
    - Different valid approaches to the same problem
    - Partial credit for partially correct answers
    - Both theoretical understanding and practical application
    """
    # Implementation here
    pass

def select_interview_question(qa_pairs, num_questions=1):
    """
    You are tasked with selecting optimal interview questions. Your role is to:
    1. Review the provided QA pairs and their quality scores
    2. Select questions considering:
        - Quality score (prioritize highest-scoring questions)
        - Topic coverage (ensure diverse topics if multiple questions)
        - Difficulty distribution (maintain appropriate challenge level)
    
    Selection criteria:
    - Randomly select from top 36 highest-scoring questions
    - Ensure selected questions cover different aspects of data science
    - Balance theoretical and practical questions
    
    Return:
    - Selected question(s) with full context
    - Reasoning for selection
    """
    # Implementation here
    pass