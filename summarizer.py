import os
import json
import anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# 1. API SETUP
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# To maintain conversation history
messages = []  

# Function to summarize text using AI API
def summarize_text(text):
    # Validate API key
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
    
    # RTCCO structured prompt
    def create_summary_prompt(report_text, target_audience="Students"):

        # 1. ROLE: `Define who the AI is`
        role = "You are a professional instructor."

        # 2. TASK: `Define the primary action`
        task = "Summarize the provided report into a high-level course summary."

        # 3. CONTEXT: `Provide necessary background information`
        context = f"The following report contains data regarding AI class lesson Plan:\n\n{report_text}\n\nYour task is to analyze this report and create a comprehensive summary that can be used to design a course curriculum for {target_audience}."

        # 4. CONSTRAINTS: `List any limitations or requirements`
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

        # 5. OUTPUT: `Specify the desired format of the response`
        output_format = (
            "Structure the response as follows:\n"
            "1. A 3-5 page report summarizing the whole topic.\n"
            "2. A clear topic and subtopics.\n"
            "3. Bullet points on important key points.\n"
            "4. Key takeaways and actionable recommendations."
        )
        
        #combine into a single prompt
        prompt = f"""
ROLE: {role}
TASK: {task}
CONTEXT: {context}
CONSTRAINTS: {constraints}
OUTPUT: {output_format}

"""
        return prompt

# Use the structured prompt
    prompt = create_summary_prompt(text)
    messages.append({"role": "user", "content": prompt})
    
    # Call Anthropic API using SDK
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=messages
    )
    
    # Extract and return the summary
    summary = response.content[0].text
    messages.append({"role": "assistant", "content": summary})
    return summary


# Main program
def main():
    print("=== AI Report Summariser ===")
    
    text = input("Paste your report:\n")
   
    if not text.strip():
        print("No input provided.")
        return
    
    print("\nGenerating summary...\n")
    
    try:
        summary = summarize_text(text)
        print("=== Executive Summary ===")
        print(summary)
            
    except ValueError as ve:
        print(f"Configuration error: {ve}")
    except anthropic.APIError as ae:
        print(f"API error: {ae}")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Run program
if __name__ == "__main__":
    main()