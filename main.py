import pip

# from server import keep_alive

pip.main(['install', 'pytelegrambotapi'])
from aiogram import Bot, Dispatcher, executor, types, utils
import keyboard as kb
import db
import datetime
from texts import texts


token = '5997812115:AAGoLOMTQqfUl9tKB5WWOHha_8J0YL3l_wU'
bot = Bot(token=token)
dp = Dispatcher(bot)


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
                     leader_birthday=datetime.date.today())

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

    await bot.answer_callback_query(callback.id)
    await bot.send_message(chat_id=chat_id, text='done')

    # после того как пользователь выбрал язык спрашиваем его пол
    # если спросить в hello_message то он отправит сразу запрос и на язык и на пол
    await bot.send_message(chat_id=chat_id, text=texts[lang]['gender_q'], reply_markup=kb.choose_gender_kb(lang=lang))


@dp.callback_query_handler(lambda c: c.data == 'male' or c.data == 'female' or c.data == '')
async def choose_gender(callback: types.CallbackQuery):
    chat_id = callback.from_user.id
    data = callback.data

    db.update_value(column_name='leader_gender', new_value=data, leader_id=chat_id)

    await bot.answer_callback_query(callback.id)
    await bot.send_message(chat_id=chat_id, text='done')


# keep_alive()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
