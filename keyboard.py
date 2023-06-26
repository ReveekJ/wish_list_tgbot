from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# callback_data = 'ru' or 'en
def choose_lang_kb():
    btn_ru = InlineKeyboardButton(text='Русский', callback_data='ru')
    btn_en = InlineKeyboardButton(text='English', callback_data='en')

    lang_kb = InlineKeyboardMarkup(row_width=1).add(btn_ru, btn_en)

    return lang_kb

