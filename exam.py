# 沒意義的註解
#測試2
#引入pandas 作為分析的工具(以pd表示)
  
import pandas as pd
import re
from utils import *
import discord
single108 = pd.read_csv("data/108單科.csv")
mult108 = pd.read_csv("data/108多科.csv")
single109 = pd.read_csv("data/109單科.csv")
mult109 = pd.read_csv("data/109多科.csv")
single110 = pd.read_csv("data/110單科.csv")
mult110 = pd.read_csv("data/110多科.csv")
ntu109 = pd.read_csv("data/台大109.csv")
class ExamInternalState:
    def run(self, message: Message, user_stack: list):
        s = message.content
        l = [s]
        if processingQuerySubjects(s) !='' and processingQueryScore(s) != -1:
          exam_command_handler(message.channel, l,list)
        else:
           embed = Embed(
               title='你懂什麼是浪漫嗎？',
               description='你這樣亂回我訊息是浪漫嗎？'
           )
           embed.set_image(url='https://i.imgur.com/JB3Xx7U.jpg')

           send_msg(message.channel,emb=embed)


    def require_input(self):
        return True
def exam_command_handler(channel: TextChannel, args: list, user_stack: list):
    s = listToString(args)
    if processingQuerySubjects(s) =='':
      user_stack.append(ExamInternalState())
      embed = Embed(
          title='我真的不知道怎麼辦',
          description='講你要查的科目還有級分，我又不會通靈\n 來 再輸一次'
      )
      embed.set_image(url='https://i.imgur.com/D98CN5s.jpg')
      send_msg(channel,emb=embed)
      return
    if processingQueryScore(s) == -1:
      user_stack.append(ExamInternalState())
      embed = Embed(
          title='你懂什麼是浪漫嗎？',
          description='你這樣亂回我訊息是浪漫嗎？'
      )
      embed.set_image(url='https://i.imgur.com/JB3Xx7U.jpg')
      send_msg(channel,emb=embed)
      return

    random.seed(time.time())
    if random.choice([True, False]):
        send_ad(channel, '找到最浪漫的落點')
    embed=discord.Embed(title="歡迎收看浪漫Duke，幫你找到屬於你的落點", color=0xffb8f7)
    embed.set_author(name="浪漫Duke", icon_url="https://media.discordapp.net/attachments/874841739792355363/876105436275826708/unknown.png")
    embed.add_field(name="累積人數:", value=f'{get(processingQuerySubjects(s),processingQueryScore(s))}\n', inline=False)
    embed.add_field(name="109年對應級分", value=f'{search(109,processingQuerySubjects(s),get(processingQuerySubjects(s),processingQueryScore(s)))}\n', inline=True)
    embed.add_field(name="108年對應級分", value=f'{search(109,processingQuerySubjects(s),get(processingQuerySubjects(s),processingQueryScore(s)))}\n', inline=True)

    send_msg(channel,emb=embed)
#查校系(目前只有寫109的NTU))))
def major_command_handler(channel: TextChannel, args: list, user_stack: list):
    # duke 查學冊 123 456
    s = listToString(args).replace(" ","").replace(args[0], "")
    if len(s) == 0:
      embed = Embed(
          title='你懂什麼是浪漫嗎？',
          description=f'你這樣亂回我訊息是浪漫嗎？請在{args[0]}後面加上你要查的校系'
      )
      embed.set_image(url='https://i.imgur.com/JB3Xx7U.jpg')
      send_msg(channel,emb=embed)
      return
    print(s)
    random.seed(time.time())
    if random.choice([True, False]):
        send_ad(channel, '考上第一志願')
    embed=discord.Embed(title="歡迎收看浪漫Duke，幫你找到屬於你的落點", description="--目前為demo板，只有用出台大109年的資料",color=0xffb8f7)
    embed.set_author(name="浪漫Duke", icon_url="https://media.discordapp.net/attachments/874841739792355363/876105436275826708/unknown.png")
    con = ntu109["系"].str.contains(s)
    data = ntu109[con]
    print(data.shape[0])
    if data.shape[0] == 0:
      #blob:https://imgur.com/058a7564-b476-4905-ab0b-780aed43296f
      embed = Embed(
          title='你查的校系不夠浪漫，Duke沒聽過！',
          description=f'找不到對應的校系'
      )
      embed.set_image(url='https://i.imgur.com/JB3Xx7U.jpg')
      send_msg(channel,emb=embed)
      return
    for i in range(data.shape[0]):
      seri = data.iloc(0)[i]
      embed.add_field(name="代碼", value=f'{seri[0]}', inline=False)
      embed.add_field(name="校系", value=f'{seri[1]}', inline=False)
      embed.add_field(name="人數", value=f"{seri[2]}", inline=True)  
      embed.add_field(name="篩選1", value=f"{seri[3]}\n{get109(processingQuerySubjects(seri[3]),processingQueryScore(seri[3]))}", inline=True)
      embed.add_field(name="篩選2", value=f"{seri[4]}\n{get109(processingQuerySubjects(seri[4]),processingQueryScore(seri[4]))}", inline=True) 
      embed.add_field(name="篩選3", value=f"{seri[5]}\n{get109(processingQuerySubjects(seri[5]),processingQueryScore(seri[5]))}", inline=True) 
      embed.add_field(name="篩選4", value=f"{seri[6]}\n{get109(processingQuerySubjects(seri[6]),processingQueryScore(seri[6]))}", inline=True) 
      embed.add_field(name="有無超額比序", value=f"{seri[7]}", inline=True)
     
    embed.add_field(name="會不會上?", value=f'在浪漫的世界裡沒有會上不會上，\n 只有今年上和以後上', inline=False)

    send_msg(channel,emb=embed)

