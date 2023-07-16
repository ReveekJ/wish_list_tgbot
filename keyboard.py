from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from texts import texts
# import db


# callback_data = 'ru' or 'en'
def choose_lang_kb(lang: str = None):
    btn_ru = InlineKeyboardButton(text=texts[lang]['change_to'], callback_data='ru')
    btn_en = InlineKeyboardButton(text=texts[lang]['change_to'], callback_data='en')
    btn_next = InlineKeyboardButton(text=texts[lang]['next'], callback_data='next')

    if lang == 'ru':
        lang_kb = InlineKeyboardMarkup(row_width=1).add(btn_en, btn_next)
    elif lang == 'en':
        lang_kb = InlineKeyboardMarkup(row_width=1).add(btn_ru, btn_next)
    else:
        lang_kb = InlineKeyboardMarkup(row_width=1).add(btn_ru, btn_en, btn_next)

    return lang_kb


def choose_gender_kb(gender: str, lang: str = None):
    btn_male = InlineKeyboardButton(text=texts[lang]['male'] if gender != 'male' else texts[lang]['male'] + ' ✅',
                                    callback_data='male')
    btn_female = InlineKeyboardButton(
        text=texts[lang]['female'] if gender != 'female' else texts[lang]['female'] + ' ✅', callback_data='female')
    btn_none = InlineKeyboardButton(
        text=texts[lang]['none_gender'] if gender != 'none' else texts[lang]['none_gender'] + ' ✅',
        callback_data='none')
    btn_next = InlineKeyboardButton(text=texts[lang]['next'], callback_data='next')
    # btn_male = InlineKeyboardButton(text='male', callback_data='male')
    # btn_female = InlineKeyboardButton(text='female', callback_data='female')
    # btn_none = InlineKeyboardButton(text='none', callback_data='none')

    gender_kb = InlineKeyboardMarkup(row_width=1).add(btn_male, btn_female, btn_none, btn_next)

    return gender_kb


def choose_month_birth_kb(month: str, lang: str):
    months = ['dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov']
    month_kb = InlineKeyboardMarkup(row_width=3)
    # i == 'dec' for example
    for i in range(0, len(months), 3):
        month_kb.add(InlineKeyboardButton(text=texts[lang][months[i]] if months[i] != month else texts[lang][months[i]]
                                          + ' ✅', callback_data=months[i]),
                     InlineKeyboardButton(text=texts[lang][months[i + 1]] if months[i + 1] != month else
                     texts[lang][months[i + 1]] + ' ✅', callback_data=months[i + 1]),
                     InlineKeyboardButton(text=texts[lang][months[i + 2]] if months[i + 2] != month else
                     texts[lang][months[i + 2]] + ' ✅', callback_data=months[i + 2])
                     )

    month_kb.add(InlineKeyboardButton(text=texts[lang]['next'], callback_data='next'))

    return month_kb


def choose_day_birth_kb(day: int, month: str, lang: str):
    month_day = {'dec': 31, 'jan': 31, 'feb': 29, 'mar': 31, 'apr': 30, 'may': 31, 'jun': 30, 'jul': 31, 'aug': 31,
                 'sep': 30, 'oct': 31, 'nov': 30}
    day_kb = InlineKeyboardMarkup(row_width=3)

    for i in range(1, month_day[month] + 1, 3):
        if i + 2 <= month_day[month]:
            day_kb.add(InlineKeyboardButton(text=str(i) if day != i else str(i) + ' ✅', callback_data=str(i)),
                       InlineKeyboardButton(text=str(i + 1) if day != i + 1 else str(i + 1) + ' ✅',
                                            callback_data=str(i + 1)),
                       InlineKeyboardButton(text=str(i + 2) if day != i + 2 else str(i + 2) + ' ✅',
                                            callback_data=str(i + 2)))
        elif i + 1 <= month_day[month]:
            day_kb.add(InlineKeyboardButton(text=str(i) if day != i else str(i) + ' ✅', callback_data=str(i)),
                       InlineKeyboardButton(text=str(i + 1) if day != i + 1 else str(i + 1) + ' ✅',
                                            callback_data=str(i + 1)))
        else:
            day_kb.add(InlineKeyboardButton(text=str(i) if day != i else str(i) + ' ✅', callback_data=str(i)))
        # day_kb.add(InlineKeyboardButton(text=str(i) if day != i else str(i) + ' ✅', callback_data=str(i)))

    day_kb.add(InlineKeyboardButton(text=texts[lang]['next'], callback_data='next'))
    return day_kb
