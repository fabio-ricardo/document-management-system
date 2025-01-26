
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def categorize_document(content: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that categorizes documents."},
            {"role": "user", "content": f"Categorize the following document content into one of these categories: Invoice, Contract, Report, or Other. Content: {content}"},
        ],
        max_tokens=10,
    )
    return response.choices[0].message.content.strip()

def summarize_document(content: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
            {"role": "user", "content": f"Summarize the following document content in one sentence: {content}"},
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content.strip()
