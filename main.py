import pip
from aiogram import Bot, Dispatcher, executor, types
import keyboard as kb
import db
import datetime
from texts import texts, text_to_num_month
from Parser_Telegram_chats.main import send_messages, client

# from server import keep_alive

pip.main(['install', 'pytelegrambotapi'])

token = '5997812115:AAGoLOMTQqfUl9tKB5WWOHha_8J0YL3l_wU'
bot = Bot(token=token)
dp = Dispatcher(bot)
group_name = {}


# async def send_invite(contact_id, from_id):
#     # lang = db.search_value('leader_lang', leader_id=contact_id)
#     name = db.search_value('leader_name', leader_id=from_id)[0]
#
#     async with client:
#         await send_messages(contact_id, [f'{texts["any"]["invite1"]} {name} {texts["any"]["invite2"]}'])


# TODO: нужен ли создатель группы в столбце пользователи?
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def invite(message: types.Contact, ):
    global group_name
    print(message)
    # id и телефон контакта, которого отправил пользователь
    phone = message['contact']['phone_number']
    contact_id = message['contact']['user_id']
    chat_id = message['from']['id']
    user_name = db.search_value('leader_name', leader_id=chat_id)[0]
    lang = db.search_value('leader_lang', leader_id=chat_id)[0]
    old_users = db.search_value('users', leader_id=chat_id)[0]
    print(group_name)

    try:
        db.update_value('users', old_users + ' ' + str(contact_id), groups_name=group_name[chat_id])
    except KeyError:
        # TODO: отправление сообщения данной группы не существует (вроду бы)
        return None

    try:
        # если в бд есть contact_id - то он не упадет с ошибкой, иначе nameError
        contact_lang = db.search_value('leader_lang', leader_id=contact_id)[0]
        db.search_value('leader_id', leader_id=contact_id)
        await bot.send_message(chat_id=contact_id,
                               text=f'{texts[contact_lang]["invite1"]} {user_name} {texts[contact_lang]["invite2"]}')
    except NameError:
        # await send_invite(phone if phone is not None else contact_id, chat_id)
        async with client:
            await send_messages(name_chat_to_send=contact_id,
                                value=[f'{texts["any"]["invite1"]} {user_name} {texts["any"]["invite2"]}'])

    group_name.pop(chat_id)
    await bot.send_message(chat_id=chat_id, text=texts[lang]['invite_done'], reply_markup=kb.end_invite_kb(lang=lang))
    # print(phone, contact_id)


# @dp.message_handler(content_types=types.ContentType.ANY)
# async def t(mes):
#     await bot.send_message(chat_id=5953837676, text='привет')


@dp.message_handler(commands=['start'])
async def hello_message(message: types.Message):
    chat_id = message.from_id
    try:
        lang = message.from_user.language_code if db.search_value('leader_lang', leader_id=chat_id) == tuple() else \
            db.search_value('leader_lang', leader_id=chat_id)[0]
    except NameError:
        lang = message.from_user.language_code

    name = message.from_user.first_name + ' ' + message.from_user.last_name if message.from_user.last_name is not None \
        else message.from_user.first_name
    # print(lang)
    # await bot.send_message(chat_id=chat_id, text='Choose language (Выберите язык)', reply_markup=kb.choose_lang_kb()

    db.add_new_group(group_name=texts[lang]['personally_group_name'] + '_' + str(chat_id),
                     users=str(chat_id),
                     leader_id=chat_id,
                     leader_name=name,
                     leader_lang=lang,
                     leader_birthday='NONE',
                     leader_gender='NONE')
    # отправляем запрос ны выбор языка
    if db.search_value('leader_gender', leader_id=chat_id)[0] == 'NONE':
        await bot.send_message(chat_id=chat_id, text=texts[lang]['auto_lang'],
                               reply_markup=kb.choose_lang_kb(lang=lang), disable_notification=True)
    else:
        # TODO: отправить основное сообщение
        pass
    # await bot.send_message(chat_id=chat_id, text=texts)


