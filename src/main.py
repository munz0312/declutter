import ollama


def main():
    client = ollama.Client(host='http://192.168.1.131:11434')
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
