def create_summary_prompt(report_text, target_audience="Students", students="students"):
    # 1. ROLE: `Define who the AI is`
    role = "You are a professional instructor."
    
    # 2. TASK: `Define the primary action`
    task = "Summarize the provided report into a high-level course summary."
    
    # 3. CONTEXT: `Provide background data (the actual report content)`
    context = f"The following report contains data regarding AI class lesson Plan:\n\n{ report_text}\n\nYour task is to analyze this report and create a comprehensive summary that can be used to design a course curriculum for {target_audience}."
    
    # 4. CONSTRAINTS: `List boundaries and rules`
    constraints = (
        "- Do not exceed a five page document.\n"
        "- Avoid technical jargon unless necessary.\n"
        "- Put bullet points in order of importance.\n"
        "- Add neccessary Headings and Subheadings to make the lesson  easier to read.\n"
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
        "4. "
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

# Usage example
report_content = "Ai Class Lesson Plan..."
final_prompt = create_summary_prompt(report_content)
print(final_prompt)

