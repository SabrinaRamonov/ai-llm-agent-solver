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
            if action == Action.GAME_OVER:
                break
            await agent.execute_action(action, page)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
