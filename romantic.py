from utils import *
import json

romantic_data = None
with open('data/romantic_states.json', 'r') as f:
    romantic_data=json.loads(f.read())


def step_options(anwser: str, stack: list):
    new_options = romantic_data[anwser]['options']
    display = romantic_data[anwser]['print']
    if len(new_options) > 0:
        stack.append(RomanticInternalState(new_options))
        display += '\n你可以輸入: '
        for opt in  new_options:
            display += '\n' + opt
    stack.append(PrintState(display))


class RomanticInternalState:
    def __init__(self, options: list) -> None:
        self.options = options
    
    
    def run(self, message: Message, user_stack: list):
        anwser = message.content
        if anwser in self.options:
            step_options(anwser, user_stack)
        else:
            user_stack.append(self)
            user_stack.append(PrintState("請重新輸入"))


    def require_input(self):
        return True


def romantic_command_handler(channel: TextChannel, args: list, user_stack: list):
    step_options("問題類型", user_stack)