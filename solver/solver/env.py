from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, Page
from agent import Action

class StepResult:
    def __init__(self, response_type: str, content: str = None):
        self.response_type = response_type
        self.content = content

class EnvContext:
    def __init__(self, page: Page):
        self._page = page

    async def step(self, action: Action) -> StepResult:
        if action == Action.ASK_QUESTION:
            # TODO: Implement logic to ask a question
            return StepResult("guess_result", "LLM feedback for the question")
        elif action == Action.GUESS_PASSWORD:
            # TODO: Implement logic to guess the password
            # For now, we'll assume it's always incorrect
            return StepResult("incorrect_password")

class Env:
    def __init__(self, url: str = "https://gandalf.lakera.ai/baseline"):
        self.url = url

    @asynccontextmanager
    async def start(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(self.url)
            
            try:
                yield EnvContext(page)
            finally:
                await browser.close()
