import asyncio
from env import Env
from agent import Agent

async def main():
    env = Env()
    agent = Agent()

    async with env.start() as env_context:
        while True:
            action = await agent.next_action()
            if action is None:
                break

            result = await env_context.step(action)
            
            if result.response_type == "correct_password":
                print("Correct password guessed!")
                break
            elif result.response_type == "incorrect_password":
                print("Incorrect password guessed.")
            elif result.response_type == "guess_result":
                print(f"LLM feedback: {result.content}")

            # TODO: Update agent's state based on the result

if __name__ == "__main__":
    asyncio.run(main())
