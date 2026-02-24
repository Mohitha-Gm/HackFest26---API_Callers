from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"


def analyze_patterns(jobs):
    prompt = f"""
    You are a career optimization AI agent.

    Analyze this job application dataset:

    {jobs}

    1. Identify which resume versions perform best.
    2. Identify which role types get more interviews.
    3. Suggest improvements.
    4. Provide strategic advice to maximize interview rate.

    Return clear bullet-point insights.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def generate_followup_email(job):
    prompt = f"""
    Draft a short professional follow-up email.

    Company: {job['company']}
    Role: {job['role']}
    Applied more than 7 days ago.

    Keep it polite and concise.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def generate_cold_outreach(job, resume_summary, hr_name):
    prompt = f"""
    Draft a short, professional follow-up email.

    Candidate Name: Mohitha G
    Applied Role: {job['role']}
    Company: {job['company']}
    HR Contact: {hr_name}

    Resume Summary:
    {resume_summary}

    The email should:
    - Mention the applied role
    - Highlight 1 relevant project
    - Be polite and concise
    - Not sound generic
    - Stay under 150 words
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def get_resume_summary():
    return """
    Candidate Name: Mohit

    Education:
    - B.Tech in Computer Science

    Core Skills:
    - Python
    - Machine Learning
    - Deep Learning
    - FastAPI
    - Backend Development
    - Data Structures & Algorithms
    - REST APIs
    - SQL

    Key Projects:
    - AI Financial Agent using Gemini + MCP
    - Crop Disease Detection using Multimodal AI
    - Autonomous Job Tracking & Optimization Agent
    - RAG-based Government Scheme Assistant

    Domain Focus:
    - Machine Learning Engineering
    - Backend Systems
    - AI Agent Architectures

    Technical Strengths:
    - Building production-grade APIs
    - Integrating LLMs into real systems
    - Designing agentic workflows
    - Cloud deployment (Cloud Run)
    """