@dp.callback_query_handler(lambda c: c.data == 'ru' or c.data == 'en' or c.data == 'cancel_choose_lang')
async def choose_lang(callback: types.CallbackQuery):
    chat_id = callback.from_user.id
    data = callback.data

    if data != 'cancel_choose_lang':
        db.update_value(column_name='leader_lang', new_value=data, leader_id=chat_id)
        db.update_value(column_name='groups_name', new_value=texts[data]['personally_group_name'] + '_' + str(chat_id),
                        leader_id=chat_id)

    lang = db.search_value('leader_lang', leader_id=chat_id)[0]
    # gender = db.search_value('leader_gender', leader_id=chat_id)[0]

    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_message(chat_id=chat_id, text=texts[lang]['auto_lang'], reply_markup=kb.choose_lang_kb(lang=lang),
                           disable_notification=True)


@dp.callback_query_handler(lambda c: c.data == 'male' or c.data == 'female' or c.data == 'none')
async def choose_gender(callback: types.CallbackQuery):
    chat_id = callback.from_user.id
    data = callback.data

    db.update_value(column_name='leader_gender', new_value=data, leader_id=chat_id)

    lang = db.search_value('leader_lang', leader_id=chat_id)[0]
    gender = db.search_value('leader_gender', leader_id=chat_id)[0]

    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_message(chat_id=chat_id, text=texts[lang]['gender_q'],
                           reply_markup=kb.choose_gender_kb(gender=gender, lang=lang),
                           disable_notification=True)


# сначала др потом гендер
@dp.callback_query_handler(lambda c: c.data in ['dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul',
                                                'aug', 'sep', 'oct', 'nov'])
async def choose_month(callback: types.CallbackQuery):
    data = callback.data
    data = text_to_num_month(data)
    chat_id = callback.from_user.id
    callback_id = callback.id
    mes_id = callback.message.message_id
    lang = db.search_value('leader_lang', leader_id=chat_id)[0]

    db.update_value('leader_birthday', datetime.date(year=datetime.date.today().year, month=data,
                                                     day=datetime.date.today().day), leader_id=chat_id)

    await bot.answer_callback_query(callback_id)
    await bot.delete_message(chat_id=chat_id, message_id=mes_id)
    # отправляем запрос на день рождения
    month = db.search_value('leader_birthday', leader_id=chat_id)

    await bot.send_message(chat_id=chat_id, text=texts[lang]['choose_month'],
                           reply_markup=kb.choose_month_birth_kb(lang=lang,
                                                                 month=text_to_num_month(month.month) if type(
                                                                     month) != str else month),
                           disable_notification=True)


@dp.callback_query_handler(lambda c: c.data.isdigit())
async def choose_day_of_birth(callback: types.CallbackQuery):
    chat_id = callback.from_user.id
    lang = db.search_value('leader_lang', leader_id=chat_id)[0]
    data = int(callback.data)
    month = db.search_value('leader_birthday', leader_id=chat_id).month
    # ожидается что вернется datetime.date в db.search
    new_date = datetime.date(year=2000,
                             month=month, day=data)

    db.update_value('leader_birthday', new_date, leader_id=chat_id)
    await bot.answer_callback_query(callback.id)
    # удаляем сообщение и отправляем снова
    await bot.delete_message(chat_id=chat_id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=chat_id, text=texts[lang]['day_q'],
                           reply_markup=kb.choose_day_birth_kb(day=data, month=text_to_num_month(month),
                                                               lang=lang),
                           disable_notification=True)


async def create_group1(chat_id):
    # здесь мы выставляем параметр create_group на 1 и отправляем сообщение: введи название группы, далее дело
    # переходит к функции create_group2
    lang = db.search_value('leader_lang', leader_id=chat_id)[0]
    db.update_value('create_group', new_value=1, leader_id=chat_id)

    await bot.send_message(chat_id=chat_id, text=texts[lang]['create_group1'], disable_notification=True)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def create_group2(message: types.Message):
    chat_id = message.from_user.id
    global group_name
    if db.search_value('create_group', leader_id=chat_id)[0]:
        lang = db.search_value('leader_lang', leader_id=chat_id)[0]
        name = db.search_value('leader_name', leader_id=chat_id)[0]
        birthday = db.search_value('leader_birthday', leader_id=chat_id)
        gender = db.search_value('leader_gender', leader_id=chat_id)[0]
        group_name[chat_id] = message.text + '_' + str(chat_id)

        db.add_new_group(group_name=group_name[chat_id],
                         users=str(chat_id),
                         leader_id=chat_id,
                         leader_name=name,
                         leader_lang=lang,
                         leader_birthday=birthday,
                         leader_gender=gender)

        db.update_value('create_group', new_value=0, leader_id=chat_id)
        await bot.send_message(chat_id=chat_id, text=texts[lang]['create_group2'], disable_notification=True,
                               reply_markup=kb.end_invite_kb(lang=lang))


