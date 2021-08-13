import asyncio
from discord import *

def send_msg(ch: TextChannel, text: str):
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(ch.send(text), loop)


def print_help(ch: TextChannel):
    send_msg(ch, 'Need help?')


def say_hello(channel: TextChannel, args=[]):
    send_msg(channel, '歡迎收看 浪漫 Duke ! 想學更多浪漫技巧記得訂閱我的 channel ，開啟小鈴鐺，分享！浪漫 Duke 幫你找回屬於你的浪漫')