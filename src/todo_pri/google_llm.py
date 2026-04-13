from google import genai

client = genai.Client()


def call_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )
    if not isinstance(response.parsed, dict):
        raise ValueError("Expected response to be a dict")
    return str(response.parsed)
