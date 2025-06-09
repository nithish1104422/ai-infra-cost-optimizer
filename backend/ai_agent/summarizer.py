# GPT-based summarization logic

import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(resource_name, resource_type, usage_data, recommendation):
    prompt = (
        f"Summarize the cost optimization insight for the following cloud resource:\n\n"
        f"Resource Name: {resource_name}\n"
        f"Resource Type: {resource_type}\n"
        f"Usage Data: {usage_data}\n"
        f"Recommendation: {recommendation}\n\n"
        f"Generate a short and clear summary suitable for Slack or an executive dashboard."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful cloud cost optimization assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"
