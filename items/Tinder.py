from items.states import *
from items.ItemBase import ItemBase
from items.ItemManager import add_item
from user_data import get_user_bag


class Tinder(ItemBase):
    pass

add_item('Tinder', '俗人專用', 0, Tinder)