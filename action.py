from mix import get_user_data, send
from discord import *
from utils import *

def use_golves(channel, user, user_stack: list, data):
    target_users = data['target']
    mentions = ' '.join([mem.mention for mem in target_users])
    emb = Embed(
        title='決鬥啦'
    )
    emb.set_image(url='https://cdn.discordapp.com/attachments/871443577400606736/877058248996450304/a748b4f5a3e97d10.gif')
    data = get_user_data(user)
    item_amount = 0
    for item in data['bag']:
        print(data['bag'])
        if item["item"] == '手套':
            item_amount = int(item['amount'])
            item_amount -= len(target_users)
            item['amount'] = item_amount
    user_stack.append(PrintState(f'{mentions} 聽好了！{user.mention} 對你使用手套，狠狠的賞了你一巴掌！\n {user.display_name}剩下{item_amount}雙手套', embed=emb))

action_dict = {
    "手套": use_golves
}

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


def push_golves(channel, user, user_stack: list):
    def check_name(message: Message):
        data = get_user_data(user)
        item_amount = 0
        for item in data['bag']:
            print(data['bag'])
            if item["item"] == '手套':
                item_amount = int(item['amount'])
        if len(message.mentions)>0 and len(message.mentions) >= item_amount:
            send_msg(channel, f'{user.mention} 你的手套不夠喔')
        return len(message.mentions)>0 and len(message.mentions) < item_amount
    

    def wrap_name(msg):
        return msg.mentions
    
    cache = {}
    user_stack.append(DoActionState(cache, action_dict["手套"], user))
    user_stack.append(ActionInputState(cache, "target", check_name, input_wrapper=wrap_name))
    user_stack.append(PrintState("你想要對哪位紳士使用手套？"))



push_action_dict = {
    "手套": push_golves
}
def run_action(channel, user, act_name, user_stack):
    push_action_dict[act_name](channel, user, user_stack)