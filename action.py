from user_data import get_user_bag
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


class Golve:
    def acquired():
        embed = Embed(title='紳士決鬥！')
        embed.set_image(url='https://media.githubusercontent.com/media/XYFC128/DukeBot/master/data/gifs/%E7%B4%B3%E5%A3%AB%E6%B1%BA%E9%AC%A5.gif')
        return PrintState(embed=embed)


    def push(channel, user, user_stack: list):
        def check_name(message: Message):
            bag = get_user_bag(user)
            item_amount = 0
            for item in bag:
                if item["item"] == '手套':
                    item_amount = int(item['amount'])
            if len(message.mentions)>0 and len(message.mentions) > item_amount:
                embed = Embed(
                    title='紳士之恥',
                    description=f'{user.mention} 你的手套不夠甩爛{len(message.mentions)}個人，Duke 這邊先教訓你個自不量力的紳士'
                )
                embed.set_image(url='https://media.githubusercontent.com/media/XYFC128/DukeBot/master/data/gifs/%E7%B4%B3%E5%A3%AB%E4%B8%9F%E8%87%89.gif')
                send_msg(channel, emb=embed)
            return len(message.mentions)>0 and len(message.mentions) <= item_amount
        

        def wrap_name(msg):
            return msg.mentions
        
        cache = {}
        user_stack.append(DoActionState(cache, Golve.use, user))
        user_stack.append(ActionInputState(cache, "target", check_name, input_wrapper=wrap_name))
        user_stack.append(PrintState("你想要對哪位紳士使用手套？"))


    def use(channel, user, user_stack: list, data):
        target_users = data['target']
        mentions = ' '.join([mem.mention for mem in target_users])
        emb = Embed(
            title='決鬥啦'
        )
        emb.set_image(url='https://cdn.discordapp.com/attachments/871443577400606736/877058248996450304/a748b4f5a3e97d10.gif')
        bag = get_user_bag(user)
        item_amount = 0
        for item in bag:
            if item["item"] == '手套':
                item_amount = int(item['amount'])
                item_amount -= len(target_users)
                item['amount'] = item_amount
        user_stack.append(PrintState(f'{mentions} 聽好了！{user.mention} 對你使用手套，狠狠的賞了你一巴掌！\n {user.display_name}剩下{item_amount}雙手套', embed=emb))

actions = {
    "手套": Golve
}

def run_action(channel, user, act_name, user_stack):
    actions[act_name].push(channel, user, user_stack)

def action_exist(act_name):
    return act_name in actions


def got_action(act_name):
    if action_exist(act_name):
        return actions[act_name].acquired()
    return None