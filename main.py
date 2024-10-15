'''
Задача:
Необходимо написать телеграм бота, который будет:

1. принимать 3 переменные:
    дата (пока 2 идеи: вводить пользователю или брать из даты отправки сообщения)
    категория трат (реализовать командой через слэш заранее подготовленные категории,
                    после которой пользователю потребуется внести сумму)
    сумма (просто числа);

2. выводить на экран по команде show статистику по месяцам: сумму по каждой категории (если трат не было, не выводим).

    кажется здесь подойдет словарь, в котором:
    ключ - категория
    значение - другой словарь:
                ключ - месяц + год
                значение - список из сумм (множество не подходит)

Доп. фичи:
1. выводить файлом
2. удалить ошибочный ввод или заполнение даты в другой день
3. анализ, сравнение по месяцам, рекомендации
4. плановые значение расхода(возможно писать, сколько денег можно потратить, чтобы вписаться в план)
'''

#функция вызова установленной библиотеки для Телеграм. Установка вводом в командную строку: pip3 install --user pyTelegramBotAPI
import telebot
#функция вызова стандартной библиотеки для работы с датами и временем
import time

#полагаю что мне нужно разобраться!!!!!!!!!!
from telebot import types

#обращение к идентификатору телеграмм бота, полученному при его регистрации
token = '7607024997:AAFaoi3yLHUXoed8c2jApEh6lWHlA8dR8oE'

HELP = """
Hello!
Welcome to the expense tracking bot!
/help - display a list of available commands.
/show - show expense information.

Select a spending category, click on the command and enter the amount:
/beauty
/big_expenses
/clothing
/debts
/digital_shopping
/education
/entertainment
/food
/health
/household_goods
/internet_and_communications
/other
/pets
/rent
/repair
/tourism
/transport
"""

categories = {
    '/beauty' : {},
    '/big_expenses' : {},
    '/clothing' : {},
    '/debts' : {},
    '/digital_shopping' : {},
    '/education' : {},
    '/entertainment' : {},
    '/food' : {},
    '/health' : {},
    '/household_goods' : {},
    '/internet_and_communications' : {},
    '/other' : {},
    '/pets' : {},
    '/rent' : {},
    '/repair' : {},
    '/tourism' : {},
    '/transport' : {}
}


def add_spend(date, category, amount):
    global categories
    # Проверяем, есть ли уже такая дата в словаре этой категории
    if date not in categories[category]:
        categories[category][date] = []

    # Добавляем сумму в список для данной даты
    categories[category][date].append(amount)
    print(categories) #для проверки корректности в терминале


bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['help', 'start'])
def help(message):
    bot.send_message(message.chat.id, HELP)

enter_category = ''

@bot.message_handler(commands = ['beauty', 'big_expenses', 'clothing', 'debts', 'digital_shopping', 'education', 'entertainment', 'food', 'health', 'household_goods', 'internet_and_communications', 'other', 'pets', 'rent', 'repair', 'tourism', 'transport'])
def category(message):
    bot.send_message(message.chat.id, 'Enter the amount spent in this category')
    global enter_category #использование глобальных переменных
    enter_category = message.text
    # print(enter_category)

@bot.message_handler(commands = ['show'])
def show(message):
    global categories
    # Собираем все уникальные даты
    all_dates = set()
    for category_data in categories.values():
        all_dates.update(category_data.keys())

    # Проходим по каждой уникальной дате
    for date in sorted(all_dates):
        bot.send_message(message.chat.id, f'Date: {date}')
        total_amount = 0
        for category, transactions in categories.items():
            if date in transactions:
                category_amount = sum(transactions[date])
                total_amount += category_amount
                bot.send_message(message.chat.id, f'  Category: {category}')
                bot.send_message(message.chat.id, f'    Amount: {category_amount}')
        bot.send_message(message.chat.id, f'Total Amount on {date}: {total_amount} \n')


@bot.message_handler(content_types='text')
def amount(message):
    global enter_category
    enter_amount = message.text
    enter_date = time.strftime('%B %Y', time.gmtime(float(message.date)))
    # Дата из Телеграмм возвращается в формате Unix, для того чтобы ее конвертировать в обычную необходимо импортировать библиотеку time (import time)
    # В коде используется одна строка, ниже пошаговый алгоритм для понимания как работают методы:

    # enter_date = message.date  #берем дату из последнего сообщения в формате UNIX
    # enter_date = float(enter_date) #конвертируем его в тип данных float
    # enter_date = time.gmtime(enter_date) #преобразовываем в переменную из которой можно вытягивать. день/месяц/год и т.д.
    # при печати будет результат:
    # time.struct_time(tm_year=2024, tm_mon=10, tm_mday=10, tm_hour=11, tm_min=53, tm_sec=47, tm_wday=3, tm_yday=284, tm_isdst=0)
    # enter_date = time.strftime('%B %Y', enter_date) #вытягиваем месяц и год

    # print(enter_amount)
    # print(enter_category)

    add_spend(enter_date, enter_category, int(enter_amount))
    text = 'The operation has been accepted. Spent ' +str(enter_amount) + ' in category ' + str(enter_category) + ' ' + str(enter_date)
    bot.send_message(message.chat.id, text)




#Функция polling постоянно обращается к серверам Телеграм
bot.polling(none_stop=True)

