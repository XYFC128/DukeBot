import discord
from discord import Guild, Message, TextChannel
import random

from utils import *
from user_data import get_all_users, get_user_bag, get_user_wallet, set_user_wallet
from action import run_action, action_exist, got_action

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
        elif "🫀" == args[0]:
            if open_account(user, user_stack):
                earn(user, user_stack)
        elif "商店" == args[0]:
            shop(user, user_stack)
        elif "包包" == args[0]:
            bag(user, user_stack)
        elif "買" == args[0] and len(args) == 3:
            if open_account(user, user_stack):
                buy(user, user_stack, args[1], int(args[2]))
        elif "賣" == args[0] and len(args) == 3:
            if open_account(user, user_stack):
                sell(user, user_stack, args[1], int(args[2]))
        elif "搶" == args[0] and len(args) == 2 and len(message.mentions) == 1:
            rob(user, user_stack, message.mentions[0])
        elif "送" == args[0] and len(args) == 3 and len(message.mentions) == 1:
            print(args)
            give(user, user_stack, message.mentions[0], args[2])
        elif "排行榜" == args[0] and len(args) == 2:
            leaderboard(user, user_stack, int(args[1]))
        elif "用"  == args[0] and len(args) == 2:
            use(user, user_stack, message.channel, args[1])

    def require_input(self):
        return True


def open_account(user, user_stack):
    '''
    data = get_user_data(user)
    
    if "wallet" not in data:
        data["wallet"] = 0
        user_stack.append(PrintState(text="浪漫存摺建立完成!"))
        return False

    with open('data/user_data.json', 'w') as f:
        json.dump(user_data, f)
    '''

    return True


def balance(user, user_stack):
    wallet_amt = get_user_wallet(user)
    em = discord.Embed(title=f'{user.name}的浪漫存摺👛', description=f'餘額: {wallet_amt}點', color=0xFF95CA)
    user_stack.append(PrintState(embed=em))


def earn(user, user_stack):
    earnings = random.randrange(11)
    user_stack.append(PrintState(text=f'{user.mention}獲得了{earnings}點浪漫因子!!!'))
    wallet = get_user_wallet(user)
    wallet += earnings
    set_user_wallet(user, wallet)


def shop(user, user_stack):
    em = discord.Embed(title="浪漫商店🏩", color= 0xFF95CA)
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name=name, value=f'{price} | {desc}')
    user_stack.append(PrintState(embed=em))


def bag(user, user_stack):
    bag = get_user_bag(user)
    if len(bag) == 0: 
        em = discord.Embed(title=f'{user.name}的浪漫包包💗', color= 0xFF95CA, description="你的包包空無一物......")
    else:
        em = discord.Embed(title=f'{user.name}的浪漫包包💗', color= 0xFF95CA, description="")

    for item in bag:
        name = item["item"]
        amount = item["amount"]
        em.add_field(name=name, value=amount)    
    user_stack.append(PrintState(embed=em))


def buy_this(user, item_name, amount):
    name = None
    for item in mainshop:
        if item["name"] == item_name:
            name = item["name"]
            price = item["price"]
            break
    if name == None:
        return [False, 1]

    wallet = get_user_wallet(user)
    bag = get_user_bag(user)

    cost = price * amount
    if wallet < cost:
        return [False, 2]

    item_in_bag = False
    for thing in bag:
        n = thing["item"]
        if n == item_name:
            new_amt = thing["amount"] + amount
            thing["amount"] = new_amt
            item_in_bag = True
            break
    if not item_in_bag:
        bag.append({"item": item_name, "amount": amount})
    
    wallet -= cost
    set_user_wallet(user, wallet)
    return [True, "Done"]   

def buy(user, user_stack, item, amount=1):
    result = buy_this(user, item, amount)
    if not result[0]:
        if result[1] == 1:
            user_stack.append(PrintState(text="Duke沒有這件商品"))
        if result[1] == 2:
            user_stack.append(PrintState(text=f"你這樣浪漫嗎?妳的浪漫因子無法兌換{amount}個{item}，快去收集浪漫因子吧!"))
    else:
        item_intro = got_action(item)
        if item_intro != None:
            user_stack.append(item_intro)
        user_stack.append(PrintState(text=f"恭喜你獲得{amount}個{item}!!!"))


