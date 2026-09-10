# src/services/telegram_bot.py
import time
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from .job_checker import is_job_up  # Assuming the function is_job_up is in src/services/job_checker.py

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Chat ID to send notifications
CHAT_ID = 'YOUR_CHAT_ID'

# Function to send notification to the user
def send_notification(bot, chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)

# Callback function to check for new job applications
def check_new_job_applications(context: CallbackContext):
    if is_job_up():
        message = """
Job title
Seniority
Company
Main tech stack(Up to 4 technologies)
Secondary tech stack(Unlimited)
Glassdoor salary estimative
Job link
"""
        send_notification(Bot(TELEGRAM_BOT_TOKEN), CHAT_ID, message)

# Telegram Bot setup
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! I will notify you about new job applications')

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    # Set a job to check for new job applications every 3600 seconds (1 hour)
    dp.job_queue.run_repeating(check_new_job_applications, interval=3600, context=updater)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()