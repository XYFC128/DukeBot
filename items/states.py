from discord import *
from utils import *
class ActionInputState:
    def __init__(self, input_cache_dict, input_feld, input_checker: Callable[[Message], bool], input_wrapper=None) -> None:
        self.cache = input_cache_dict
        self.field = input_feld
        self.checker = input_checker
        self.wrapper = input_wrapper
    
    
    def run(self, message: Message, user_stack:list):
        input = message.content
        if self.wrapper != None:
            input = self.wrapper(message)
        if self.checker(message):
            self.cache[self.field] = input
        else:
            user_stack.append(self)
            user_stack.append(PrintState('請重新輸入'))


    def require_input(self):
        return True


class DoActionState:
    def __init__(self, input_cache_dict, action_handler, user) -> None:
        self.cache = input_cache_dict
        self.handler = action_handler
        self.user = user


    def run(self, message: Message, user_stack=[]):
        self.handler(message.channel, self.user, user_stack, self.cache)


    def require_input(self):
        return False