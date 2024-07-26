from enum import Enum, auto

class Action(Enum):
    ASK_QUESTION = auto()
    GUESS_PASSWORD = auto()

class Agent:
    def __init__(self):
        self.current_level = 1
        self.max_levels = 8

    async def next_action(self, page):
        # TODO: Implement logic to decide whether to ask a question or guess the password
        # This is a placeholder implementation
        if self.current_level <= self.max_levels:
            # For now, let's alternate between asking questions and guessing passwords
            return Action.ASK_QUESTION if self.current_level % 2 == 1 else Action.GUESS_PASSWORD
        else:
            print("Game over!")
            return None
