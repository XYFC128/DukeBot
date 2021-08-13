#!/usr/bin/python3

from utils import *
from romantic import *

from discord import Client, Guild, Message, TextChannel
from discord.ext import commands

import os

def get_user_stack(user) -> list:
    user_stacks = {}
    
    if not user in user_stacks:
        user_stacks[user] = []

    return user_stacks[user]


def clear_no_input_states(message: Message, stack: list):
    if len(stack) == 0:
        return

    while len(stack) > 0 and not stack[-1].require_input():
        cur_state = stack[-1]
        del stack[-1]

        cur_state.run(message, cur_state)


def main_command_handler(message: Message):
    """
    Handle command
    """

    command_handlers = {
        'hello' : say_hello,
        '說你好' : say_hello,
        '找浪漫' : romantic_command_handler
    }
    cmds = message.content.split(' ')
    if len(cmds) < 2 or not cmds[1] in command_handlers:
        print_help(message.channel, message.author, command_handlers)
    else:
        hdlr = command_handlers[cmds[1]]
        stack = get_user_stack(message.author)
        hdlr(message.channel, cmds[1:], stack)
        clear_no_input_states(message, stack)


def user_msg_handler(message: Message):
    """
    Main state loop
    """
    user = message.author
    stack = get_user_stack(user)
    
    if len(stack) == 0:
        return

    cur_state = stack[-1]
    del stack[-1]
    cur_state.run(message, cur_state)

    clear_no_input_states(message, stack)


bot = Client()

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message: Message):
    if message.author == bot.user:
        return

    if message.content.startswith('duke'):
        main_command_handler(message)
    else:
        user_msg_handler(message)

@bot.event
async def on_guild_join(guild : Guild):
    #Duke 加入一個新的伺服器，準備幹話一番
    pass


with open('token.txt', 'r') as f:
    bot.run(f.read())