from agent.langchain_agent import agent

def is_gdp_question(text):
    keywords = ["gdp", "bip", "bruttoinlandsprodukt", "economic output", "gross domestic"]
    return any(k in text.lower() for k in keywords)

def main():
    print("Welcome to the LangChain GDP Agent!")
    print("Ask GDP-related questions like:\n- 'Germany, 1990'\n- 'Germany, France, UK, 2020'")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask a GDP question: ")
        if query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        if not is_gdp_question(query):
            print("Sorry, but I can only answer questions about GDP analysis.")
            continue  
        try:
            response = agent.invoke(query)
            print(f"{response}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()