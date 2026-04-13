from openai import OpenAI

client = OpenAI()


def call_llm(prompt: str) -> dict:
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

    return response.output[0].content[0].parsed
