from items.states import *
from items.ItemBase import ItemBase
from items.ItemManager import add_item
from user_data import get_user_bag


class Line(ItemBase):
    pass

add_item('Line', '新新人類所使用的通訊軟體', 0, Line)