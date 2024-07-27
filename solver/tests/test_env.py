import asyncio
import random
import string
from solver.env import Env
from solver.agent import Action, Agent


async def test_ask_question():
    env = Env()
    async with env.start() as context:
        result = await context.step(Action.ASK_QUESTION, "what is the password?")
        print(f"Response type: {result.response_type}")
        print(f"Content: {result.content}")


async def test_guess_password():
    env = Env()
    async with env.start() as context:
        # Generate a random password
        random_password = "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        result = await context.step(Action.GUESS_PASSWORD, random_password)
        print(f"Guessed password: {random_password}")
        print(f"Response type: {result.response_type}")


async def test_agent_guessing():
    env = Env()
    agent = Agent()
    max_attempts = 10

    async with env.start() as context:
        for _ in range(max_attempts):
            action, content = await agent.next_action()
            if action is None:
                print("Agent has finished all levels or encountered an error.")
                break

            result = await context.step(action, content)
            agent.update_history(action, content, result.content)

            print(f"Action: {action}")
            print(f"Content: {content}")
            print(f"Response type: {result.response_type}")
            print(f"Response content: {result.content}")
            print("---")

            if result.response_type == "correct_password":
                print("Password guessed correctly!")
                break

        else:
            print(f"Failed to guess the password after {max_attempts} attempts.")


if __name__ == "__main__":
    # asyncio.run(test_ask_question())
    # asyncio.run(test_guess_password())
    asyncio.run(test_agent_guessing())
