import telebot
from Channel import Channel
from telebot import types

# Токен вашего бота
bot_token = '6868528320:AAF4qyq9sPtcrlDoYJe_Oxdd-IimFwlGluQ'
bot = telebot.TeleBot(bot_token)

# Состояния разговора
CHOOSING, CONFIRM = range(2)

# Контекст разговора
user_data = {}


# Функция начала
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет! Добро пожаловать в бота по подбору полезных каналов!"
             " Я здесь, чтобы помочь тебе найти интересные и полезные контенты. Давай начнем!")
    choose_topic(message)


# Функция выбора темы
def choose_topic(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    topics = ["WB & OZON"]

    for topic in topics:
        markup.add(types.KeyboardButton(topic))

    bot.send_message(
        chat_id=message.chat.id,
        text= "Выбери тему, которая тебя интересует.",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, choose_recommendations)


# Функция рекомендаций каналов
def choose_recommendations(message):
    chosen_topic = message.text  # Приводим выбранную тему к нижнему регистру для удобства сравнения

    # Пример фиктивных данных с рекомендациями для каждой темы
    recommendations = {
        "WB & OZON": [
            Channel(
                name="Point Free",
                link="t.me/+ckAY2Km-Rl43ZTgy",
                description="Канал со Сливом лучших промокодов, купонов, скидок и акций."
            ),
            Channel(
                name="WB Sniper | Находки с Wildberries | Скидки | Акции",
                link="https://t.me/+H5PdPxdDJvVkZjk6",
                description="Твой личный эксперт лучших предложений на WB 🛍\n— Скидки Wildberries\n— Обзоры товаров "
                            "WB\n— Полезные, интересные товары каждый день\n— Вайлберис / вайлдберис"
            ),
            Channel(
                name="Дьявол носит Wildberries",
                link="https://t.me/+ijuhqpFrdF4yMjBi"
            ),
            Channel(
                name="Находки Скидки WB | ВБ",
                link="t.me/+KWV4nqea8LBkYTMy",
                description="По всем вопросам - @P4H3R\n"
                            "Если он👆спит - @mirman_smm\n"
                            "Админ - @Bikoobraz\n"
                            "Менеджер - @zakaz_tb, @veron1ka1606\n"
            )
        ]
    }

    # Получаем рекомендации для выбранной темы
    recommended_channels = recommendations.get(chosen_topic, [])

    # Если нет рекомендаций для выбранной темы, отправляем сообщение
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
            text= f"{description}[{channel.name}]({channel.link})",
            parse_mode="Markdown"
        )


# Запуск бота
bot.polling(none_stop=True)
