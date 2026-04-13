from openai import OpenAI

client = OpenAI()


def call_llm(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        # response_format={
        #     "type": "json_schema",
        #     "json_schema": {
        #         "name": "response",
        #         "schema": {
        #             "type": "object",
        #             "properties": {
        #                 "answer": {"type": "string"},
        #                 "confidence": {"type": "number"},
        #             },
        #             "required": ["answer"],
        #         },
        #     },
        # },
    )
    if not isinstance(response.output_text, str):
        raise ValueError("Expected response output to be a string")
    return response.output_text
