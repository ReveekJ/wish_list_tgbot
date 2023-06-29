import pip

# from server import keep_alive

pip.main(['install', 'pytelegrambotapi'])
from aiogram import Bot, Dispatcher, executor, types, utils
import keyboard as kb
import db
import datetime

token = '5997812115:AAGoLOMTQqfUl9tKB5WWOHha_8J0YL3l_wU'
bot = Bot(token=token)
dp = Dispatcher(bot)

texts = {'ru': {'auto_lang': 'Привет! Автоматически выбран русский язык (Hello! Automatically selected Russian '
                             'language)',
                'personally_group_name': 'Личное 🔒'},
         'en': {'auto_lang': 'Hello! Automatically selected English language (Привет! Автоматически выбран английский '
                             'язык)',
                'personally_group_name': 'Personally 🔒'}}


@dp.message_handler(commands=['start'])
async def hello_message(message: types.Message):
    chat_id = message.from_id
    try:
        lang = message.from_user.language_code if db.search_value('leader_lang', leader_id=1506907277) == tuple() else \
            db.search_value('leader_lang', leader_id=1506907277)[0]
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


@dp.callback_query_handler(lambda c: c.data == 'ru' or c.data == 'en' or c.data == 'cancel_choose_lang')
async def selected_ru_lang(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback.id)
    chat_id = callback.from_user.id
    data = callback.data

    if data != 'cancel_choose_lang':
        db.update_value(column_name='leader_lang', new_value=callback.data, leader_id=chat_id)

    db.update_value(column_name='groups_name', new_value=texts[data]['personally_group_name'] + '_' + str(chat_id),
                    leader_id=chat_id)
    await bot.send_message(chat_id=chat_id, text='done')


# keep_alive()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
