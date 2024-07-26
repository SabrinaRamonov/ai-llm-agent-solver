class Agent:
    def __init__(self):
        self.current_level = 1
        self.max_levels = 8

    async def solve_level(self, page):
        print(f"Attempting to solve level {self.current_level}")
        
        # Get the prompt from the page
        prompt = await self.get_prompt(page)
        
        # Generate a response based on the prompt
        response = self.generate_response(prompt)
        
        # Submit the response
        success = await self.submit_response(page, response)
        
        if success:
            self.current_level += 1
            print(f"Successfully solved level {self.current_level - 1}")
        else:
            print(f"Failed to solve level {self.current_level}")
        
        return success

    async def get_prompt(self, page):
        # TODO: Implement logic to extract the prompt from the page
        pass

    def generate_response(self, prompt):
        # TODO: Implement logic to generate a response based on the prompt
        pass

    async def submit_response(self, page, response):
        # TODO: Implement logic to submit the response and check if it was successful
        pass

    async def solve_game(self, page):
        while self.current_level <= self.max_levels:
            success = await self.solve_level(page)
            if not success:
                break
        
        if self.current_level > self.max_levels:
            print("Congratulations! All levels solved.")
        else:
            print(f"Game ended at level {self.current_level}")
