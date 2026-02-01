import ollama

MODEL_NAME = "phi3:mini"

def call_llm(prompt: str) -> str:
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        options={
            "num_ctx": 1024,
            "temperature": 0.2
        },
        stream=True,
        keep_alive="30m"
    )

    final = ""
    for chunk in response:
        final += chunk["message"]["content"]

    return final