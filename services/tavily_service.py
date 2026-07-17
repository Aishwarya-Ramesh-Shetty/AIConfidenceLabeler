import os
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def search_evidence(question: str) -> list[dict]:
    """
    Queries the Tavily Search API asynchronously to retrieve the top 3 search results.
    
    Args:
        question: The user's input question.
        
    Returns:
        A list of dictionaries containing 'title', 'url', and 'content' keys.
        Returns an empty list on key omission or API failures to fail gracefully.
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key or not api_key.strip():
        # Handle missing key gracefully (log warning and return empty sources)
        print("Tavily search skipped: TAVILY_API_KEY is not configured in .env")
        return []

    if not question or not question.strip():
        return []

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": question,
        "search_depth": "basic",
        "max_results": 3
    }

    try:
        # Perform asynchronous POST request to Tavily
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code != 200:
                print(f"Tavily API responded with status {response.status_code}: {response.text}")
                return []
                
            data = response.json()
            results = data.get("results", [])
            
            # Format and return the top 3 sources
            sources = []
            for item in results[:3]:
                sources.append({
                    "title": item.get("title", "Untitled Source"),
                    "url": item.get("url", "#"),
                    "content": item.get("content", "")
                })
            return sources

    except Exception as e:
        # Log exception and fail gracefully
        print(f"Tavily API connection failed: {str(e)}")
        return []
