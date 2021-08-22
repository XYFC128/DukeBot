from items.ItemBase import ItemBase


items = {}


def add_item(name: str, description: str, price: int, item_class: ItemBase):
    if issubclass(item_class, ItemBase):
        items[name] = {}
        it = items[name]
        it['name'] = name
        it['description'] = description
        it['price'] = price
        it['class'] = item_class


def get_all_items(sort=False):
    if sort:
        return sorted(items.values(), key=lambda x: x['price'])
    else:
        return items.values()


def get_item_by_name(name):
    if item_exist(name):
        return items[name]
    return None


def use_item(channel, user, item_name, user_stack):
    items[item_name]['class'].init_user_stack(channel, user, user_stack)


def item_exist(name):
    return name in items


def got_item(name):
    if item_exist(name):
        return items[name]['class'].acquired()
    return None