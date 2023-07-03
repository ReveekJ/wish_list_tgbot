from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from texts import texts


# callback_data = 'ru' or 'en'
def choose_lang_kb(lang: str = None):
    btn_ru = InlineKeyboardButton(text='Изменить на русский 🇷🇺', callback_data='ru')
    btn_en = InlineKeyboardButton(text='Change to English 🇺🇸', callback_data='en')

    if lang == 'ru':
        btn_cancel = InlineKeyboardButton(text='Не изменять ❌', callback_data='cancel_choose_lang')
        lang_kb = InlineKeyboardMarkup(row_width=1).add(btn_en, btn_cancel)
    elif lang == 'en':
        btn_cancel = InlineKeyboardButton(text='Do not change ❌', callback_data='cancel_choose_lang')
        lang_kb = InlineKeyboardMarkup(row_width=1).add(btn_ru, btn_cancel)
    else:
        btn_cancel = InlineKeyboardButton(text='Не изменять (Do not change) ❌', callback_data='cancel_choose_lang')
        lang_kb = InlineKeyboardMarkup(row_width=1).add(btn_ru, btn_en, btn_cancel)

    return lang_kb


def gender_q_kb(lang: str = None):
    btn_male = InlineKeyboardButton(text=texts[lang]['male'], callback_data='male')
    btn_female = InlineKeyboardButton(text=texts[lang]['female'], callback_data='female')
    btn_none = InlineKeyboardButton(text=texts[lang]['none_gender'], callback_data='none')

    gender_kb = InlineKeyboardMarkup(row_width=1).add(btn_male, btn_female, btn_none)

    return gender_kb
