import telebot as tb
a = 0
bot = tb.TeleBot('5108668338:AAHaju-1tM5drLdU2_DaUK_RS40akcv4aug')

CHANNEL_NAME = '@ispbase'

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Введи значение формата ЗнакЧисло (пример /34), где\n+ - плюс\n- - минус'
                                '\n/ - деление\n* - умножение\nИзначально результат равен нулю'
                                '\nЕсли ввести "." , то значение такжеобнулится')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    global a
    # try:
    if str(message.text)[0] == '+':
        bot.send_message(message.chat.id, 'результат: ' + str(a + float(str(message.text)[1:])))
        a += float(message.text[1:])
    elif str(message.text)[0] == '/':
        bot.send_message(message.chat.id, 'результат: ' + str(a / float(str(message.text)[1:])))
        a /= float(message.text[1:])
    elif str(message.text)[0] == '*':
        bot.send_message(message.chat.id, 'результат: ' + str(a * float(str(message.text)[1:])))
        a *= float(message.text[1:])
    elif str(message.text)[0] == '-':
        bot.send_message(message.chat.id, 'результат: ' + str(a + float(message.text)))
        a += float(message.text)
    elif str(message.text) == '.':
        a = 0
        bot.send_message(message.chat.id, 'результат: ' + str(a))
    else:
        bot.send_message(message.chat.id, 'попробуйте снова')
    # except:
    #     bot.send_message(message.chat.id, 'попробуйте снова')
bot.polling(none_stop=True, interval=0)

