import asyncio
from playwright.async_api import async_playwright
from agent import Agent, Action

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://gandalf.lakera.ai/baseline")
        
        agent = Agent()
        while True:
            action = await agent.next_action(page)
            if action is None:
                break
            
            if action == Action.ASK_QUESTION:
                # TODO: Implement logic to ask a question
                print("Asking a question...")
            elif action == Action.GUESS_PASSWORD:
                # TODO: Implement logic to guess the password
                print("Guessing the password...")
            
            # TODO: Implement logic to handle the response and update the agent's state
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
