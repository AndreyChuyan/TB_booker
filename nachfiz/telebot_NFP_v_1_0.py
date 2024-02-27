'''Телеграмм бот NFP
'''
#-----библиотеки
import telebot
from telebot import types
import config

#-----переменные
bot = telebot.TeleBot(config.token, parse_mode=None)
#-----функции
#-----цикл

#-----чтение файла Exel
# библиотеки
import xlrd
user_dict = {}
#Функция конвертер значений на листах эксель в словари
#пример пользования xls_dict_Yc_Xr("exercise.xls",2,4,20), где аргументы (файл.xls, номер листа, столбец значений, число строк)
def xls_dict_Yc_Xr(file, list_n, Ycol, Xrow):
    ex_list = []
    #открыть книгу
    workbook = xlrd.open_workbook(file)
    #смотрим нужный лист
    worksheet = workbook.sheet_by_index((list_n)-1)
    #переберем столбцы и строки
    for rowx in range(0, Xrow):
        for colx in range((Ycol-2), Ycol):
            #формируем список
            ex_list.append(worksheet.cell_value(rowx, colx))
    #конвертируем список в словарь
    ex_dict = {ex_list[i]: ex_list[i + 1] for i in range(0, len(ex_list), 2)}
    return ex_dict


upr_1 = xls_dict_Yc_Xr("nfp.xls",1,2,50)
# print(upr_1)
upr_2 = xls_dict_Yc_Xr("nfp.xls",2,2,59)
# print(upr_2)
upr_3 = xls_dict_Yc_Xr("nfp.xls",3,2,25)
# print(upr_3)
upr_4 = xls_dict_Yc_Xr("nfp.xls",4,2,30)
# print(upr_4)
upr_5 = xls_dict_Yc_Xr("nfp.xls",5,2,25)
# print(upr_5)
upr_6 = xls_dict_Yc_Xr("nfp.xls",6,2,15)
# print(upr_6)
upr_7 = xls_dict_Yc_Xr("nfp.xls",7,2,5)
# print(upr_7)
upr_8 = xls_dict_Yc_Xr("nfp.xls",8,2,42)
# print(upr_8)
upr_9 = xls_dict_Yc_Xr("nfp.xls",9,2,39)
# print(upr_9)

#создаем класс пользователя

class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


def mainmenu():
    keyboardmain = types.InlineKeyboardMarkup(row_width=1)  
    but_1 = types.InlineKeyboardButton(text ='1. Сгибание и разгибание рук в упоре лежа', callback_data='call_1')
    but_2 = types.InlineKeyboardButton(text ='2. Наклон туловища вперед', callback_data='call_2')
    but_3 = types.InlineKeyboardButton(text ='3. Подтягивание на перекладине', callback_data='call_3')
    but_4 = types.InlineKeyboardButton(text ='4. Поднимание ног к перекладине', callback_data='call_4')
    but_5 = types.InlineKeyboardButton(text ='5. Подъем переворотом на перекладине', callback_data='call_5')
    but_6 = types.InlineKeyboardButton(text ='6. Подъем силой на перекладине', callback_data='call_6')
    but_7 = types.InlineKeyboardButton(text ='7. Комбинированное силовое упражнение', callback_data='call_7')
    but_8 = types.InlineKeyboardButton(text ='8. Сгибание и разгибание рук в упоре на брусьях', callback_data='call_8')
    but_9 = types.InlineKeyboardButton(text ='9. Угол в упоре на брусьях', callback_data='call_9')    
    but_about = types.InlineKeyboardButton(text ='-О чат боте-', callback_data='call_about')
    keyboardmain.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8, but_9, but_about)
    return keyboardmain

