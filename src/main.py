from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import os
import utils

load_dotenv()
INFERENCE_HOST = os.getenv("INFERENCE_HOST")


def main():

    client = ChatOllama(model='qwen2.5vl:3b', base_url=INFERENCE_HOST)
    file_path = "/home/munzir/Downloads/strawberry.jpg"
    image_data = utils.encode_image(file_path)
    mime_type = utils.get_mime_type(file_path)

    messages = [
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": """
                            What's in this image?
                            Describe it briefly in one sentence.
                            """
                },
                {
                    "type": "image_url",
                    "image_url": f"data:{mime_type};base64,{image_data}"
                }
            ]
        )
    ]

    ai_msg = client.invoke(messages)
    print(ai_msg.content)


if __name__ == "__main__":
    main()
