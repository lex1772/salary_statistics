import json
import logging
import os

from dotenv import load_dotenv, find_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters)

from console import service

# Загрузка файла .env с автоматическим поиском
load_dotenv(find_dotenv())

# Вывод логов в консоль
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Функция приветствия при нажатии на кнопку /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Hi <a href='t.me/"
             f"{update.effective_user.username}'>"
             f"{update.effective_user.first_name} "
             f"{update.effective_user.last_name}</a>!",
        parse_mode='html')


# Функция получения данных и отправки обработанных данных пользователю
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_message = json.loads(update.message.text)
    except json.decoder.JSONDecodeError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Невалидный запрос. '
                 'Пример запроса:\n{"dt_from": '
                 '"2022-09-01T00:00:00", "dt_upto": '
                 '"2022-12-31T23:59:00", '
                 '"group_type": "month"}')
    else:
        try:
            func = getattr(service, user_message["group_type"])
        except AttributeError:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Невалидный запрос. '
                     'Пример запроса:\n{"dt_from": '
                     '"2022-09-01T00:00:00", "dt_upto": '
                     '"2022-12-31T23:59:00", '
                     '"group_type": "month"}')
        else:
            try:
                result = await func(user_message)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=result
                )
            except ValueError:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Невалидный запрос. '
                         'Пример запроса:\n{"dt_from": '
                         '"2022-09-01T00:00:00", "dt_upto": '
                         '"2022-12-31T23:59:00", "group_type": '
                         '"month"}')


# Запуск программы
if __name__ == '__main__':
    # Строим приложение при помощи токена
    application = ApplicationBuilder().token(os.getenv('TG_BOT_TOKEN')).build()

    # Определяем точки взаимодействия с пользователем
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, message
        )
    )

    # Инициализация, старт приложения и получение обновлений
    application.run_polling()
