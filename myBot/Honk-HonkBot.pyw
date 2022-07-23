import telebot
token = open(r'E:\MyProduct\Python\myBot\token' , 'r').read()
bot = telebot.TeleBot(token)
@bot.message_handler(content_types=['text'])
def repeat_all_message(message):
    nadegdaNameList = ['надя', 'надежда', 'надю', 'наде', 'нади', 'надежду', 'надежды', 'надежде', 'надюха']
    for name in nadegdaNameList:
        if name in message.text.lower():
            bot.send_voice(message.chat.id,'AwACAgQAAxkBAAMpYtuwHLSqrMaWRyAlSodThLsVjBMAAoIOAAKr1NlSQckaFadIWQ0pBA', reply_to_message_id=message.id)
            break    

# #@bot.message_handler(commands=['like'])
# @bot.message_handler(content_types=['audio'])
# def reply_message_handler(message):
#     file_id = message.audio.file_id
#     #bot.send_message(cid, str(cid))
#     bot.reply_to(message, file_id)

# @bot.message_handler(content_types=['voice'])
# def reply_message_handler(message):
#     file_id = message.voice.file_id
#     #bot.send_message(cid, str(cid))
#     bot.reply_to(message, file_id)

bot.infinity_polling()