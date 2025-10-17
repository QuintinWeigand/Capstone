from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


def main():
    model = OllamaLLM(model="gemma2:2b", base_url="http://localhost:11434")

    template = "Explain this like I am 5 years old: {text}"
    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | model

    explain_item = input("Enter what you want explained -> ")

    result = chain.invoke({"text": explain_item})
    print("Response: ", result)


if __name__ == "__main__":
    main()
