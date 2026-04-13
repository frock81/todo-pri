from google import genai

client = genai.Client()

def call_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )
    return response.parsed