@dp.callback_query_handler(lambda c: c.data == 'next')
async def _next(callback: types.CallbackQuery):
    chat_id = callback.from_user.id
    mes_id = callback.message.message_id
    text = callback.message.text
    lang = db.search_value('leader_lang', leader_id=chat_id)[0]
    await bot.delete_message(chat_id=chat_id, message_id=mes_id)

    if db.search_value('leader_gender', leader_id=chat_id)[0] == 'NONE':
        if text == texts[lang]['auto_lang']:
            # отправляем запрос на день рождения
            # month = db.search_value('leader_birthday', leader_id=chat_id)

            await bot.send_message(chat_id=chat_id, text=texts[lang]['choose_month'],
                                   reply_markup=kb.choose_month_birth_kb(lang=lang,
                                                                         month='none'),
                                   disable_notification=True)  # month.month if type(month)
            # != str else month
        elif text == texts[lang]['choose_month']:
            # отправляем сообщение на выбор дня рождения
            # TODO: bug fix
            '''ERROR: Task exception was never retrieved
future: <Task finished name='Task-18' coro=<Dispatcher._process_polling_updates() done, defined at /home/user/PycharmProjects/wish_list_tgbot/venv/lib/python3.11/site-packages/aiogram/dispatcher/dispatcher.py:407> exception=ValueError("time data 'NONE' does not match format '%Y-%m-%d'")>
Traceback (most recent call last):
  File "/home/user/PycharmProjects/wish_list_tgbot/venv/lib/python3.11/site-packages/aiogram/dispatcher/dispatcher.py", line 415, in _process_polling_updates
    for responses in itertools.chain.from_iterable(await self.process_updates(updates, fast)):
                                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/PycharmProjects/wish_list_tgbot/venv/lib/python3.11/site-packages/aiogram/dispatcher/dispatcher.py", line 235, in process_updates
    return await asyncio.gather(*tasks)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/PycharmProjects/wish_list_tgbot/venv/lib/python3.11/site-packages/aiogram/dispatcher/handler.py", line 117, in notify
    response = await handler_obj.handler(*args, **partial_data)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/PycharmProjects/wish_list_tgbot/venv/lib/python3.11/site-packages/aiogram/dispatcher/dispatcher.py", line 283, in process_update
    return await self.callback_query_handlers.notify(update.callback_query)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/PycharmProjects/wish_list_tgbot/venv/lib/python3.11/site-packages/aiogram/dispatcher/handler.py", line 117, in notify
    response = await handler_obj.handler(*args, **partial_data)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/PycharmProjects/wish_list_tgbot/main.py", line 218, in _next
    month = db.search_value('leader_birthday', leader_id=chat_id).month
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/PycharmProjects/wish_list_tgbot/db.py", line 121, in search_value
    return datetime.datetime.strptime(res[0][0], '%Y-%m-%d')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/_strptime.py", line 568, in _strptime_datetime
    tt, fraction, gmtoff_fraction = _strptime(data_string, format)
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/_strptime.py", line 349, in _strptime
    raise ValueError("time data %r does not match format %r" %
ValueError: time data 'NONE' does not match format '%Y-%m-%d'''
            month = db.search_value('leader_birthday', leader_id=chat_id).month

            await bot.send_message(chat_id=chat_id, text=texts[lang]['day_q'],
                                   reply_markup=kb.choose_day_birth_kb(day=0, month=text_to_num_month(month),
                                                                       lang=lang), disable_notification=True)
        elif text == texts[lang]['day_q']:
            # запрос гендера
            await bot.send_message(chat_id=chat_id, text=texts[lang]['gender_q'],
                                   reply_markup=kb.choose_gender_kb(gender='none', lang=lang),
                                   disable_notification=True)
        elif text == texts[lang]['gender_q']:
            # создание группы

            await create_group1(chat_id=chat_id)
    else:
        if text == texts[lang]['gender_q']:
            # создание группы
            await create_group1(chat_id=chat_id)
        elif text == texts[lang]['invite_done'] or text == texts[lang]['create_group2']:
            # основное сообщение
            pass

    await bot.answer_callback_query(callback.id)


# keep_alive()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
