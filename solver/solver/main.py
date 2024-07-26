import asyncio
from playwright.async_api import async_playwright
from agent import Agent

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://gandalf.lakera.ai/baseline")
        
        agent = Agent()
        await agent.solve_game(page)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
