from utils import *
import json
import xml.etree.ElementTree as ET

roman_data = ET.parse('data/romantic_states.xml')
root = roman_data.getroot()

class RomanticState:
    def __init__(self, cur_node: ET.Element, inter=None) -> None:
        self.node = cur_node
        displays = []
        options = {}
        for child in self.node:
            if child.tag == 'display':
                if child.attrib['type'] == 'normal':
                    displays.append(child.text)
            elif child.tag == 'node':
                options[child.attrib['name']] = child
        
        self.displays = displays
        self.options = options
        self.inter = inter

    def selected_handler(self, inter, stack):
        selected = [option.label for option in inter.select_menu.selected_options]
        ans = selected[0]
        node = self.options[ans]
        stack.append(RomanticState(node, inter))


    def run(self, message: Message, user_stack: list):
        if len(self.options) > 0:
            options = [opt for opt in self.options]
            user_stack.append(MenuState('輸入選單：', options, self.selected_handler))

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


def romantic_command_handler(channel: TextChannel, args: list, user_stack: list):
    user_stack.append(RomanticState(root))