import pandas as pd
import numpy as np

from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Bot, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import logging


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

class SpreadSheet():

    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open("Data-Team's Ideas").get_worksheet(0)

    current_file_col = len(sheet.row_values(1))   # spreadsheet file indexes start with 1
    current_file_row = len(sheet.col_values(current_file_col)) + 1



def save_idea(idea, user):

    SpreadSheet.current_file_col = len(SpreadSheet.sheet.row_values(1))   # spreadsheet file indexes start with 1
    SpreadSheet.current_file_row = len(SpreadSheet.sheet.col_values(SpreadSheet.current_file_col)) + 1
    SpreadSheet.sheet.update_cell(SpreadSheet.current_file_row, SpreadSheet.current_file_col, "{} : {}".format(idea, user))
    SpreadSheet.current_file_row += 1


class CommandAnalyzer():

    def handle_new_message(update, context, callback=False):
        user_id = update.message.from_user.username
        message = update.message.text
        chat_id = update.message.chat_id
        if message in ["/start", "/cancel"]:
            CommandAnalyzer.show_to_user(chat_id, "اگه ایده ای داشتی وارد کن که به صد تا ایده برسیم :)")
        elif message.split(":")[0] =="new_topic":
            topic = message.split(":")[1]
            SpreadSheet.sheet.update_cell(1,SpreadSheet.current_file_col+1, "موضوع {} : {}".format(SpreadSheet.current_file_col+1, topic))
            SpreadSheet.current_file_col += 1
            CommandAnalyzer.show_to_user(chat_id,text =  "موضوع جدید ثبت شد")
        else:
            CommandAnalyzer.show_to_user(chat_id,
                                         "{} امین ایده تو {} رو ثبت کردی. بازم ایده داشتی بنویس که به صدتا ایده برسیم :)".format(SpreadSheet.current_file_row - 1,
                                                                                                                                       SpreadSheet.sheet.cell(1, SpreadSheet.current_file_col).value))
            save_idea(user_id, message)

    def show_to_user(chat_id, text, reply_markup = None):
        CommandAnalyzer.bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)