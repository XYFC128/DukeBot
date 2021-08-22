import json
import os


users = {}
data_file = 'data/user_data.json'

def init_user(user):
    user_id = str(user.id)
    users[user_id] = {}
    data = users[user_id]
    data['name'] = user.name
    data['stack'] = []
    data['wallet'] = 0
    data['bag'] = []


def user_exist(user):
    return str(user.id) in users


def get_all_users():
    return users


def get_user_stack(user):
    id = str(user.id)
    if not user_exist(user):
        init_user(user)
    return users[id]['stack']


def get_user_bag(user):
    id = str(user.id)
    if not user_exist(user):
        init_user(user)
    return users[id]['bag']


def get_user_wallet(user):
    id = str(user.id)
    if not user_exist(user):
        init_user(user)
    return users[id]['wallet']


def set_user_wallet(user, amount):
    id = str(user.id)
    if not user_exist(user):
        init_user(user)
    if isinstance(amount, int) and 0 <= amount:
        users[id]['wallet'] = amount


def load_users_datas():
    if os.path.isfile(data_file):
        with open(data_file, 'r') as f:
            global users
            users = json.load(f)


def save_users_datas():
    '''
    write users datas to disk
    [Warning]:this function is slow, don't call it too often
    '''
    saved_data = {}
    for user_id in users:
        saved_user = users[user_id].copy()
        saved_user['stack'] = []
        saved_data[user_id] = saved_user
    with open(data_file, 'w') as f:
        json.dump(saved_data, f)