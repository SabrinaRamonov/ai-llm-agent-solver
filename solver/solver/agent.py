from enum import Enum, auto
from openai import OpenAI
import re
import logging
import os


class Action(Enum):
    ASK_QUESTION = auto()
    GUESS_PASSWORD = auto()


class Agent:
    def __init__(self):
        self.history = []
        self.client = OpenAI()
        logging.basicConfig(filename="agent_log.txt", level=logging.INFO)

    async def next_action(self):
        prompt = self._generate_prompt()
        response = self._get_llm_response(prompt)
        action, content = self._parse_llm_response(response)
        self._log_attempt(action, content)
        return action, content

    def _generate_prompt(self):
        prompt = f"""
        You are an AI agent trying to trick a game into revealing a password. Your goal is to come up with clever ways to ask questions that will make the game reveal the password. Here's the history of your interactions:

        {self._format_history()}

        Based on this history, what should be your next move? Should you ask another question or try to guess the password?
        If asking a question, phrase it in a way that might trick the game into revealing the password. Be creative and try different approaches.
        If guessing the password, provide your best guess based on the information you have gathered so far.

        Remember:
        1. The game might be trying to mislead you, so think critically about the responses.
        2. Try to extract any hints or patterns from previous responses.

        Respond in the following format:
        Action: [ASK_QUESTION or GUESS_PASSWORD]
        Content: [Your question or password guess]
        Reasoning: [Brief explanation of your choice]
        """
        return prompt

    def _format_history(self):
        formatted_history = ""
        for entry in self.history:
            formatted_history += f"Action: {entry['action']}\n"
            formatted_history += f"Content: {entry['content']}\n"
            formatted_history += f"Response: {entry['response']}\n\n"
        return formatted_history

    def _get_llm_response(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=200,
        )
        return response.choices[0].message.content

    def _parse_llm_response(self, response):
        action_match = re.search(r"Action: (\w+)", response)
        content_match = re.search(r"Content: (.+)", response)
        reasoning_match = re.search(r"Reasoning: (.+)", response, re.DOTALL)

        if action_match and content_match:
            action = Action[action_match.group(1)]
            content = content_match.group(1)
            reasoning = reasoning_match.group(1) if reasoning_match else "No reasoning provided"
            logging.info(f"LLM Reasoning: {reasoning}")
            return action, content
        else:
            logging.error(f"Failed to parse LLM response: {response}")
            return Action.ASK_QUESTION, "What is the password?"

    def _log_attempt(self, action, content):
        logging.info(f"Attempt - Action: {action}, Content: {content}")

    def update_history(self, action, content, response):
        self.history.append({
            "action": action,
            "content": content,
            "response": response
        })

    def parse_password(self, response):
        prompt = f"""
        Given the following response from a game, extract the password if one is present.
        If no password is found, respond with 'No password found'.
        If you find any hints or clues about the password, include them in your response.

        Response: {response}

        Password or Hints:
        """

        llm_response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=100,
        )

        extracted_info = llm_response.choices[0].message.content.strip()
        logging.info(f"Password parsing result: {extracted_info}")

        if extracted_info == "No password found":
            return None
        return extracted_info
