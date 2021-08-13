import asyncio
from discord import *

def send_msg(ch: TextChannel, text: str):
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(ch.send(text), loop)


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


class PrintState:
    def __init__(self, text: str) -> None:
        self.text = text
    
    
    def run(self, message: Message, user_stack=[]):
        send_msg(message.channel, self.text)

    def require_input(self):
        return False
