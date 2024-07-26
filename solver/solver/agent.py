from enum import Enum, auto

class Action(Enum):
    GET_PROMPT = auto()
    GENERATE_RESPONSE = auto()
    SUBMIT_RESPONSE = auto()
    GAME_OVER = auto()

class Agent:
    def __init__(self):
        self.current_level = 1
        self.max_levels = 8
        self.prompt = None
        self.response = None

    async def next_action(self, page):
        if self.current_level > self.max_levels:
            return Action.GAME_OVER

        if self.prompt is None:
            return Action.GET_PROMPT

        if self.response is None:
            return Action.GENERATE_RESPONSE

        return Action.SUBMIT_RESPONSE

    async def execute_action(self, action, page):
        if action == Action.GET_PROMPT:
            self.prompt = await self.get_prompt(page)
            print(f"Level {self.current_level} prompt: {self.prompt}")

        elif action == Action.GENERATE_RESPONSE:
            self.response = self.generate_response(self.prompt)
            print(f"Generated response: {self.response}")

        elif action == Action.SUBMIT_RESPONSE:
            success = await self.submit_response(page, self.response)
            if success:
                self.current_level += 1
                print(f"Successfully solved level {self.current_level - 1}")
            else:
                print(f"Failed to solve level {self.current_level}")
            self.prompt = None
            self.response = None

        elif action == Action.GAME_OVER:
            print("Game over!")

    async def get_prompt(self, page):
        # TODO: Implement logic to extract the prompt from the page
        pass

    def generate_response(self, prompt):
        # TODO: Implement logic to generate a response based on the prompt
        pass

    async def submit_response(self, page, response):
        # TODO: Implement logic to submit the response and check if it was successful
        pass
