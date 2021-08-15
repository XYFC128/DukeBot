
#引入pandas 作為分析的工具(以pd表示)
  
import pandas as pd
import re
from utils import *
import discord
#使用的分析資料
single108 = pd.read_csv("data/108單科.csv")
mult108 = pd.read_csv("data/108多科.csv")
single109 = pd.read_csv("data/109單科.csv")
mult109 = pd.read_csv("data/109多科.csv")
single110 = pd.read_csv("data/110單科.csv")
mult110 = pd.read_csv("data/110多科.csv")
#檢查輸入並發送級分訊息
def exam_command_handler(channel: TextChannel, args: list, user_stack: list):
    s = listToString(args)
    if processingQuerySubjects(s) =='':
      user_stack.append(PrintState("講你要查的科目還有級分，我又不會通靈"))
      return
    if processingQueryScore(s) == -1:
      user_stack.append(PrintState("輸入正常的級分，這樣Duke才有辦法幫你"))
      return

    
    embed=discord.Embed(title="歡迎收看浪漫Duke，幫你找到屬於你的落點", color=0xffb8f7)
    embed.set_author(name="浪漫Duke", icon_url="https://media.discordapp.net/attachments/874841739792355363/876105436275826708/unknown.png")
    embed.add_field(name="累積人數:", value=f'{get(processingQuerySubjects(s),processingQueryScore(s))}\n', inline=False)
    embed.add_field(name="109年對應級分", value=f'{search(109,processingQuerySubjects(s),get(processingQuerySubjects(s),processingQueryScore(s)))}\n', inline=True)
    embed.add_field(name="108年對應級分", value=f'{search(109,processingQuerySubjects(s),get(processingQuerySubjects(s),processingQueryScore(s)))}\n', inline=True)

    user_stack.append(PrintState(embed=embed))
#提取出科目的部分
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

    '''
    回傳累積人數
    '''
    if len(s) == 1:
        return int(single110[s][15-score])
    elif len(s) <= 4:
        return int(mult110[s][(len(s)*15)-score])
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
            
