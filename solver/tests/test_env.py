import asyncio
import random
import string
from solver.env import Env
from solver.agent import Action


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


if __name__ == "__main__":
    # asyncio.run(test_ask_question())
    asyncio.run(test_guess_password())
