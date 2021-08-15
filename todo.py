from utils import *
from discord import Guild, Message, TextChannel
import xml.etree.ElementTree as ET

todo_data = ET.parse('data/todo_states.xml')
todo_root = todo_data.getroot()

user_todo_list = {}
todo_correspondence = {"名稱":0, "截止日期與時間":1, "重要程度":2, "其他資訊":3}

'''
[name, end_datetime, priority, notes]
排序1: 依end_datetime排序
排序2: 依priority排序  >> sorted(todo_list, key=lambda todo_list:todo_list[2], reverse=True)

type:
input  接下來使用者輸入即為該child.attrib['name']資訊
todo_list 顯示todo_list name選單
print_todo_list embed該使用者所有待辦事項
button 1~10 button

在按"新增/編輯完成"前
持續傳送"請選擇todo功能"

bonus:
通知
read google calendar
todo list/event
'''

def get_todo_list(user) -> list:
    if not user in user_todo_list:
        user_todo_list[user] = [[]]
    return user_todo_list[user]

def print_user_todo_list(user):
    todo_list = get_todo_list(user)
    if todo:
        # TBD 排序->embed
        pass
    else:
        TextChannel.send("無待辦事項")
  

class TodoState:
    def __init__(self, cur_node: ET.Element, inter=None) -> None:
        self.node = cur_node
        displays = []
        options = {}
        for child in self.node:
            if child.tag == 'display':
                displays.append(child.text)
                if child.attrib['type'] == 'input':
                    # TBD
                    pass
                elif child.attrib['type'] == 'todo_list':
                    # TBD
                    pass
                elif child.attrib['type'] == 'print_todo_list':
                    # TBD
                    pass
                elif child.attrib['type'] == 'button':
                    # TBD
                    pass
            elif child.tag == 'node':
                options[child.attrib['name']] = child
        
        self.displays = displays
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
            user_stack.append(MenuState('選單：', options, self.selected_handler))

        self.displays = self.displays[::-1]
        if len(self.displays) > 0:
            first_display = None
            if self.inter != None:
                first_display = self.displays.pop()
            for display in self.displays:
                user_stack.append(PrintState(display))
            if first_display != None:
                user_stack.append(PrintState(first_display, inter=self.inter))

    def require_input(self):
        return False
    
def todo_command_handler(channel: TextChannel, args: list, user_stack: list):
    user_stack.append(TodoState(todo_root))
