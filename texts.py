texts = {'ru': {'auto_lang': 'Привет! Автоматически выбран русский язык (Hello! Automatically selected Russian '
                             'language)',
                'personally_group_name': 'Личное 🔒',
                'age_q': 'Ваш день рождения',
                'gender_q': 'Ваш пол:',
                'male': 'Мужской',
                'female': 'Женский',
                'none_gender': 'Не хочу сообщать',
                'invite1': 'Пользователь',
                'invite2': 'приглашает Вас в группу желаний в боте Wish List (https://t.me/Wish_List_Rev_Bot)',
                'jan': 'Январь',
                'feb': 'Февраль',
                'mar': 'Март',
                'apr': 'Апрель',
                'may': 'Май',
                'jun': 'Июнь',
                'jul': 'Июль',
                'aug': 'Август',
                'sep': 'Сентябрь',
                'oct': 'Октябрь',
                'nov': 'Ноябрь',
                'dec': 'Декабрь',
                'choose_month': 'Выберите месяц своего рождения',
                'next': 'Далее',
                'change_to': 'Change to English 🇺🇸',
                'day_q': 'Выберите день вашего рождения:',
                'create_group1': 'Введи название новой группы: ',
                'create_group2': 'А теперь выберите пользователей, которые будут в группе (отправьте пользователей в '
                                 'виде контактов (📎 -> Контакт))',
                'invite_done': 'Пользователю отправлено приглашение (отправьте еще контакты или нажмите "Далее", '
                               'чтобы завершить выбор контактов)',
                'note_birthday': 'Нам требуется твой месяц и день рождения, чтобы мы могли предупреждать твоих друзей '
                                 'о твоём празднике',
                'ok': 'Хорошо'},
         'en': {'auto_lang': 'Hello! Automatically selected English language (Привет! Автоматически выбран английский '
                             'язык)',
                'personally_group_name': 'Personally 🔒',
                'age_q': 'Your birthday',
                'gender_q': "What's your gender:",
                'male': 'Male',
                'female': 'Female',
                'none_gender': "I don't want to report",
                'invite1': 'User',
                'invite2': 'invites you to the wish group in the Wish List bot (https://t.me/Wish_List_Rev_Bot)',
                'jan': 'January',
                'feb': 'February',
                'mar': 'March',
                'apr': 'April',
                'may': 'May',
                'jun': 'June',
                'jul': 'July',
                'aug': 'August',
                'sep': 'September',
                'oct': 'October',
                'nov': 'November',
                'dec': 'December',
                'choose_month': 'Select your birth month',
                'next': 'Next',
                'change_to': 'Изменить на русский 🇷🇺',
                'day_q': 'Select your birthday:',
                'create_group1': 'Enter the name of the new group: ',
                'create_group2': 'And now select the users who will be in the group (send users as contacts (📎 -> '
                                 'Contact))',
                'invite_done': 'An invitation has been sent to the user (send more contacts or click "next" to ',
                'note_birthday': 'We need your month and birthday so we can alert your friends about your holiday',
                'ok': 'Okay'},
         'any': {'invite1': 'Пользователь (User)',
                 'invite2': 'приглашает Вас в группу желаний в боте Wish List (https://t.me/Wish_List_Rev_Bot) ('
                            'invites you to the wish group in the Wish List bot (https://t.me/Wish_List_Rev_Bot))'}}


# сначала месяц:цифра, затем цифра:месяц
def text_to_num_month(text):
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    nums = [i for i in range(1, 13)]

    a = {months[i]: nums[i] for i in range(len(months))}
    _a = {j: i for i, j in a.items()}

    if type(text) == str:
        return a[text]
    else:
        return _a[text]
