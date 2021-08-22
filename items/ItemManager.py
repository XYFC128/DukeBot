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
    possible_names = []
    for it_name in items.keys():
        if it_name.startswith(name):
            possible_names.append(it_name)
        elif str(it_name).find(name) != -1:
            possible_names.append(it_name)
    
    if len(possible_names) == 1:
        return items[possible_names[0]]
    
    return None


def use_item(channel, user, item_name, user_stack):
    items[item_name]['class'].init_user_stack(channel, user, user_stack)


def item_exist(name):
    return name in items


def got_item(name):
    item = get_item_by_name(name)
    if item != None:
        return item['class'].acquired()
    return None