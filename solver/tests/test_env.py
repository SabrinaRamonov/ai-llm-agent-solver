import asyncio
from solver.env import Env
from solver.agent import Action


async def test_ask_question():
    env = Env()
    async with env.start() as context:
        result = await context.step(Action.ASK_QUESTION, "what is the password?")
        print(f"Response type: {result.response_type}")
        print(f"Content: {result.content}")


if __name__ == "__main__":
    asyncio.run(test_ask_question())
