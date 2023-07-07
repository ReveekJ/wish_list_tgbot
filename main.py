import pip

# from server import keep_alive

pip.main(['install', 'pytelegrambotapi'])
from aiogram import Bot, Dispatcher, executor, types
import keyboard as kb
import db
import datetime
from texts import texts
from Parser_Telegram_chats.main import send_messages, client

token = '5997812115:AAGoLOMTQqfUl9tKB5WWOHha_8J0YL3l_wU'
bot = Bot(token=token)
dp = Dispatcher(bot)


# TODO: выбор дня рождения

async def send_invite(contact_id, from_id):
    # lang = db.search_value('leader_lang', leader_id=contact_id)
    name = db.search_value('leader_name', leader_id=from_id)[0]

    async with client:
        await send_messages(contact_id, [f'{texts["any"]["invite1"]} {name} {texts["any"]["invite2"]}'])


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def invite(message: types.Contact):
    # id и телефон контакта, которого отправил пользователь
    phone = message['contact']['phone_number']
    contact_id = message['contact']['user_id']
    user_id = message['from']['id']
    user_name = db.search_value('leader_name', leader_id=user_id)[0]
    contact_lang = db.search_value('leader_lang', leader_id=contact_id)

    try:
        # если в бд есть contact_id - то он не упадет с ошибкой, иначе nameError
        db.search_value('leader_id', leader_id=contact_id)
        await bot.send_message(chat_id=contact_id, text=f'{texts[contact_lang]["invite1"]} {user_name} {texts[contact_lang]["invite2"]}')
    except NameError:
        await send_invite(phone if phone is not None else contact_id, user_id)
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

    print(lang)
    name = message.from_user.first_name + ' ' + message.from_user.last_name if message.from_user.last_name is not None \
        else message.from_user.first_name
    # print(lang)
    # await bot.send_message(chat_id=chat_id, text='Choose language (Выберите язык)', reply_markup=kb.choose_lang_kb()

    db.add_new_group(group_name=texts[lang]['personally_group_name'] + '_' + str(chat_id),
                     users=str(chat_id),
                     leader_id=chat_id,
                     leader_name=name,
                     leader_lang=lang,
                     leader_birthday=datetime.date.today(),
                     leader_gender='none')

    await bot.send_message(chat_id=chat_id, text=texts[lang]['auto_lang'], reply_markup=kb.choose_lang_kb(lang=lang))
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
    gender = db.search_value('leader_gender', leader_id=chat_id)[0]

    await bot.answer_callback_query(callback.id)
    await bot.send_message(chat_id=chat_id, text='done')

    # после того как пользователь выбрал язык спрашиваем его пол
    # если спросить в hello_message то он отправит сразу запрос и на язык и на пол
    await bot.send_message(chat_id=chat_id, text=texts[lang]['gender_q'], reply_markup=kb.choose_gender_kb(gender=gender
                                                                                                           , lang=lang))


@dp.callback_query_handler(lambda c: c.data == 'male' or c.data == 'female' or c.data == 'none')
async def choose_gender(callback: types.CallbackQuery):
    chat_id = callback.from_user.id
    data = callback.data

    db.update_value(column_name='leader_gender', new_value=data, leader_id=chat_id)

    lang = db.search_value('leader_lang', leader_id=chat_id)[0]
    gender = db.search_value('leader_gender', leader_id=chat_id)[0]

    await bot.answer_callback_query(callback.id)
    await callback.message.delete()
    await bot.send_message(chat_id=chat_id, text=texts[lang]['gender_q'], reply_markup=kb.choose_gender_kb(gender=gender
                                                                                                           , lang=lang))


# keep_alive()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
