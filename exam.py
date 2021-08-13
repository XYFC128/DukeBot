# 沒意義的註解
#測試2

import pandas as pd
import re

single108 = pd.read_csv("108單科.csv")
mult108 = pd.read_csv("108多科.csv")
single109 = pd.read_csv("109單科.csv")
mult109 = pd.read_csv("109多科.csv")
single110 = pd.read_csv("110單科.csv")
mult110 = pd.read_csv("110多科.csv")

 

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
    return reString;

def processingQueryScore(s:str) -> int:
    '''
    找到字串中的級分
    '''
    return eval(re.sub("\D","",s))

def get(s:str,score:int) ->int:

    '''
    回傳累積人數
    '''
    if len(s) == 1:
        return int(single110[s][15-score])
    elif len(s) <= 4:
        return int(mult110[s][(len(s)*15)-score])
        
def correspond(subject:str,acl:int) -> str:
    result = ""
    result += search(108,subject,acl)
    result += search(109,subject,acl)
    return result
    
def search(year:int,subject:str,alc:int)->str:
    result = f'{year}年對應到的級分為'
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
            
