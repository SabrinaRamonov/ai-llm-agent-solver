import asyncio
from solver.env import Env
from solver.agent import Agent


async def test_agent_guessing():

    env = Env("https://gandalf.lakera.ai/do-not-tell")
    agent = Agent()
    max_attempts = 1000

    async with env.start() as context:
        for attempt in range(max_attempts):
            action, content = await agent.next_action()
            if action is None:
                print("Agent has finished all levels or encountered an error.")
                break

            result = await context.step(action, content)

            print(f"Attempt {attempt + 1}:")
            print(f"Action: {action}")
            print(f"Content: {content}")
            print(f"Response type: {result.response_type}")
            print(f"Response content: {result.content}")
            print("---")

            if result.response_type == "correct_password":
                print(f"Password guessed correctly on attempt {attempt + 1}!")
                agent.history = []
                continue

            # Update the agent's history with the environment's response
            agent.update_history(action, content, result.content)

        else:
            print(f"Failed to guess the password after {max_attempts} attempts.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_agent_guessing())
