from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, Page
from solver.agent import Action


class StepResult:
    def __init__(self, response_type: str, content: str = None):
        self.response_type = response_type
        self.content = content


class EnvContext:
    def __init__(self, page: Page):
        self._page = page

    async def ask_question(self, question: str) -> StepResult:
        # Wait for the textarea to be available
        await self._page.wait_for_selector("textarea#comment")

        # Fill out the textarea with the question and press Enter
        await self._page.fill("textarea#comment", question)
        await self._page.press("textarea#comment", "Enter")

        # Wait for the response to be visible
        response_element = await self._page.wait_for_selector("p.answer")

        # Read the text content of the response
        response_text = await response_element.inner_text()

        return StepResult("guess_result", response_text)

    async def guess_password(self, password: str) -> StepResult:
        # Wait for the input element to be available
        await self._page.wait_for_selector("input#guess")

        # Fill out the input with the password guess
        await self._page.fill("input#guess", password)

        # Click the Validate button
        await self._page.click('button:has-text("Validate")')

        # Wait for the result alert to appear
        alert_element = await self._page.wait_for_selector("div.customAlert")

        # Read the text content of the alert
        alert_text = await alert_element.inner_text()

        if "Wrong password" in alert_text:
            return StepResult("incorrect_password")
        else:
            return StepResult("correct_password")

    async def step(self, action: Action, input_str: str) -> StepResult:
        if action == Action.ASK_QUESTION:
            return await self.ask_question(input_str)
        elif action == Action.GUESS_PASSWORD:
            return await self.guess_password(input_str)
        else:
            raise ValueError(f"Unknown action: {action}")


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
