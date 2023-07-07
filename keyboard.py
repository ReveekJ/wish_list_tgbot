from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from texts import texts
import db


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


def choose_gender_kb(gender: str, lang: str = None):
    btn_male = InlineKeyboardButton(text=texts[lang]['male'] if gender != 'male' else texts[lang]['male'] + ' ✅',
                                    callback_data='male')
    btn_female = InlineKeyboardButton(
        text=texts[lang]['female'] if gender != 'female' else texts[lang]['female'] + ' ✅', callback_data='female')
    btn_none = InlineKeyboardButton(
        text=texts[lang]['none_gender'] if gender != 'none' else texts[lang]['none_gender'] + ' ✅',
        callback_data='none')
    # btn_male = InlineKeyboardButton(text='male', callback_data='male')
    # btn_female = InlineKeyboardButton(text='female', callback_data='female')
    # btn_none = InlineKeyboardButton(text='none', callback_data='none')

    gender_kb = InlineKeyboardMarkup(row_width=1).add(btn_male, btn_female, btn_none)

    return gender_kb


def choose_month_birth_kb(lang: str):
    months = ['dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov' ]
    month_kb = InlineKeyboardMarkup()

    for i in months:
        month_kb.add(InlineKeyboardButton(text=texts[lang][i], callback_data=i))

    return month_kb
