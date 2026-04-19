import requests
import os
import json

# Replace with your actual API key
API_KEY = os.getenv("OPENAI_API_KEY")
API_URL = "https://api.openai.com/v1/chat/completions"

# Headers for API authentication
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Function to read file content
def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# RTCCO structured prompt
def create_summary_prompt(report_text, target_audience="Students"):
    # 1. ROLE: `Define who the AI is`
    role = "You are a professional instructor."
    
    # 2. TASK: `Define the primary action`
    task = "Summarize the provided report into a high-level course summary."
    
    # 3. CONTEXT: `Provide background data (the actual report content)`
    context = f"The following report contains data regarding AI class lesson Plan:\n\n{report_text}\n\nYour task is to analyze this report and create a comprehensive summary that can be used to design a course curriculum for {target_audience}."
    
    # 4. CONSTRAINTS: `List boundaries and rules`
    constraints = (
        "- Do not exceed a five page document.\n"
        "- Avoid technical jargon unless necessary.\n"
        "- Put bullet points in order of importance.\n"
        "- Add necessary Headings and Subheadings to make the lesson easier to read.\n"
        "- Highlight all the key points for each section.\n"
        "- Provide actionable insights based on the data analysis.\n"
        "- Use clear and concise language to communicate the course work effectively.\n"
        f"- Ensure the tone is professional and suitable for {target_audience}."
    )
    
    # 5. OUTPUT: `Specify the exact structure of the response`
    output_format = (
        "Structure the response as follows:\n"
        "1. A 3-5 page report summarizing the whole topic.\n"
        "2. A clear topic and subtopics.\n"
        "3. Bullet points on important key points.\n"
    )

    # Combine into a final prompt
    prompt = f"""
ROLE: {role}
TASK: {task}
CONTEXT: {context}
CONSTRAINTS: {constraints}
OUTPUT: {output_format}
"""
    return prompt

# Function to summarize text using AI API 
def summarize_text(text):
    if not API_KEY:
        return "Error: OPENAI_API_KEY environment variable is not set."

    # Create the prompt
    final_prompt = create_summary_prompt(text)

    # Request body
    data = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": "You summarize reports clearly."},
            {"role": "user", "content": final_prompt}
        ],
        "temperature": 0.5,
    }

    # Send POST request to AI API
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        # Convert JSON response into python dictionary
        result = response.json()
        
        # Extract summary from JSON
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        return f"Error: API request failed - {str(e)}"
    except (KeyError, IndexError) as e:
        return f"Error: Unexpected response format - {str(e)}"

# Main program
def main():
    print("=== AI Report Summariser ===")

    # User input choice
    choice = input("Enter '1' to paste text or '2' to upload file: ")

    if choice == "1":
        text = input("Paste your report:\n")
    elif choice == "2":
        path = input("Enter file path: ")
        try:
            text = read_file(path)
        except FileNotFoundError:
            print("Error: File not found.")
            return
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return
    else:
        print("Invalid choice")
        return

    print("\nGenerating summary...\n")

    # Get summary
    summary = summarize_text(text)

    print("=== Executive Summary ===")
    print(summary)

# Run program
if __name__ == "__main__":
    main()