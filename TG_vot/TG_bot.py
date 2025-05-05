from telebot import TeleBot, types
from dotenv import load_dotenv
import os
import openai

load_dotenv("/.env")

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

logic_mode = {}

@bot.message_handler(commands=["logic_mode"])
def enable_logic_mode(message):
    logic_mode[message.chat.id] = True
    bot.reply_to(message, "🧠 Режим логики включён! Теперь я буду объяснять, почему отвечаю так или иначе.")

@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.lower()
    explain = logic_mode.get(chat_id, False)

    if "привет" or "hello in text:
        response = "Добро пожаловать в Startup House! 🚀"
        if explain:
            response += "\n\n📌 Объяснение: найдено ключевое слово 'привет'."
        bot.reply_to(message, response)

    elif "ии" in text or "бизнес" in text:
        response = "Отлично! Расскажи, как ты используешь ИИ в бизнесе? 💡"
        if explain:
            response += "\n\n📌 Объяснение: найдено ключевое слово 'ии' или 'бизнес'."
        bot.reply_to(message, response)

    else:
        try:
            messages = [
                {"role": "user", "content": message.text}
            ]
            if explain:
                messages.insert(0, {
                    "role": "system",
                    "content": "Ты помощник, который всегда объясняет, почему дал такой ответ."
                })

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )
            reply = response.choices[0].message['content']
            bot.reply_to(message, reply)

        except Exception as e:
            bot.reply_to(message, "Ой, что-то пошло не так 😓")

bot.infinity_polling()
