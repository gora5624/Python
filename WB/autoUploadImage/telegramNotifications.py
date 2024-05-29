import telebot
import logging

from Class.tokenOperations import getTeleToken

token, chatID = getTeleToken()
bot_token = token
chat_id = chatID

bot = telebot.TeleBot(bot_token)
bot.config['api_key'] = token

def send_message(text):
    try:
        bot.send_message(chat_id, text)
        bot
    except Exception as e:
        logging.error(f"Error sending Telegram message: {e}")

class Report:
    def __init__(self):
        self.started = 0
        self.completed = 0
        self.errors = []

    def start(self):
        self.started += 1

    def complete(self):
        self.completed += 1

    def add_error(self, item, error):
        self.errors.append((item, error))

    def generate_report(self):
        report = f"#ФОТО Программа завершена.\nВсего обработано задач: {self.started}\nУспешно завершено: {self.completed}\nОшибки:\n"
        if not self.errors:
            report += "Были обработаны без ошибок.\n"
        else:
            for item, error in self.errors:
                report += f"- {item}: {error}\n"
        return report