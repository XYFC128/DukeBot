from items.states import *
from items.ItemBase import ItemBase
from items.ItemManager import add_item
from user_data import get_user_bag


class Spark(ItemBase):
    pass

add_item('星星之火', '足以燎原', 50, Spark)