def sell_this(user, item_name, amount, price=None):
    name = None
    for item in mainshop:
        if item["name"] == item_name:
            name = item["name"]
            if price == None:
                price = int(0.8 * item["price"])
            break
    if name == None:
        return [False, 1]

    bag = get_user_bag(user)

    cost = price * amount
    item_in_bag = False
    for thing in bag:
        n = thing["item"]
        if n == item_name:
            new_amt = thing["amount"] - amount
            if new_amt < 0:
                return [False, 2]

            thing["amount"] = new_amt
            item_in_bag = True
            break
    if not item_in_bag:
        return [False, 3]

    wallet = get_user_wallet()
    wallet += cost
    set_user_wallet(user, wallet)

    return [True, "Done"]


def sell(user, user_stack, item, amount=1):
    result = sell_this(user, item, amount)
    if not result[0]:
        if result[1] == 1:
            user_stack.append(PrintState(text="Duke沒有這件商品"))
        if result[1] == 2:
            user_stack.append(PrintState(text=f"你的包包裡沒有{amount}個{item}，快去浪漫商店買些東西吧!"))
        if result[1] == 3:
            user_stack.append(PrintState(text=f"你的包包裡沒有{item}，快去浪漫商店買些東西吧!"))
    else:
        user_stack.append(PrintState(text=f"你成功賣出了{amount}個{item}"))

def give(user, user_stack, another, amount=0):
    tar_id = another.id
    
    if amount == None:
        user_stack.append(PrintState(text="請輸入你要送出的浪漫因子數量"))
        return
    if amount == 'all':
        amount = get_user_wallet(user)
    amount = int(amount)
    if amount > get_user_wallet(user):
        user_stack.append(PrintState(text="你這樣浪漫嗎?快去收集浪漫因子吧!"))
        return
    elif amount < 0:
        user_stack.append(PrintState(text="你這樣浪漫嗎?請輸入正數!"))
        return

    wallet = get_user_wallet(user)
    set_user_wallet(user, wallet - amount)
    tar_wallet = get_user_wallet(another)
    set_user_wallet(another, tar_wallet + amount)
    user_stack.append(PrintState(text=f"{user.mention}你送給了 {another} {amount} 點浪漫因子!"))


def rob(user, user_stack, another):
    wallet = get_user_wallet(user)
    if wallet < 10:
        user_stack.append(PrintState(text="你懂浪漫嗎?搶劫要付出代價(10點)!"))
        return
    delta = -10

    tar_wallet = get_user_wallet(another)
    if tar_wallet < 10:
        user_stack.append(PrintState(text="他太可憐了，放過他吧"))
        return

    earnings = random.randrange(0, int(tar_wallet / 2))
    delta += earnings 
    set_user_wallet(user, wallet + delta)
    set_user_wallet(another, tar_wallet - earnings)

    if delta >= 0:
        user_stack.append(PrintState(text=f"你花了 {10} 點搶到 {another} 的 {earnings} 個浪漫因子!"))
    else:
        user_stack.append(PrintState(text=f"哈哈笑死，你賠了 {-delta} 個浪漫因子!"))


def leaderboard(user, user_stack, n):
    leader_board = {}
    total = []
    user_data = get_all_users()
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


def use(user, user_stack, channel, item):
    if action_exist(item):
        run_action(channel, user, item, user_stack)


def mix_command_handler(channel: TextChannel, args: list, user_stack: list):
    user_stack.append(MixState())
    embed = discord.Embed(
            title="歡迎收看浪漫Duke，帶你找回屬於你的浪漫因子",
            url="https://www.youtube.com/channel/UCzjNxGvrqfxL9KGkObbzrmg",
            description="馬上訂閱 Duke 的 Channel，開啟小鈴鐺，分享!\n\n你只要有這個浪漫因子，你做的一舉一動都是浪漫的事\n你只要有了這個浪漫因子，它就是你跟她浪漫之間的一個催化劑\n\n想要來點浪漫因子嗎? 輸入 🫀 吧!\n想要查看自己擁有多少浪漫因子? 輸入 存摺 吧!\n想要更多浪漫嗎? 輸入 商店 來到浪漫商店吧!\n想要看看自己有哪些浪漫道具? 輸入 包包 吧!\n想要購買浪漫Duke的浪漫道具? 輸入 買 <道具名稱> <數量> 吧!\n想要賣掉已經購買的商品? 輸入 賣 <道具名稱> <數量> 吧!\n想要搶走別人的浪漫因子? 輸入 搶 <人名> <數量> 來大開殺戒吧!\n想要把浪漫因子送給別人? 輸入 送 <人名> <數量> 吧!\n想要查看排行榜? 輸入 排行榜 <人數> 來顯示前 <人數> 名吧!\n想要離開Duke的服務? 輸入 離開 吧!",
            color=0xFF95CA
            )
    embed.set_image(url="http://i.imgur.com/71YwSHy.jpg")
    user_stack.append(PrintState(embed=embed))