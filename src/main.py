import ollama
from dotenv import load_dotenv
import os
load_dotenv()
INFERENCE_HOST = os.getenv("INFERENCE_HOST")


def main():
    client = ollama.Client(host=INFERENCE_HOST)
    response = client.chat(
        model='qwen2.5vl:3b',
        messages=[{
            'role': 'user',
            'content': 'What is 10 + 10'
        }]
    )

    print(response['message']['content'])


if __name__ == "__main__":
    main()
