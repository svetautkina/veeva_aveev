import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8476303286:AAH8aYcUDx3ou5D0rqe8YemF2R2gY8YHfOY"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я твой первый бот. Напиши мне что-нибудь!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
Доступные команды:
/start - начать работу
/help - получить помощь
Просто напиши сообщение - и я его повторю!
    """
    await update.message.reply_text(help_text)

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    await update.message.reply_text(f'Вы написали: {user_message}')

def main():

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    print("Бот запущен! Нажмите Ctrl+C для остановки")

    application.run_polling()

if __name__ == '__main__':
    main()
