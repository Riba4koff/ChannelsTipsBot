import telebot
import sqlite3
import Topics

from list_of_channels.WB_OZON import list_channels_of_wb_and_ozon
from models.Topic import Topic
from models.Channel import Channel
from telebot import types

# Токен вашего бота
bot_token = '6868528320:AAF4qyq9sPtcrlDoYJe_Oxdd-IimFwlGluQ'
bot = telebot.TeleBot(bot_token)

# Состояния разговора
CHOOSING, CONFIRM = range(2)

BACK_BUTTON_NAME = "Назад"
CATEGORIES_BUTTON_NAME = "Категории"
FEED_BACK_BUTTON_NAME = "Обратная связь"

back_button = types.KeyboardButton(BACK_BUTTON_NAME)
categories_button = types.KeyboardButton(CATEGORIES_BUTTON_NAME)
feedback_button = types.KeyboardButton(FEED_BACK_BUTTON_NAME)


# Функция начала
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Привет! 👋\nДобро пожаловать в бота по подбору полезных каналов!"
             "\nЯ здесь, чтобы помочь тебе найти интересные и полезные контенты.")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(categories_button, feedback_button)

    bot.send_message(
        chat_id=message.chat.id,
        reply_markup=markup,
        text="Давай начнём!"
    )

    # Ждем пока пользователь нажмет на кнопку
    bot.register_next_step_handler(message, menu)


def menu(message):
    chosen_menu = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if chosen_menu == CATEGORIES_BUTTON_NAME:
        choose_topic(message)
    if chosen_menu == FEED_BACK_BUTTON_NAME:
        feedback(message)
    if chosen_menu == BACK_BUTTON_NAME:
        markup.add(categories_button, feedback_button)

        bot.send_message(
            chat_id=message.chat.id,
            text="Выберите пункт меню",
            reply_markup=markup
        )

        bot.register_next_step_handler(message, menu)


def feedback(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(back_button)

    bot.send_message(
        chat_id=message.chat.id,
        text="Если у вас возникли проблемы или вы обнаружили ошибку, не стесняйтесь связаться с нашей службой "
             "поддержки. Мы готовы помочь вам в любое время.\n"
             "\n📧 Электронная почта: channelstipsbot@gmail.com"
             "\n\nОпишите ваш запрос или проблему как можно более подробно, прикрепите скриншоты, если необходимо."
             " Наша команда поддержки постарается оперативно решить ваш вопрос. Благодарим за обратную связь и "
             "сотрудничество!",
        reply_markup=markup
    )

    bot.register_next_step_handler(message, menu)


# Функция выбора темы
def choose_topic(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(Topics.wildberries_and_ozon_button, back_button)

    bot.send_message(
        chat_id=message.chat.id,
        text="Выбери тему, которая тебя интересует.",
        reply_markup=markup
    )

    # Ждем пока пользователь нажмет на кнопку
    bot.register_next_step_handler(message, choose_recommendations)


# Функция рекомендаций каналов
def choose_recommendations(message):
    chosen_topic = message.text  # Приводим выбранную тему к нижнему регистру для удобства сравнения

    # Пример фиктивных данных с рекомендациями для каждой темы
    recommendations = {
        Topics.wildberries_and_ozon_title: list_channels_of_wb_and_ozon
    }

    # Получаем рекомендации для выбранной темы
    recommended_channels = recommendations.get(chosen_topic, [])

    # Если нет рекомендаций для выбранной темы, отправляем сообщение
    if chosen_topic == BACK_BUTTON_NAME:
        menu(message)
        return
    if not recommended_channels:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Извините, но у нас пока нет рекомендаций для темы '{chosen_topic}'. Выберите другую тему:"
        )
        choose_topic(message)
        return

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Отличный выбор! Вот несколько рекомендуемых каналов по теме '{chosen_topic}':"
    )

    # Отправляем ссылки на каналы с описанием
    for channel in recommended_channels:
        description = f"\n*{channel.description}\n\n*" if channel.description else ""
        bot.send_message(
            chat_id=message.chat.id,
            text=f"{description}[{channel.name}]({channel.link})",
            parse_mode="Markdown"
        )

    # Ждем пока пользователь нажмет на кнопку
    bot.register_next_step_handler(message, choose_recommendations)


# Запуск бота
bot.polling(none_stop=True)