#@bot.message_handler(content_types=['text'])
@bot.message_handler(commands=['start', 'help'])
def menu(message): 
    #keyboard
    keyboardmain = types.InlineKeyboardMarkup(row_width=1)  
    but_1 = types.InlineKeyboardButton(text ='1. Сгибание и разгибание рук в упоре лежа', callback_data='call_1')
    but_2 = types.InlineKeyboardButton(text ='2. Наклон туловища вперед', callback_data='call_2')
    but_3 = types.InlineKeyboardButton(text ='3. Подтягивание на перекладине', callback_data='call_3')
    but_4 = types.InlineKeyboardButton(text ='4. Поднимание ног к перекладине', callback_data='call_4')
    but_5 = types.InlineKeyboardButton(text ='5. Подъем переворотом на перекладине', callback_data='call_5')
    but_6 = types.InlineKeyboardButton(text ='6. Подъем силой на перекладине', callback_data='call_6')
    but_7 = types.InlineKeyboardButton(text ='7. Комбинированное силовое упражнение', callback_data='call_7')
    but_8 = types.InlineKeyboardButton(text ='8. Сгибание и разгибание рук в упоре на брусьях', callback_data='call_8')
    but_9 = types.InlineKeyboardButton(text ='9. Угол в упоре на брусьях', callback_data='call_9')    
    but_about = types.InlineKeyboardButton(text ='-О чат боте-', callback_data='call_about')
    
    keyboardmain.add(but_1, but_2, but_3, but_4, but_5, but_6, but_7, but_8, but_9, but_about)
    # message
    bot.send_message(message.chat.id,'Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный для расчета \nбаллов физической подготовки\nНФП 2023 года \nВыберите упражнение:'.format(message.from_user, bot.get_me()), parse_mode='html',reply_markup=keyboardmain)

def menu_short(message): 
    #keyboard
    keyboardmain_short = types.InlineKeyboardMarkup(row_width=1)  
    but_menu_short = types.InlineKeyboardButton(text ='-В меню-', callback_data='menu')
    keyboardmain_short.add(but_menu_short)
    # message
    bot.send_message(message.chat.id,'Войдите в меню, чтобы выбрать следущее упражнение'.format(message.from_user, bot.get_me()), parse_mode='html',reply_markup=keyboardmain_short)



#---вешаем обработчик событий на нажатие всех inline-кнопок
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    #о боте
    if call.data == 'call_about':
        keyboard_about = types.InlineKeyboardMarkup(row_width=1)
        but_menu = types.InlineKeyboardButton(text ='В меню', callback_data='menu')
        keyboard_about.add(but_menu)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Я - Начфиз, бот созданный для расчета баллов физической подготовки \nНФП 2023 года\nО боте (v.1.0):\nНа текущий момент добавлены упражнения, не требующие дополнительных данных, таких как возраст, пол и вес. В дальнейшем планируется учитывать эти данные и включить больше нормативов ',reply_markup=keyboard_about)
    elif call.data == 'menu':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Вы вернулись в главное меню', reply_markup=mainmenu())
       
    #---упражнения    
    #упражнение 1
    elif call.data == 'call_1':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Введите результаты выполнения упражнения 1: (1-50)')
        bot.register_next_step_handler(msg, mes_upr_1) #передаем ответ в функцию process_name_step
        
    elif call.data == 'call_2':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Введите результаты выполнения упражнения 2: (2-60)')
        bot.register_next_step_handler(msg, mes_upr_2) #передаем ответ в функцию process_name_step             

    elif call.data == 'call_3':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Введите результаты выполнения упражнения 3: (1-25)')
        bot.register_next_step_handler(msg, mes_upr_3) #передаем ответ в функцию process_name_step             

    elif call.data == 'call_4':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Введите результаты выполнения упражнения 4: (1-18)')
        bot.register_next_step_handler(msg, mes_upr_4) #передаем ответ в функцию process_name_step             

    elif call.data == 'call_5':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Введите результаты выполнения упражнения 5: (1-25)')
        bot.register_next_step_handler(msg, mes_upr_5) #передаем ответ в функцию process_name_step             

    elif call.data == 'call_6':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Введите результаты выполнения упражнения 6: (1-15)')
        bot.register_next_step_handler(msg, mes_upr_6) #передаем ответ в функцию process_name_step             

    elif call.data == 'call_7':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Введите результаты выполнения упражнения 7: (1-5)')
        bot.register_next_step_handler(msg, mes_upr_7) #передаем ответ в функцию process_name_step             

    elif call.data == 'call_8':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Введите результаты выполнения упражнения 8: (1-42)')
        bot.register_next_step_handler(msg, mes_upr_8) #передаем ответ в функцию process_name_step             

    elif call.data == 'call_9':
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'Введите результаты выполнения упражнения 9: (2-40)')
        bot.register_next_step_handler(msg, mes_upr_9) #передаем ответ в функцию process_name_step             

