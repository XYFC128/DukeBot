from items.states import *
from items.ItemBase import ItemBase
from items.ItemManager import add_item
from user_data import get_user_bag


class Golve(ItemBase):
    def acquired():
        embed = Embed(title='紳士決鬥！')
        embed.set_image(url='https://media.githubusercontent.com/media/XYFC128/DukeBot/master/data/gifs/%E7%B4%B3%E5%A3%AB%E6%B1%BA%E9%AC%A5.gif')
        return PrintState(embed=embed)


    def init_user_stack(channel, user, user_stack: list):
        def check_name(message: Message):
            bag = get_user_bag(user)
            item_amount = 0
            for item in bag:
                if item["item"] == '手套':
                    item_amount = int(item['amount'])
            if len(message.mentions)>0 and len(message.mentions) > item_amount:
                embed = Embed(
                    title='紳士之恥',
                    description=f'{user.mention} 你的手套不夠甩爛{len(message.mentions)}個人，Duke 這邊先教訓你個自不量力的紳士'
                )
                embed.set_image(url='https://media.githubusercontent.com/media/XYFC128/DukeBot/master/data/gifs/%E7%B4%B3%E5%A3%AB%E4%B8%9F%E8%87%89.gif')
                send_msg(channel, emb=embed)
            return len(message.mentions)>0 and len(message.mentions) <= item_amount
    

        def wrap_name(msg):
            return msg.mentions


        cache = {}
        user_stack.append(DoActionState(cache, Golve.use, user))
        user_stack.append(ActionInputState(cache, "target", check_name, input_wrapper=wrap_name))
        user_stack.append(PrintState("你想要對哪位紳士使用手套？"))


    def use(channel, user, user_stack: list, data):
        target_users = data['target']
        mentions = ' '.join([mem.mention for mem in target_users])
        emb = Embed(
            title='決鬥啦'
        )
        emb.set_image(url='https://cdn.discordapp.com/attachments/871443577400606736/877058248996450304/a748b4f5a3e97d10.gif')
        bag = get_user_bag(user)
        item_amount = 0
        for item in bag:
            if item["item"] == '手套':
                item_amount = int(item['amount'])
                item_amount -= len(target_users)
                item['amount'] = item_amount
        user_stack.append(PrintState(f'{mentions} 聽好了！{user.mention} 對你使用手套，狠狠的賞了你一巴掌！\n {user.display_name}剩下{item_amount}雙手套', embed=emb))

add_item('手套', '紳士決鬥時使用', 5, Golve)