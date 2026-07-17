import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Structured verification response schema
class VerificationResponse(BaseModel):
    label: str = Field(..., description="Certain, Uncertain, or Needs Verification")
    confidence: int = Field(..., description="Confidence score from 0 to 100")
    reason: str = Field(..., description="Short explanation of why the label was assigned")
    supported_facts: list[str] = Field(..., description="Facts from the AI answer that are supported by the evidence")
    contradictions: list[str] = Field(..., description="Contradictions between the AI answer and the evidence")

# Lazy-loaded Gemini Client
_client = None

def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in environment or .env file.")
        _client = genai.Client(api_key=api_key)
    return _client

async def verify_answer(question: str, answer: str, sources: list[dict]) -> dict:
    """
    Compares the generated AI answer against Tavily evidence snippets using Gemini 3.5 Flash as a verifier.
    Relies ONLY on the supplied evidence and ignores external knowledge.
    
    Args:
        question: The user's input question.
        answer: The AI-generated answer to fact-check.
        sources: A list of dicts representing Tavily search results.
        
    Returns:
        A dict matching the VerificationResponse schema.
    """
    client = get_client()

    # Compile retrieved sources into structured text
    evidence_text = ""
    if not sources:
        evidence_text = "No evidence retrieved."
    else:
        for idx, src in enumerate(sources):
            evidence_text += f"Source {idx+1}: {src.get('title', 'Untitled')}\n"
            evidence_text += f"URL: {src.get('url', '#')}\n"
            evidence_text += f"Content: {src.get('content', '')}\n\n"

    # Verification prompt instructing Gemini to compare answer against ONLY evidence
    prompt = f"""You are an AI fact-checking assistant.

You are NOT allowed to use your own knowledge.

Only use the supplied evidence.

Question:
{question}

AI Answer:
{answer}

Evidence:
{evidence_text}

Determine whether the AI answer is:
Certain
Uncertain
Needs Verification

Definitions:
Certain:
- The answer is fully supported by multiple pieces of evidence.
- No contradictions exist.

Uncertain:
- Evidence only partially supports the answer.
- Some important details are missing.
- Evidence is weak or limited.

Needs Verification:
- Evidence contradicts the answer.
- No reliable supporting evidence exists.

Return ONLY valid JSON.

Format:
{{
  "label": "Certain" | "Uncertain" | "Needs Verification",
  "confidence": 0-100,
  "reason": "Short explanation",
  "supported_facts": ["...", "..."],
  "contradictions": ["...", "..."]
}}

Do not return Markdown.
Do not return code blocks.
Return JSON only.
"""

    async def call_gemini_verifier(stricter_instruction: str = "") -> dict:
        full_prompt = prompt
        if stricter_instruction:
            full_prompt += f"\n\nCRITICAL WARNING: {stricter_instruction}"

        # Request structured JSON format from Gemini using Pydantic schema
        model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash").strip()
        response = await client.aio.models.generate_content(
            model=model_name,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VerificationResponse,
                temperature=0.0  # Keep verification deterministic
            )
        )

        if not response or not response.text:
            raise RuntimeError("Gemini verifier returned empty response text.")

        # Parse JSON response
        parsed = json.loads(response.text)
        
        # Normalise / sanitize labels
        label = parsed.get("label", "Needs Verification")
        if label not in ["Certain", "Uncertain", "Needs Verification"]:
            parsed["label"] = "Needs Verification"
            
        return parsed

    try:
        # First attempt
        return await call_gemini_verifier()
    except Exception as e:
        print(f"First verification call failed: {str(e)}. Retrying with stricter instructions...")
        try:
            # Second attempt with strict retry warning
            stricter_msg = "Your previous output failed validation. You MUST return ONLY valid JSON matching the exact schema definition. No extra text or formatting."
            return await call_gemini_verifier(stricter_instruction=stricter_msg)
        except Exception as retry_err:
            print(f"Retry verification call failed: {str(retry_err)}. Using fallback response.")
            # Graceful fallback response to prevent API crashes
            return {
                "label": "Needs Verification",
                "confidence": 0,
                "reason": f"Verification failed due to a processing error: {str(retry_err)}",
                "supported_facts": [],
                "contradictions": ["The system could not run the verification check successfully. Please check server logs."]
            }
