import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from bot_database import BotDatabase
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TelegramBot:
    def __init__(self, token, db):
        self.application = Application.builder().token(token).build()
        self.db = db
        self.setup_handlers()

    def setup_handlers(self):
        """Настройка обработчиков команд и сообщений"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.message.from_user
        user_id = user.id

        if not self.db.user_exists(user_id):
            self.db.add_user(user_id, user.username, user.first_name)
            welcome_text = f"Привет, {user.first_name}! Вы зарегистрированы в системе."
        else:
            welcome_text = f"С возвращением, {user.first_name}!"
        await update.message.reply_text(welcome_text)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        user_id = update.message.from_user.id
        message_text = update.message.text

        self.db.save_message(user_id, message_text)
        await update.message.reply_text("Сообщение сохранено!")

    def run(self):
        """Запуск бота"""
        print("Бот запущен...")
        self.application.run_polling()