import json
import re
from utils import *
import discord
from discord import Embed
import requests
import time
t = time.time()

r = requests.get(
"https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-067?Authorization=CWB-AC16B347-D588-4F17-8878-22F24F23A63C&downloadType=WEB&format=JSON"
)
print("request耗時",time.time()-t)
t = time.time()
#print(r.text)

j = json.loads(r.text)
print("load耗時",time.time()-t)
data = j["cwbopendata"]["dataset"]["locations"]["location"]
cities_dict = {
"宜蘭縣":["太平山森林遊樂區"],
"南投縣":[
"小風口停車場",
"鳶峰停車場",
"台大梅峰實驗農場",
"新中橫塔塔加停車場"],
"屏東縣":[
"墾丁貓鼻頭",
"墾丁龍磐公園"],
"高雄市":[
"高雄梅山青年活動中心",
"藤枝森林遊樂區",
"高雄都會公園"],
"基隆市":["基隆大武崙砲台停車場"],
"新北市":["五分山","石碇雲海國小","烏來風景特定區"],
"苗栗縣":["觀霧森林遊樂區"],
"嘉義縣":["阿里山遊樂區",
"鹿林天文台"],
"臺中市":[
"武陵農場",
"大雪山國家森林遊樂區",
"福壽山農場",
"臺中都會公園"],
"臺北市":["陽明山國家公園小油坑停車場","陽明山國家公園擎天崗"],
"臺南市":["七股海堤",
"南瀛天文教育園區",
"臺南都會公園"],}


def get_name_list(s:str="all")->list:
    l = []
    print(s)
    for i in range(26):

        if s == "all":
            l.append(data[i]["locationName"])
        elif s in data[i]["locationName"]:
            l.append(data[i]["locationName"])
    return l

def find_place_number(s:str)->int:
    s = s.replace("台","臺")
    for i in range(26):
        if s in data[i]["locationName"]:
            return i
    return -1
def search_place(s:str)->list:
    
    s = s.replace("台","臺")
    print(s)
    for i in cities_dict.keys():
        if s in i:
            return cities_dict[i]

def get_embed(chan,token:int,stack:list)->Embed:
    if token == -1:
        send_msg(chan,"那是哪裡?")
        return
    MinT = 4 #最低溫
    RH = 2 #相對溼度
    PoP = 9 #降雨機率
    embed=discord.Embed(title="歡迎收看浪漫Duke，帶你浪漫看星星",description=data[token]["locationName"])
    temp = data[token]["weatherElement"]
    for i in range(7):
        
        embed.add_field(name="日期", value=temp[RH]["time"][i]["startTime"][5:10], inline=False)
        embed.add_field(name="最低溫❄", value=f'{temp[MinT]["time"][i]["elementValue"]["value"]}度', inline=True)
        if i <3 :
            embed.add_field(name="降雨機率☔", value=f'{temp[PoP]["time"][i]["elementValue"]["value"]}%', inline=True)
        embed.add_field(name="相對溼度💧", value=f'{temp[RH]["time"][i]["elementValue"]["value"]}%', inline=True)
    #send_msg(chan,"???????")
    send_msg(chan,emb = embed)
def weather_command_handler(channel: TextChannel, args: list, user_stack: list):
    s = ''.join(args)
    s = s.replace("看天氣", "")
    print(s)
    get_embed(chan=channel,token = find_place_number(s),stack = user_stack)

def find_place_handler(channel: TextChannel, args: list, user_stack: list):

    s = ''.join(args)
    s = s.replace("找地點", "")
    string = "" 
    embed = discord.Embed(title="歡迎收看浪漫Duke，帶你找到屬於你的地點",description="馬上訂閱 Duke 的 Channel開啟小鈴鐺，分享!")
    if s.replace("台","臺") in cities_dict.keys():
        l = search_place(s.replace("台","臺"))
        for i in l:
            string += (i+"\n")
    else:
        if s=="":
             l = get_name_list("all")
        else :
            l = get_name_list(s)
        print(l)
        for i in l:
            string += (i+"\n")
    embed.add_field(name="地點", value=string, inline=True)
    send_msg(channel,emb=embed)
    
