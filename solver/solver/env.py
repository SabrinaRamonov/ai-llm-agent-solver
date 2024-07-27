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
        logger.info(f"Asking question: {question}")
        
        # Wait for the textarea to be available
        await self._page.wait_for_selector("textarea#comment")
        logger.info("Textarea found")

        # Fill out the textarea with the question and press Enter
        await self._page.fill("textarea#comment", question)
        await self._page.press("textarea#comment", "Enter")
        logger.info("Question submitted")

        # Wait for the response to be visible
        response_element = await self._page.wait_for_selector("p.answer")
        logger.info("Response element found")

        # Read the text content of the response
        response_text = await response_element.inner_text()
        logger.info(f"Response received: {response_text[:100]}...")  # Log first 100 chars of response

        return StepResult("guess_result", response_text)

    async def guess_password(self, password: str) -> StepResult:
        logger.info(f"Guessing password: {password}")
        
        # Wait for the input element to be available
        await self._page.wait_for_selector("input#guess")
        logger.info("Password input field found")

        # Fill out the input with the password guess
        await self._page.fill("input#guess", password)
        logger.info("Password entered")

        # Click the Validate button
        await self._page.click('button:has-text("Validate")')
        logger.info("Validate button clicked")

        # Wait for the result alert to appear
        alert_element = await self._page.wait_for_selector("div.customAlert")
        logger.info("Alert element found")

        # Read the text content of the alert
        alert_text = await alert_element.inner_text()
        logger.info(f"Alert text: {alert_text}")

        if "Wrong password" in alert_text:
            logger.info("Incorrect password")
            return StepResult("incorrect_password")
        else:
            logger.info("Correct password!")
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
