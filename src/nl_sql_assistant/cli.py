from nl_sql_assistant.pipeline import run_text_to_sql


def main():
    print("NL-SQL Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Ask a question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        if not question:
            print("Please enter a question.\n")
            continue

        try:
            result = run_text_to_sql(question)

            print("\nGenerated SQL:")
            print(result["sql"])

            print("\nResults:")
            for row in result["results"]:
                print(row)

            print()

        except Exception as error:
            print(f"\nError: {error}\n")


if __name__ == "__main__":
    main()