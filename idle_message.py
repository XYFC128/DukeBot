import json
import discord
from utils import *
json_keyword = ""
f = open('data/idle_message.json',"r",encoding="utf-8")
  
# returns JSON object as 
# a dictionary
json_keyword = json.load(f)
keyword = ["浪漫","英雄聯盟","功課","跑操場","跑步", "Line","科學","道德","衝刺"]

def keyword_command_handler(message):
    for i in keyword:
        if i in message.content:
            f=""
            for j in json_keyword["keyword"][i]:
                f += j+"\n"
                
            
            embed = discord.Embed(title=f"有人提到{i}嗎?",description=f)
            embed.set_author(name="浪漫Duke", icon_url="https://media.discordapp.net/attachments/874841739792355363/876105436275826708/unknown.png")
            send_msg(message.channel,emb = embed)
            return 

