import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# We will initialize the client dynamically or at startup to ensure it picks up any updates to .env
_client = None

def get_client() -> genai.Client:
    """
    Returns an initialized Google GenAI Client.
    """
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            # We don't crash at startup if key is missing, but we raise when used.
            # This allows the app to start even if the user hasn't filled the .env yet.
            raise ValueError("GEMINI_API_KEY is not set in environment or .env file.")
        _client = genai.Client(api_key=api_key)
    return _client

async def generate_answer(question: str) -> str:
    """
    Asynchronously queries Gemini 3.5 Flash with the provided question and returns the answer.
    
    Args:
        question: The user's input question.
        
    Returns:
        The generated text response from Gemini.
    """
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    client = get_client()
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()
    try:
        # Use the modern client.aio async interface of the google-genai SDK
        response = await client.aio.models.generate_content(
            model=model_name,
            contents=question
        )
        if not response or not response.text:
            raise RuntimeError("Gemini API returned an empty response.")
        return response.text
    except Exception as e:
        # Wrap the error to give descriptive feedback
        raise RuntimeError(f"Gemini API error: {str(e)}")
