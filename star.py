import json
import re
from utils import *
import discord
from discord import Embed
import requests
import time
import shutil
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
    embed.set_image(url="https://opendata.cwb.gov.tw/fileapi/opendata/MSC/O-A0058-003.png")
    send_msg(chan,emb = embed)
    temp = data[token]["weatherElement"]
    for i in range(7):
        #temp[RH]["time"][i]["startTime"][5:10]
        if i <3:
            color = set_color(RH=eval(temp[RH]["time"][i]["elementValue"]["value"]),rain = eval(temp[PoP]["time"][i]["elementValue"]["value"]))
        else :
            color = set_color(eval(temp[RH]["time"][i]["elementValue"]["value"]))
        sub_embed = discord.Embed(title=temp[RH]["time"][i]["startTime"][5:10],color=color)
        sub_embed.add_field(name="最低溫❄", value=f'{temp[MinT]["time"][i]["elementValue"]["value"]}度', inline=True)
        if i <3 :
            sub_embed.add_field(name="降雨機率☔", value=f'{temp[PoP]["time"][i]["elementValue"]["value"]}%', inline=True)
        sub_embed.add_field(name="相對溼度💧", value=f'{temp[RH]["time"][i]["elementValue"]["value"]}%', inline=True)
        send_msg(chan,emb = sub_embed)
    #send_msg(chan,"???????")

def set_color(RH:int,rain:int = -1)->int:
    if rain!= -1:
        hum = (RH+rain)/2
    else:
        hum = RH
    if hum >90 :
        return 0x000000
    elif hum >80 :
        return 0x7d7d7d
    elif hum >70:
        return 0xb8b8b8
    elif hum >60:
        return 0xededed
    elif hum >50:
        return 0xffffff
    elif hum >40:
        return 0xffcccc
    elif hum >30:
        return 0xffa8a8
    elif hum >20:
        return 0xf68383d
    elif hum >10:
        return 0xff6b6b       
    else :
        return 0xff4747     
def weather_command_handler(channel: TextChannel, args: list, user_stack: list):
    s = ''.join(args)
    s = s.replace("看天氣", "")
    print(s)
    get_embed(chan=channel,token = find_place_number(s),stack = user_stack)

def find_place_handler(channel: TextChannel, args: list, user_stack: list):
    if random.choice([True, False,False]):
        send_ad(channel, '知道浪漫Duke的私房景點')
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
def weather_filter_handler(channel: TextChannel, args: list, user_stack: list):
    
    s = ''.join(args)
    if random.choice([True, False,False]):
        send_ad(channel, '找到最適合看星星的時機')
    embed=discord.Embed(title="浪漫Duke 幫你找出最棒的時機")
    embed.set_image(url="https://media.discordapp.net/attachments/874841739792355363/876679072724439130/moonface_202108.jpg?width=496&height=609")
    embed.set_footer(text="月象參考圖")
    s = s.replace("天氣篩選", "")
    t = re.sub("\D","",s)
    Threshold = 20
    if len(t)>0:
        Threshold = int(t)
    t = 0
    embed.add_field(name = "濕度閥值",value=Threshold)
    
    for i in range(26):
        #地點
        for j in range(7):
            if int(data[i]["weatherElement"][2]["time"][j]["elementValue"]["value"])<Threshold:
                
                embed.add_field(name=data[i]["locationName"], value=data[i]["weatherElement"][2]["time"][j]["startTime"][5:10], inline=False)
                embed.add_field(name="相對溼度💧", value=data[i]["weatherElement"][2]["time"][j]["elementValue"]["value"], inline=True)
                if j<3:
                    embed.add_field(name="降雨機率☔", value=data[i]["weatherElement"][9]["time"][j]["elementValue"]["value"], inline=True)
                
                t +=1
    if t ==0:
        embed.add_field(name="找不到適合的狀況",value=f"相對濕度皆大於{Threshold}%",inline=False)
    send_msg(channel,emb =embed)
    print(t)
    if t ==0:
        fail_embed=discord.Embed(title="雖然目前沒有適合的時機，但觀星最重要的精華就是要忍耐，忍到那個最佳時機，在這之前絕對絕對都要忍住")
        fail_embed.set_image(url="https://images-ext-2.discordapp.net/external/ZH-jodEJvRwFmOUEgwjerKA5yn_H4O-xr19zenMPIhg/https/i.imgur.com/to1S7ft.jpg?width=660&height=371")
        send_msg(channel,emb =fail_embed)

