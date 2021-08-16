#!/usr/bin/python3
from star import *
from utils import *
from romantic import *
from exam import *
from todo import *
from discord import Guild, Message, TextChannel
from discord.ext import commands
from dislash import InteractionClient

import os

user_stacks = {}
def get_user_stack(user) -> list:
    if not user.id in user_stacks:
        user_stacks[user.id] = []

    return user_stacks[user.id]


def clear_no_input_states(message: Message, stack: list):
    if len(stack) == 0:
        return

    while len(stack) > 0 and not stack[-1].require_input():
        cur_state = stack.pop()
        cur_state.run(message, stack)

    if not isinstance(stack, list):
        stack = [stack]


def main_command_handler(message: Message):
    """
    Handle command
    """

    command_handlers = {
        'hello' : say_hello,
        '說你好' : say_hello,
        'STFU': clear_stack,
        '閉嘴': clear_stack,
        '教我' : romantic_command_handler,
        '查學測' : exam_command_handler,
        '查校系' : major_command_handler,
        'todo' : todo_command_handler,
        '看天氣' : weather_command_handler,
        '找地點': find_place_handler
        'todo' : todo_command_handler
    }
    cmds = message.content.split(' ')
    if len(cmds) < 2 or not cmds[1] in command_handlers:
        print_help(message.channel, message.author, command_handlers)
    else:
        hdlr = command_handlers[cmds[1]]
        stack = get_user_stack(message.author)
        todo_list = get_todo_list(message.author)
        hdlr(message.channel, cmds[1:], stack)
        clear_no_input_states(message, stack)


def user_msg_handler(message: Message):
    """
    Main state loop
    """
    user = message.author
    stack = get_user_stack(user)
    todo_list = get_todo_list(message.author)
    if len(stack) == 0:
        return

    cur_state = stack.pop()
    cur_state.run(message, stack)

    clear_no_input_states(message, stack)


bot = commands.Bot(command_prefix='$')
slash = InteractionClient(bot)

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


@slash.event
async def on_dropdown(inter: MessageInteraction):
    user = inter.author
    stack = get_user_stack(user)
    handler = get_handler(inter.message)
    if handler != None:
        handler(inter, stack)
        clear_no_input_states(inter.message, stack)


with open('token.txt', 'r') as f:
    bot.run(f.read())