def processingQuerySubjects(s:str)->str:
    '''
    turn s into inorder subject string
    order 國英數自社
    '''
    reString = ""
    if "國" in s:
        reString += "國"
    if "英" in s:
        reString += "英"
    if "數" in s:
        reString += "數"
    if "自" in s:
        reString += "自"
    if "社" in s:
        reString += "社"
    return reString

def processingQueryScore(s:str) -> int:
    '''
    找到字串中的級分
    '''
    score = re.sub("\D","",s)
    if score == "":
      return -1
    if int(score) < 0:
      return -1
    if int(score) > len(processingQuerySubjects(s))*15:
      return -1
    return int(score)

def get(s:str,score:int) ->int:
    if score == -1:
      return
    '''
    回傳累積人數
    '''
    if len(s) == 1:
        return int(single110[s][15-score])
    elif len(s) <= 4:
        return int(mult110[s][(len(s)*15)-score])
def get109(s:str,score:int) ->str:

    '''
    回傳累積人數
    '''
    if score == -1:
      return ""
    if len(s) == 1:
        return f'累積人數:{int(single109[s][15-score])}'
    elif len(s) <= 4:
        return f'累積人數:{int(mult109[s][(len(s)*15)-score])}'
def listToString(s): 
    
    # initialize an empty string
    str1 = " " 
    
    # return string  
    return (str1.join(s))
        
def correspond(subject:str,acl:int) -> str:
    result = ""
    result += search(108,subject,acl)
    result += search(109,subject,acl)
    return result
    
def search(year:int,subject:str,alc:int)->str:
    #result = f'{year}年對應到的級分為'
    result = ""
    if year == 108:
        if len(subject) == 1:
            condition = single108[subject] <= alc
            score = (15 -(single108[condition].shape[0]))
            result += f'{score}\n'
            
            condition2 = single108[subject] <= alc-1000
            closescore =  ((len(subject)*15)-int(single108[condition2].shape[0]))
            if score != closescore:
                result += f'相當接近{closescore}級分(累積人數差不到1000)\n'
                
            
            
        else:
            condition = mult108[subject] <= alc
            score = ((len(subject)*15)-int(mult108[condition].shape[0]))
            result += f'{score}級分\n'
            condition2 = mult108[subject] <= alc-1000
            closescore =  ((len(subject)*15)-int(mult108[condition2].shape[0]))
            if score != closescore:
                result += f'相當接近{closescore}級分(累積人數差不到1000)     '
            #result += 15*len(subject) - int(mult108[condition].shape[0])
    if year == 109:
        if len(subject) == 1:
            condition = single109[subject] <= alc
            score = (15 -int(single109[condition].shape[0]))
            result += f'{score}\n'
            
            condition2 = single109[subject] <= alc-1000

            closescore =  ((len(subject)*15)-int(single109[condition2].shape[0]))
            if score != closescore:
                result += f'相當接近{closescore}級分(累積人數差不到1000)\n'
                
            
            
        else:
            condition = mult109[subject] <= alc
            score = ((len(subject)*15)-int(mult109[condition].shape[0]))
            result += f'{score}級分\n'
            condition2 = mult109[subject] <= alc-1000
            closescore =  ((len(subject)*15)-int(mult109[condition2].shape[0]))
            if score != closescore:
                result += f'相當接近{closescore}級分(累積人數差不到1000)\n'
            #result += 15*len(subject) - int(mult108[condition].shape[0])
            
    return result
            
