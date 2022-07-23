import telebot

token = open(r'E:\MyProduct\Python\WB\FBSStocks\Class\token', 'r').read()
bot = telebot.TeleBot(token)
#@bot.message_handler(content_types=['text'])
#@bot.send_message(message.chat.id,'test',)
#def start_message(message):
bot.send_message(-740230650, 'test')
# #def sendMyMessage(message):
# @bot.message_handler(commands=['like'])
# def like(message):

#   cid = message.chat.id
#   bot.send_message(cid, str(cid))
# @bot.callback_query_handler(func=lambda call: call.data in ['yes', 'no'])
# def callback_handler(call):

#     cid = call.message.chat.id
#     mid = call.message.message_id
#     answer = call.data
#     #update_lang(cid, answer)
#     try:
#         bot.edit_message_text("You voted: " + answer, cid, mid)
#     except:
#         pass


# bot.infinity_polling()