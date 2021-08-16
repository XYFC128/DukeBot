import discord
from discord import Guild, Message, TextChannel
import json
import random

from utils import *

user_data = {}
mainshop = [
    {"name":"LINE","price":0,"description":"新新人類所使用的通訊軟體"},
    {"name":"tinder","price":0,"description":"俗人專用"},
    {"name":"手套","price":5,"description":"紳士決鬥時使用"},
    {"name":"操場","price":10,"description":"Duke小時候跑的操場"},
    {"name":"月老廟","price":20,"description":"face-to-face的科學浪漫"},
    {"name":"星星之火","price":50,"description":"足以燎原"},]

class MixState:
    def __init__(self) -> None:
        pass

    def run(self, message: Message, user_stack: list):
        args = message.content.split(" ")
        user = message.author
        if args[0] != "離開":
            user_stack.append(MixState())
            user_stack.append(PrintState(text="再來啊"))
        if "存摺" == args[0]:
            if open_account(user, user_stack):
                balance(user, user_stack)
        if "🫀" == args[0]:
            if open_account(user, user_stack):
                earn(user, user_stack)
        if "商店" == args[0]:
            shop(user, user_stack)
        if "包包" == args[0]:
            bag(user, user_stack)
        if "買" == args[0] and len(args) == 3:
            if open_account(user, user_stack):
                buy(user, user_stack, args[1], int(args[2]))
        if "排行榜" == args[0] and len(args) == 2:
            leaderboard(user, user_stack, int(args[1]))

    def require_input(self):
        return True

def get_user_data(user):
    if user.id not in user_data:
        user_data[user.id] = {"name": user.name}
    return user_data[user.id]

def open_account(user, user_stack):
    data = get_user_data(user)

    if "wallet" not in data:
        data["wallet"] = 0
        user_stack.append(PrintState(text="浪漫存摺建立完成!"))
        return False
    else:
        return True

def balance(user, user_stack):
    data = get_user_data(user)

    wallet_amt = data["wallet"]
    em = discord.Embed(title=f'{user.name}的浪漫存摺👛', description=f'餘額: {wallet_amt}點', color=0xFF95CA)
    user_stack.append(PrintState(embed=em))

def earn(user, user_stack):
    data = get_user_data(user)

    earnings = random.randrange(11)
    user_stack.append(PrintState(text=f'{user.mention}獲得了{earnings}點浪漫因子!!!'))
    data["wallet"] += earnings

def shop(user, user_stack):
    em = discord.Embed(title="浪漫商店🏩", color= 0xFF95CA)
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name, value=f'{price} | {desc}')
    user_stack.append(PrintState(embed=em))

def bag(user, user_stack):
    data = get_user_data(user)

    if "bag" not in data:
        data["bag"] = []
        em = discord.Embed(title=f'{user.name}的浪漫包包💗', color= 0xFF95CA, description="你的包包空無一物......")
    elif data["bag"] == []: 
        em = discord.Embed(title=f'{user.name}的浪漫包包💗', color= 0xFF95CA, description="你的包包空無一物......")
    else:
        em = discord.Embed(title=f'{user.name}的浪漫包包💗', color= 0xFF95CA, description="")

    bag = data["bag"]    
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        em.add_field(name=name, value=amount)    
    user_stack.append(PrintState(embed=em))

def buy_this(user, item_name, amount):
    data = get_user_data(user)
    
    name = None
    for item in mainshop:
        if item["name"] == item_name:
            name = item["name"]
            price = item["price"]
            break
    if name == None:
        return [False, 1]

    cost = price * amount
    if data["wallet"] < cost:
        return [False, 2]

    item_in_bag = False
    for thing in data["bag"]:
        n = thing["item"]
        if n == item_name:
            new_amt = item["amount"] + amount
            thing["amount"] = new_amt
            item_in_bag = True
            break
    if not item_in_bag:
        data["bag"].append({"item": item_name, "amount": amount})
    
    data["wallet"] -= cost
    return [True, "Done"]   

def buy(user, user_stack, item, amount):
    result = buy_this(user, item, amount)
    if not result[0]:
        if result[1] == 1:
            user_stack.append(PrintState(text="Duke沒有這件商品"))
        if result[1] == 2:
            user_stack.append(PrintState(text=f"你這樣浪漫嗎?妳的浪漫因子無法兌換{amount}個{item}，快去收集浪漫因子吧!"))
    else:
        user_stack.append(PrintState(text=f"恭喜你獲得{amount}個{item}!!!"))

def leaderboard(user, user_stack, n):
    leader_board = {}
    total = []
    for name in user_data:
        amount = user_data[name]["wallet"]
        leader_board[amount] = name
        total.append(amount)
    total = sorted(total, reverse=True)
    if total == []:
        em = discord.Embed(title="浪漫排行榜🏆", description=f"你們這樣浪漫嗎?快去收集浪漫因子吧!", color=0xFF95CA)
    else:
        em = discord.Embed(title="浪漫排行榜🏆", description=f"前{n}名", color=0xFF95CA)
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        name_ = user_data[id_]["name"]
        em.add_field(name=f'{index}. {name_}', value=amt, inline=False)
        if index == n:
            break
        else:
            index += 1
    user_stack.append(PrintState(embed=em))

def mix_command_handler(channel: TextChannel, args: list, user_stack: list):
    user_stack.append(MixState())
    embed = discord.Embed(
            title="歡迎收看浪漫Duke，帶你找回屬於你的浪漫因子",
            url="https://www.youtube.com/channel/UCzjNxGvrqfxL9KGkObbzrmg",
            description="馬上訂閱 Duke 的 Channel，開啟小鈴鐺，分享!\n\n你只要有這個浪漫因子，你做的一舉一動都是浪漫的事\n你只要有了這個浪漫因子，它就是你跟她浪漫之間的一個催化劑\n\n想要來點浪漫因子嗎? 輸入 🫀 吧!\n想要查看自己擁有多少浪漫因子? 輸入 存摺 吧!\n想要更多浪漫嗎? 輸入 商店 來到浪漫商店吧!\n想要看看自己有哪些浪漫道具? 輸入 包包 吧!\n想要購買浪漫Duke的浪漫道具? 輸入 買 <道具名稱> <數量> 吧!\n想要查看排行榜? 輸入 排行榜 <人數> 來顯示前 <人數> 名吧!\n想要離開Duke的服務? 輸入 離開 吧!",
            color=0xFF95CA
            )
    embed.set_image(url="http://i.imgur.com/71YwSHy.jpg")
    user_stack.append(PrintState(embed=embed))