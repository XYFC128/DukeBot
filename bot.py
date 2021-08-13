#!/usr/bin/python3

from utils import *

from discord import Client, Guild, Message, TextChannel
from discord.ext import commands

import os

def main_command_handler(message: Message):
    """
    Handle command
    """

    command_handlers = {
        'hello' : say_hello,
        '說你好' : say_hello
    }
    cmds = message.content.split(' ')
    if len(cmds) < 2 or not cmds[1] in command_handlers:
        print_help(message.channel, message.author, command_handlers)
    else:
        hdlr = command_handlers[cmds[1]]
        hdlr(message.channel, cmds[1:])

bot = Client()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message: Message):
    message.author.nick
    if message.author == bot.user:
        return

    if message.content.startswith('duke'):
        main_command_handler(message)


@bot.event
async def on_guild_join(guild : Guild):
    #Duke join new server
    pass


with open('token.txt', 'r') as f:
    bot.run(f.read())