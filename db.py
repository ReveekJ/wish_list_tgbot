import sqlite3 as sql
from DEBUG.DEBUG import DEBUG


def create_user_db():
    global db_name
    con = sql.connect(f'{db_name}.db', detect_types=sql.PARSE_DECLTYPES | sql.PARSE_COLNAMES)

    with con:
        con.execute(f'''CREATE TABLE IF NOT EXISTS {db_name} (
                            groups_name TEXT,
                            users TEXT,
                            wish TEXT,
                            leader_id INTEGER,
                            leader_name TEXT,
                            leader_birthday timestamp,
                            leader_lang TEXT,
                            leader_gender TEXT,
                            )''')


#  group_name = family_23145, where 23145 if leader_id
def add_new_group(group_name: str, users: str, leader_id: int, leader_name: str, leader_birthday,
                  leader_lang: str, wish: str = ''):
    global db_name
    con = sql.connect(f'{db_name}.db')

    try:
        with con:
            group = [i for i in con.execute(f'SELECT * FROM {db_name} WHERE groups_name = "{group_name}"')]
            print(group)
            if not group:
                con.execute(f'INSERT INTO {db_name} (groups_name, users, wish, leader_id, leader_name,'
                            f'leader_birthday, leader_lang) values(?, ?, ?, ?, ?, ?, ?)',
                            (group_name, users, wish, leader_id, leader_name,
                             leader_birthday, leader_lang))

    except sql.OperationalError as e:
        if DEBUG:
            print(e)


def delete_group(group_name: str):
    global db_name
    con = sql.connect(f'{db_name}.db')

    try:
        with con:
            con.execute(f'DELETE FROM {db_name} WHERE groups_name = "{group_name}"')
    except sql.OperationalError as e:
        if DEBUG:
            print(e)
        raise NameError('Данной группы не существует')


def add_wish(group_name: str, wish: str):
    global db_name
    con = sql.connect(f'{db_name}.db')

    try:
        with con:
            list_wish = [i for i in
                         con.execute(f'SELECT wish FROM {db_name} WHERE groups_name = "{group_name}"')][0][0] \
                        + separator + wish

            con.execute(f'UPDATE {db_name} SET wish = "{list_wish}" WHERE groups_name = "{group_name}"')

    except sql.OperationalError as e:
        if DEBUG:
            print(e)
        raise NameError('Данной группы не существует')

    except IndexError:
        raise NameError('Данной группы не существует')


def delete_wish(group_name: str, wish: str):
    global db_name
    con = sql.connect(f'{db_name}.db')

    try:
        with con:
            list_wish = [i for i in
                         con.execute(f'SELECT wish FROM {db_name} WHERE groups_name = "{group_name}"')][0][0]

            if wish not in list_wish:
                raise NameError('Желания не существует')

            list_wish = list_wish.replace(separator + wish, '')
            con.execute(f'UPDATE {db_name} SET wish = "{list_wish}" WHERE groups_name = "{group_name}"')

    except sql.OperationalError as e:
        if DEBUG:
            print(e)
        raise NameError('Данной группы не существует')


def update_value(column_name: str, new_value, **kwargs):
    global db_name
    con = sql.connect(f'{db_name}.db')

    try:
        with con:
            con.execute(f'UPDATE {db_name} SET {column_name} = "{new_value}" WHERE ({", ".join([i for i in kwargs.keys()])}) = ({"".join(["?, "  if i != len(kwargs.keys()) - 1 else "?" for i in range(len(kwargs.keys()))])})', tuple([i for i in kwargs.values()]))

    except sql.OperationalError as e:
        if DEBUG:
            print(e)
        raise NameError('Данной группы не существует')


def search_value(column_name: str, **kwargs):
    global db_name
    con = sql.connect(f'{db_name}.db')

    try:
        with con:
            res = [i for i in con.execute(f'SELECT {column_name} FROM {db_name} WHERE ({", ".join([i for i in kwargs.keys()])}) = ({"".join(["?, "  if i != len(kwargs.keys()) - 1 else "?" for i in range(len(kwargs.keys()))])})', tuple([i for i in kwargs.values()]))]
            return res[0]

    except sql.OperationalError as e:
        if DEBUG:
            print(e)
        raise NameError('Данной группы не существует')

    except IndexError as e:
        if DEBUG:
            print(e)
        raise NameError('Данной группы не существует')


db_name = 'groups'
separator = '♣'

# TODO: изменение пола, даты рождения, имени, языка, пользователей в группе
# create_user_db()
# print('создано')
# add_new_group(group_name='family_23512345', users='mother', leader_id=1234, leader_name='rev',
#               leader_birthday='27.10.2009', leader_lang='ru')
# print('есть данные')
# delete_group('family_23512345')
# delete_group('family_23512345')
# print('удалили')
# add_wish('family_23512345', 'ноут')
# print('добавлено желание')

# delete_wish('family_23512345', 'мышка')
