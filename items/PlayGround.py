from items.states import *
from items.ItemBase import ItemBase
from items.ItemManager import add_item
from user_data import get_user_bag


class PlayGround(ItemBase):
    pass

add_item('操場', 'Duke小時候跑的操場', 10, PlayGround)