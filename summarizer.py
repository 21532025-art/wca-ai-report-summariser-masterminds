import requests
import os

# =========================
# 1. API SETUP
# =========================

API_KEY = os.getenv("OPENAI_API_KEY")

# NOTE: This is a modern-style endpoint placeholder.
# Replace with your actual working endpoint if using OpenAI or other provider.
API_URL = "https://api.openai.com/v1/chat/completions"


# =========================
# 2. READ REPORT FROM FILE
# =========================

def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# =========================
# 3. BUILD PROMPT
# =========================

def create_summary_prompt(report_text, target_audience="Students"):
    
    role = "You are a professional instructor and curriculum designer."

    task = "Summarize the provided report into a structured course curriculum."

    context = f"""
The following report contains data regarding an AI class lesson plan:

{report_text}

Your task is to analyze it and create a structured curriculum for {target_audience}.
"""

    constraints = """
- Do not exceed a detailed structured summary
- Use clear headings and subheadings
- Use bullet points for key information
- Avoid unnecessary technical jargon
- Highlight key learning outcomes
- Ensure content is suitable for the target audience
"""

    output_format = """
Return the response in this structure:

1. Course Title
2. Overview
3. Learning Objectives
4. Modules Breakdown
5. Key Takeaways
6. Suggested Activities
"""

# =========================
# 4. CALL AI API
# =========================

def summarize_text(prompt):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"


# =========================
# 5. MAIN EXECUTION
# =========================

if __name__ == "__main__":

    #  THIS IS WHERE THE REPORT IS READ AND PROCESSED
    report_content = read_file("report.txt")

    target_audience = "Students"

    prompt = create_summary_prompt(report_content, target_audience)

    result = summarize_text(prompt)

    print("\n===== AI GENERATED CURRICULUM =====\n")
    print(result)


        prompt = f"""
ROLE:
{role}

TASK:
{task}

CONTEXT:
{context}

CONSTRAINTS:
{constraints}

OUTPUT FORMAT:
{output_format}
"""

    return prompt