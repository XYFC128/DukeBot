import discord
from discord.ext import commands, tasks
from discord import Guild, Message, TextChannel
import os 
import json
import random

from utils import *

mainshop = [
    {"name":"浪漫1","price":100,"description":"這是浪漫1"},
    {"name":"浪漫2","price":1000,"description":"這是浪漫2"},
    {"name":"浪漫3","price":10000,"description":"這是浪漫3"},
    {"name":"浪漫4","price":100000,"description":"這是浪漫4"}]

class MixState:
    def __init__(self) -> None:
        pass

    def run(self, message: Message, args: list, user_stack: list):
        embed = discord.Embed(
        title="歡迎收看浪漫Duke，帶你找到屬於你的浪漫因子",
        url="https://www.youtube.com/channel/UCzjNxGvrqfxL9KGkObbzrmg/about",
        description="馬上訂閱 Duke 的 Channel，開啟小鈴鐺，分享!\n\n想要來點浪漫因子嗎?輸入duke 浪漫因子 🫀吧!想要查看自己擁有多少浪漫因子?輸入duke 存摺吧!\n\n想要讓自己更浪漫嗎?輸入duke 商店來到浪漫商店吧!",
        color=0xFF95CA)
        send_msg(emb=embed)

        if "存摺" == args[1]:
            if open_account(user):
                balance(message)
        if "🫀" == args[1]:
            earn(message)
        if "商店" == args[1]:
            shop(message)

    def require_input(self):
        return False

def get_bank_data():
    with open('mainbank.json','r') as f:
        users = json.load(f)

    return users

def open_account(user):

    users = get_bank_data()

    if str(user.id) in users:
        return True
    else:
        user.send("浪漫存摺建立完成!")
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0

    with open('mainbank.json','w') as f:
        json.dump(users,f)

    return False

def balance(ctx):

    if open_account(ctx.author):

        user = ctx.author

        users = get_bank_data()
        wallet_amt = users[str(user.id)]["wallet"]
        em = discord.Embed(title=f'{ctx.author.name}，這些是你擁有的浪漫因子',color = discord.Color.pink())
        em.add_field(name='浪漫存摺',value=wallet_amt)
        ctx.send(embed=em)

def earn(ctx):

    if open_account(ctx.author):

        user = ctx.author

        users = get_bank_data()
        earnings = random.randrange(11)
        ctx.send(f'{ctx.author.mention}獲得了{earnings}點浪漫因子!!!')
        with open("mainbank.json",'w') as f:
            json.dump(users,f)

def shop(ctx):
    em = discord.Embed(title="浪漫商店")
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name,value=f'{price} | {desc}')
    ctx.send(embed=em)

def mix_command_handler(message: Message, args: list, user_stack: list):
    user_stack.append(MixState())
    
        