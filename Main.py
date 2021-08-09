from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Bot,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import logging
from CommandAnalyzer import *

def main():

    updater = Updater("1926243296:AAGLu-gLgvtqxlvZsKWLc3pzqsyca7x-5TA", use_context=True)
    CommandAnalyzer.bot = Bot("1926243296:AAGLu-gLgvtqxlvZsKWLc3pzqsyca7x-5TA")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler(["start", "main_menu"], CommandAnalyzer.handle_new_message))
    dp.add_handler(MessageHandler(Filters.text, CommandAnalyzer.handle_new_message))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()