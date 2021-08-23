import asyncio
from datetime import timedelta
import random
import time
from typing import Callable
from discord import *
from dislash import MessageInteraction, SelectMenu, SelectOption


def send_msg(destination, text='', emb=None):
    loop = asyncio.get_event_loop()
    asyncio.run_coroutine_threadsafe(destination.send(text, embed=emb), loop)


def send_ad(destination, want=''):
    random.seed(time.time())
    ad_contexes = [f'''
想知道如何{want}嗎？馬上訂閱 Duke 的 Channel
開啟小鈴鐺🔔
分享!
💖浪漫 Duke 帶你找回屬於你的浪漫！💖
''',
f'''
各位觀眾，如果你遇到一樣的情況
只要訂閱 Duke 的 Channel
開啟小鈴鐺🔔
分享!
Duke 就教你們如何{want}!
''',
f'''
各位觀眾，不要慌張
只要訂閱 Duke 的 Channel
開啟小鈴鐺🔔
分享!
浪漫 Duke 保證教你們怎麼{want}!
''',
f'''
想學更多{want}的浪漫技巧嗎？
歡迎訂閱 Duke 的 Channel
開啟小鈴鐺🔔
分享!
浪漫 Duke 保證教你們怎麼{want}!
''',
f'''
各位觀眾，關於如何{want}這類型的問題
請訂閱 Duke 的 Channel
開啟小鈴鐺🔔
以及分享!
💖浪漫 Duke 幫你找回屬於你的浪漫！💖
''',
f'''
Duke 之所以一直推廣💖浪漫💖這件事
是因為 Duke 覺得
這個時代 禮崩樂壞！💔
Duke 覺得要回歸英國 18 世紀的那種 紳士風範！
那該怎麼做呢？
只要訂閱 Duke 的 Channel
開啟小鈴鐺🔔
分享!
Duke 就教你們用最優雅的方式{want}!
'''
    ]
    embed = Embed(
        title = '插播一則浪漫廣告',
        description=random.choice(ad_contexes),
        colour=0xed87be
    )
    imgs = [
        'https://assets.zyrosite.com//Yle7bzyK4rSDO7Kl/img-ALpjW0Gk3Rf4WJV6-w800.jpg',
        'https://i.imgur.com/LAuMou5.jpeg',
        'https://i.imgur.com/i4ff0Wp.jpeg',
        'https://i.imgur.com/MOvJG08.jpeg',
        'https://i.imgur.com/g84q6A2.jpeg',
        'https://i.imgur.com/UL9fXwx.jpeg'
    ]
    embed.set_image(url=random.choice(imgs))
    send_msg(destination, emb=embed)

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


def stop_talking(channel: TextChannel, args: list, user_stack: list):
    voice_client = channel.guild.voice_client
    if voice_client and voice_client.is_connected():
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(voice_client.disconnect(), loop)
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


class PlayMusicState:
    def __init__(self, file: str, song_name='神秘的一首歌', play_to=None) -> None:
        self.file = file
        self.name = song_name
        self.play_to = play_to


    async def async_play(self, guild, voice_channel):
        voice_client = guild.voice_client
        if voice_client and voice_client.is_connected():
            await voice_client.move_to(voice_channel)
        else:
            await voice_channel.connect()
            voice_client = guild.voice_client
        
        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(FFmpegPCMAudio(self.file))


    def run(self, message: Message, user_stack=[]):
        target = message.author
        if self.play_to != None:
            target = self.play_to

        if not target.voice or not target.voice.channel:
            send_msg(message.channel, f'{target.mention}尚未連接到任何語音頻道，因此 Duke 無法播放《{self.name}》給你聽 QQ')
            return
        voice_channel = target.voice.channel

        emb = Embed(
            title='為您播放',
            description=self.name,
            color=0xFF95CA
        )
        send_msg(message.channel, emb=emb)
        loop = asyncio.get_event_loop()
        asyncio.run_coroutine_threadsafe(self.async_play(message.guild, voice_channel), loop)


    def require_input(self):
        return False