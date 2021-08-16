from utils import *
from discord import Guild, Message, TextChannel
import xml.etree.ElementTree as ET
import numpy as np
from datetime import *

todo_data = ET.parse('data/todo_states.xml')
todo_root = todo_data.getroot()

user_todo_list = {}
tmp_todo_list = {}

class TodoState:
    def __init__(self, cur_node: ET.Element, inter=None) -> None:
        self.node = cur_node
        displays = []
        inputs = []
        options = {}
        for child in self.node:
            if child.tag == 'display':
                # displays.append(child.text)
                if child.attrib['type'] == 'normal':
                    displays.append(child.text)
                elif child.attrib['type'] == 'embed' and child.text == 'print all':
                    displays.append(child.text)
            elif child.tag == 'input':
                inputs.append(child.text)
            elif child.tag == 'node':
                options[child.attrib['name']] = child
        
        self.displays = displays
        self.inputs = inputs
        self.options = options
        self.inter = inter

    def selected_handler(self, inter, stack):
        selected = [option.label for option in inter.select_menu.selected_options]
        ans = selected[0]
        node = self.options[ans]
        stack.append(TodoState(node, inter))
    
    def run(self, message: Message, user_stack: list):
        if len(self.options) > 0:
            options = [opt for opt in self.options]
            user_stack.append(MenuState('請選擇功能：', options, self.selected_handler))

        self.displays = self.displays[::-1]

        if len(self.displays) > 0:
            first_display = None
            if self.inter != None:
                first_display = self.displays.pop()
            for display in self.displays:
                user_stack.append(PrintState(display))
            if first_display != None:
                user_stack.append(PrintState(first_display, inter=self.inter))
        
            
        self.inputs = self.inputs[::-1]
        
        if len(self.inputs) > 0:
            first_txt = None
            if self.inter != None:
                first_txt = self.inputs.pop()
            for txt in self.inputs:
                user_stack.append(InputState(txt))
                user_stack.append(PrintState(txt))
            if first_txt != None:
                user_stack.append(InputState(first_txt, inter=self.inter))
                user_stack.append(PrintState(first_txt, inter=self.inter))  
        

    def require_input(self):
        return False
    
def todo_command_handler(channel: TextChannel, args: list, user_stack: list):
    user_stack.append(TodoState(todo_root))


class InputState:
    def __init__(self, text='', embed=None, inter=None) -> None:
        self.text = text
        self.embed = embed
        self.inter = inter
    
    def run(self, message: Message, user_stack=[]):
        if self.text == "請輸入該待辦事項__名稱__":
            tmp_todo_list[message.author] = []
            tmp_todo_list[message.author].append(message.content)
            print(tmp_todo_list[message.author])
        elif self.text == "請輸入該待辦事項__截止日期與時間__ （格式：yyyy-MM-dd HH:mm）":
            if is_valid_datetime(message.content):
                tmp_todo_list[message.author].append(message.content)
            else:
                user_stack.append(InputState(self.text))
                user_stack.append(PrintState(self.text))
        elif self.text == "請點選該待辦事項__重要程度__ （10最重要）":
            if is_valid_int(int(message.content)):
                tmp_todo_list[message.author].append(message.content)
            else:
                user_stack.append(InputState(self.text))
                user_stack.append(PrintState(self.text))
        elif self.text == "請輸入該待辦事項__其他資訊__ （無限制格式）":
            tmp_todo_list[message.author].append(message.content)
            todo_list = get_todo_list(message.author)
            idx = find_task(tmp_todo_list[message.author][0], todo_list)
            if idx == -1:
                user_todo_list[message.author].append(tmp_todo_list[message.author])
            else:
                user_todo_list[message.author].pop(idx)
                user_todo_list[message.author].append(tmp_todo_list[message.author])
            for i in range(len(user_todo_list[message.author])):
                for j in range(4):
                    print(user_todo_list[message.author][i][j])
                print()
            print()
                     
    def require_input(self):
        return True
    
def find_task(name, todo_list) -> int:
    if not todo_list:
        return -1
    for i in range(len(todo_list)):
        if todo_list[i][0] == name:
            return i
    return -1

def is_valid_datetime(datet):
    try:
        datetime.strptime(datet+':00', '%Y-%m-%d %H:%M:%S')
        return True
    except:
        return False
    
def is_valid_int(priority):
    if isinstance(priority, int) and priority>=0 and priority<=10:
        return True
    else:
        return False
    
def get_todo_list(user) -> list:
    if not user in user_todo_list:
        user_todo_list[user] = []
    return user_todo_list[user]

def print_user_todo_list(message: Message):
    todo_list = get_todo_list(user)
    if todo:
        todo_list = user_todo_list[message.author]
        tasks_name = ''
        tasks_datetime = ''
        tasks_priority = ''
        tasks_notes = ''

        for i in range(len(user_todo_list[message.author])):
            tasks_name += todo_list[i][0]+'\n'
            tasks_datetime += todo_list[i][1]+'\n'
            tasks_priority += todo_list[i][2]+'\n'
            tasks_notes += todo_list[i][3]+'\n'

        embed=discord.Embed(title=message.author.mention+" の todo list")
        embed.add_field(name="名稱", value=tasks_name, inline=True) 
        embed.add_field(name="截止日期與時間", value=tasks_datetime, inline=True)
        embed.add_field(name="重要程度", value=tasks_priority, inline=True)
        embed.add_field(name="其他資訊", value=tasks_notes, inline=True)    

        send_msg(channel,emb =embed)
        # 排序 TBD
    else:
        message.channel.TextChannel.send("無待辦事項")