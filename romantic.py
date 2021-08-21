import time
from utils import *
from user_data import get_user_bag
import random
import xml.etree.ElementTree as ET

roman_data = ET.parse('data/romantic_states.xml')
root = roman_data.getroot()

class RomanticState:
    def __init__(self, cur_node: ET.Element, inter=None) -> None:
        self.node = cur_node
        displays = []
        options = {}
        embed = None
        ad = None
        require = None
        for child in self.node:
            if child.tag == 'display':
                displays.append(child.text)
            if child.tag == 'ad':
                ad = child.text
            elif child.tag == 'embed':
                attr = child.attrib
                embed_dict = {}
                for key in attr:
                    if key == 'color':
                        embed_dict[key] = int(attr[key], base=16)
                    else:
                        embed_dict[key] = attr[key]
                
                embed = Embed.from_dict(embed_dict)

                for embed_element in child:
                    attr = embed_element.attrib
                    if embed_element.tag == 'footer':
                        embed.set_footer(text=attr['text'], icon_url=attr['icon_url'])
                    elif embed_element.tag == 'image':
                        embed.set_image(url=attr['url'])
                    elif embed_element.tag == 'thumbnail':
                        embed.set_thumbnail(url=attr['url'])
                    elif embed_element.tag == 'author':
                        embed.set_author(
                            name=attr['name'],
                            url=attr['url'],
                            icon_url=attr['icon_url']
                        )
                    elif embed_element.tag == 'field':
                        inline = True
                        if 'inline' in attr:
                            inline = (attr['inline'].lower() in ['true', '1'])
                        embed.add_field(
                            name=attr['name'],
                            value=attr['value'],
                            inline=inline
                        )

            elif child.tag == 'node':
                options[child.attrib['name']] = child
            elif child.tag == 'require':
                require = child.text
        
        self.display = '\n'.join(displays)
        self.options = options
        self.inter = inter
        self.embed = embed
        self.ad = ad
        self.require = require

    def selected_handler(self, inter, stack):
        selected = [option.label for option in inter.select_menu.selected_options]
        ans = selected[0]
        node = self.options[ans]
        stack.append(RomanticState(node, inter))


    def run(self, message: Message, user_stack: list):
        if self.ad != None:
            random.seed(time.time())
            if random.choice([True, False]):
                send_ad(message.channel, self.ad)

        if self.require != None and self.inter != None:
            bag = get_user_bag(self.inter.author)
            has_required = False
            if len(bag) > 0:
                for item in bag:
                    if item["item"] == self.require and int(item['amount']) > 0:
                        has_required = True
                        break

            if not has_required:
                goal = self.node.attrib['name']
                embed = Embed(
                    title='提示',
                    description=f'想要達成{goal}需要{self.require}喔！趕快輸入 duke 浪漫因子 前往浪漫商店購買吧！',
                    colour=0x00fbff
                )
                user_stack.append(PrintState(embed=embed))


        if len(self.options) > 0:
            options = [opt for opt in self.options]
            user_stack.append(MenuState(self.display, options, self.selected_handler, embed=self.embed, inter=self.inter))
        else:
            user_stack.append(PrintState(self.display, embed=self.embed, inter=self.inter))


    def require_input(self):
        return False


def romantic_command_handler(channel: TextChannel, args: list, user_stack: list):
    user_stack.append(RomanticState(root))