#//обработчики результатов ввода
def mes_upr_1(message):
    try:
        chat_id = message.chat.id
        name = float(message.text)
        user = User(name)
        user_dict[chat_id] = user
        bot.reply_to(message, '1. Сгибание и разгибание рук в упоре лежа (баллов)\n -- ' + str(int(upr_1[name])) + ' --')
        menu_short(message)
    except Exception as e:
        bot.reply_to(message, 'Неверный диапазон!')
        menu(message)

def mes_upr_2(message):
    try:
        chat_id = message.chat.id
        name = float(message.text)
        user = User(name)
        user_dict[chat_id] = user
        bot.reply_to(message, '2. Наклон туловища вперед (баллов)\n -- ' + str(int(upr_2[name])) + ' --')
        menu_short(message)
    except Exception as e:
        bot.reply_to(message, 'Неверный диапазон!')
        menu(message)

def mes_upr_3(message):
    try:
        chat_id = message.chat.id
        name = float(message.text)
        user = User(name)
        user_dict[chat_id] = user
        bot.reply_to(message, '3. Подтягивание на перекладине (баллов)\n -- ' + str(int(upr_3[name])) + ' --')
        menu_short(message)
    except Exception as e:
        bot.reply_to(message, 'Неверный диапазон!')
        menu(message)

def mes_upr_4(message):
    try:
        chat_id = message.chat.id
        name = float(message.text)
        user = User(name)
        user_dict[chat_id] = user
        bot.reply_to(message, '4. Поднимание ног к перекладине (баллов)\n -- ' + str(int(upr_4[name])) + ' --')
        menu_short(message)
    except Exception as e:
        bot.reply_to(message, 'Неверный диапазон!')
        menu(message)
        
def mes_upr_5(message):
    try:
        chat_id = message.chat.id
        name = float(message.text)
        user = User(name)
        user_dict[chat_id] = user
        bot.reply_to(message, '5. Подъем переворотом на перекладине (баллов)\n -- ' + str(int(upr_5[name])) + ' --')
        menu_short(message)
    except Exception as e:
        bot.reply_to(message, 'Неверный диапазон!')
        menu(message)
        
def mes_upr_6(message):
    try:
        chat_id = message.chat.id
        name = float(message.text)
        user = User(name)
        user_dict[chat_id] = user
        bot.reply_to(message, '6. Подъем силой на перекладине (баллов)\n -- ' + str(int(upr_6[name])) + ' --')
        menu_short(message)
    except Exception as e:
        bot.reply_to(message, 'Неверный диапазон!')
        menu(message)

def mes_upr_7(message):
    try:
        chat_id = message.chat.id
        name = float(message.text)
        user = User(name)
        user_dict[chat_id] = user
        bot.reply_to(message, '7. Комбинированное силовое упражнение (баллов)\n -- ' + str(int(upr_7[name])) + ' --')
        menu_short(message)
    except Exception as e:
        bot.reply_to(message, 'Неверный диапазон!')
        menu(message)
        
def mes_upr_8(message):
    try:
        chat_id = message.chat.id
        name = float(message.text)
        user = User(name)
        user_dict[chat_id] = user
        bot.reply_to(message, '8. Сгибание и разгибание рук в упоре на брусьях (баллов)\n -- ' + str(int(upr_8[name])) + ' --')
        menu_short(message)
    except Exception as e:
        bot.reply_to(message, 'Неверный диапазон!')
        menu(message)
        
def mes_upr_9(message):
    try:
        chat_id = message.chat.id
        name = float(message.text)
        user = User(name)
        user_dict[chat_id] = user
        bot.reply_to(message, '9. Угол в упоре на брусьях (баллов)\n -- ' + str(int(upr_9[name])) + ' --')
        menu_short(message)
    except Exception as e:
        bot.reply_to(message, 'Неверный диапазон!')
        menu(message)
        

      
if __name__ == '__main__':      
      bot.polling(none_stop=True)


#сократить все функциями
