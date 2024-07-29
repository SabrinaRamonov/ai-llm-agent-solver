from contextlib import asynccontextmanager
from playwright.async_api import async_playwright, Page
from solver.agent import Action
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("solver.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)


class StepResult:
    def __init__(self, response_type: str, content: str = None):
        self.response_type = response_type
        self.content = content


class EnvContext:
    def __init__(self, page: Page):
        self._page = page

    async def ask_question(self, question: str) -> StepResult:
        await self._page.wait_for_selector("textarea#comment")
        await self._page.fill("textarea#comment", question)
        await self._page.press("textarea#comment", "Enter")

        response_element = await self._page.wait_for_selector("p.answer")
        response_text = await response_element.inner_text()
        
        logger.info(f"Environment response: {response_text}...")

        return StepResult("guess_result", response_text)

    async def guess_password(self, password: str) -> StepResult:
        await self._page.wait_for_selector("input#guess")
        await self._page.fill("input#guess", password)
        await self._page.click('button:has-text("Validate")')

        alert_element = await self._page.wait_for_selector("div.customAlert")
        alert_text = await alert_element.inner_text()
        
        logger.info(f"Environment response: {alert_text}")

        if "Wrong password" in alert_text:
            return StepResult("incorrect_password")
        else:
            # wait for button that says 'Next Level' to appear
            await self._page.wait_for_selector('button:has-text("Next Level")')
            # press this button
            await self._page.click('button:has-text("Next Level")')
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
        logger.info(f"Environment initialized with URL: {self.url}")

    @asynccontextmanager
    async def start(self):
        logger.info("Starting environment")
        async with async_playwright() as p:
            logger.info("Launching browser")
            browser = await p.chromium.launch()
            logger.info("Creating new page")
            page = await browser.new_page()
            logger.info(f"Navigating to URL: {self.url}")
            await page.goto(self.url)

            try:
                logger.info("Environment setup complete, yielding EnvContext")
                yield EnvContext(page)
            finally:
                logger.info("Closing browser")
                await browser.close()
        logger.info("Environment stopped")