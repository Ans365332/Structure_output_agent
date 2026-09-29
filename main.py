from src.agent import structured_query_agent


def main():

    print("====================================")
    print("   STRUCTURED OUTPUT AI AGENT")
    print("====================================")
    print("Type 'exit' to stop the agent.")
    print()

    while True:

        try:

            user_query = input("You: ").strip()

            if user_query.lower() == "exit":

                print("\nAgent stopped. Goodbye!")
                break

            if not user_query:

                print("\nPlease enter a query.\n")
                continue

            # -----------------------------------------
            # CALL AGENT
            # -----------------------------------------

            result = structured_query_agent(
                user_query=user_query,
                max_retries=3
            )

            # -----------------------------------------
            # FINAL RESPONSE
            # -----------------------------------------

            print("\n====================================")
            print("FINAL RESPONSE")
            print("====================================")

            if "error" in result:

                print(result["error"])
                print()

                continue

            print("\nQuery:")
            print(result["query"])

            print("\nAnswer:")
            print(result["answer"])

            print("\nKey Points:")

            for point in result["key_points"]:
                print(f"- {point}")

            print(f"\nDifficulty: {result['difficulty']}")

            print()

        except KeyboardInterrupt:

            print("\n\nAgent stopped by user.")
            break

        except Exception as e:

            print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()