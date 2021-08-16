import asyncio
from typing import Callable
from discord import *
from dislash import MessageInteraction, SelectMenu, SelectOption


def send_msg(destination, text='', emb=None):
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(destination.send(text, embed=emb), loop)


def print_help(ch: TextChannel, user, supported_commands={}):
    send_msg(ch, 
f'''
有請我們的神秘嘉賓~
{user.mention} 這次有什麼事情要委託 Duke 呢?
Duke 目前支援以下幾種指令：
''' + '\n'.join(['duke ' + cmd for cmd in supported_commands]) + '\n'
    )


def say_hello(channel: TextChannel, args=[], user_stack=[]):
    send_msg(channel, '歡迎收看 浪漫 Duke ! 想學更多浪漫技巧記得訂閱我的 channel ，開啟小鈴鐺，分享！浪漫 Duke 幫你找回屬於你的浪漫')


def clear_stack(channel: TextChannel, args: list, user_stack: list):
    user_stack.clear()
    send_msg(channel, "對不起")


connections_table = {}

def connect(message, handler):
    connections_table[message.id] = handler


def disconnect(message):
    if message.id in connections_table:
        del connections_table[message]


def get_handler(message):
    if not message.id in connections_table:
        return None
    return connections_table[message.id]


class PrintState:
    def __init__(self, text='', embed=None, inter=None) -> None:
        self.text = text
        self.embed = embed
        self.inter = inter
    
    
    def run(self, message: Message, user_stack=[]):
        if self.inter != None:
            loop = asyncio.get_event_loop()
            asyncio.run_coroutine_threadsafe(
                self.inter.reply(self.text, embed=self.embed),
                loop
            )
        else:
            send_msg(message.channel, self.text, emb=self.embed)


    def require_input(self):
        return False

class MenuState:
    def __init__(self, text: str, options: list, selection_handler: Callable[[MessageInteraction, list], None], place_holder='請選擇', max_select=1, embed=None,inter=None):
        self.text = text
        self.options = options
        self.selection_handler = selection_handler
        self.place_holder = place_holder
        self.max_select = max_select
        self.embed = embed
        self.inter = inter


    async def async_run(self, message: Message, user_stack):
        sender = message.channel.send
        if self.inter != None:
            sender = self.inter.reply

        msg = await sender(
            self.text, 
            embed=self.embed,
            components=[
                SelectMenu(
                    placeholder=self.place_holder,
                    max_values=self.max_select,
                    options=[SelectOption(option, option) for option in self.options]
                )
            ]
        )
        connect(msg, self.selection_handler)


    def run(self, message: Message, user_stack=[]):
        loop = asyncio.get_event_loop()
        res = asyncio.run_coroutine_threadsafe(self.async_run(message, user_stack), loop)
        

    def require_input(self):
        return False