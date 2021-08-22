from items.states import *
from items.ItemBase import ItemBase
from items.ItemManager import add_item
from user_data import get_user_bag


class Temple(ItemBase):
    pass

add_item('月老廟', 'face-to-face的科學浪漫', 20, Temple)