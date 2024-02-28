import os
import json
import logging
from src.my_loguru import Logger
import telebot
import requests
from config import TOKEN_TELEGRAM, TOKEN_OPENAI
from openai import OpenAI

# относительные пути поддиректорий
script_dir = os.path.dirname(os.path.abspath(__file__))
# Путь к директории, где будет храниться база данных
file_db = "db.json"
dir_db = "db"
dir_path_db = os.path.join(script_dir, dir_db)
DB_PATH = os.path.join(dir_path_db, file_db)

# прокси
import os
os.environ['http_proxy'] = 'http://ifk:3f0gns1AZ@46.17.105.102:3128'
os.environ['https_proxy'] = 'http://ifk:3f0gns1AZ@46.17.105.102:3128'

#создаем экземпляры
bot = telebot.TeleBot(TOKEN_TELEGRAM)
client = OpenAI(api_key=TOKEN_OPENAI)


# простые функции
# индексация строк
def split_words_with_index(items_list):
    for index, item in enumerate(items_list, start=1):
        words = item.split(",")
        for i, word in enumerate(words, start=1):
            print(f"{index} - {word}")
            
def split_words(items_list):
    my_string = ' '.join(items_list)
    return my_string
    
# AI
def question_ai(message):
    '''Функция взаимодействия с AI'''
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
        model="gpt-3.5-turbo",
    )
    result = completion.choices[0].message.content
    return result            
            

class User:
    def __init__(self, user_id, favorite_books, favorite_genre, ignored_books):
        self.user_id = user_id
        self.favorite_books = favorite_books
        self.favorite_genre = favorite_genre
        self.ignored_books = ignored_books

class Database:
    def __init__(self):
        self.data = []      #список пользователей   

    def save_to_json(self):
        '''сохранение в БД'''
        with open(DB_PATH, 'w', encoding='utf-8') as file:
            json.dump([vars(data_block) for data_block in self.data], file, ensure_ascii=False, indent=4)

    def load_from_json(self):
        '''извлечение из БД'''
        try:
            with open(DB_PATH, 'r', encoding='utf-8') as file:
                data_db = json.load(file)
                self.data = [User(**data) for data in data_db]
        except FileNotFoundError:
            print("Не загружены данные: Файл базы данных не найден.") 

    def generate_report(self, user_id):
        '''печать отчета по пользователю'''
        self.load_from_json()
        for data_block in self.data:
            if data_block.user_id == user_id:        
                print(f"[ОТЧЕТ] ")
                print(f"Пользователь id: {data_block.user_id}")
                print(f"Любимые книги: {data_block.favorite_books}")
                print(f"Любимые жанры: {data_block.favorite_genre}")
                print(f"Игнорируемые книги: {data_block.ignored_books}")
            else:
                print("Записей нет, добавьте книги")

    def generate_report_books(self, user_id):
        '''печать отчета по любимым книгам'''
        self.load_from_json()
        for data_block in self.data:
            if data_block.user_id == user_id:        
                split_words_with_index(data_block.favorite_books)
            else:
                print("Записей нет, добавьте книги")
                

    def generate_report_ganre(self, user_id):
        '''печать отчета по любимым книгам'''
        self.load_from_json()
        for data_block in self.data:
            if data_block.user_id == user_id:        
                split_words_with_index(data_block.favorite_genre)
            else:
                print("Записей нет, добавьте книги")
                
    def generate_report_ignore(self, user_id):
        '''печать отчета по любимым книгам'''
        self.load_from_json()
        for data_block in self.data:
            if data_block.user_id == user_id:        
                split_words_with_index(data_block.ignored_books)
            else:
                print("Записей нет, добавьте книги")                                

    def generate_str_books(self, user_id):
        '''печать строки по любимым книгам'''
        self.load_from_json()
        for data_block in self.data:
            if data_block.user_id == user_id:        
                my_string = ', '.join(data_block.favorite_books)
                return my_string

    def generate_str_genre(self, user_id):
        '''печать строки по любимым жанрам'''
        self.load_from_json()
        for data_block in self.data:
            if data_block.user_id == user_id:        
                my_string = ', '.join(data_block.favorite_genre)
                return my_string
    
    def generate_str_ignored(self, user_id):
        '''печать строки по игнорируемым'''
        self.load_from_json()
        for data_block in self.data:
            if data_block.user_id == user_id:        
                my_string = ', '.join(data_block.ignored_books)
                return my_string

    def add_data(self, user):
        '''добавить запись пользователя'''
        self.load_from_json()
        user.favorite_books = [user.favorite_books] if isinstance(user.favorite_books, str) else user.favorite_books
        user.favorite_genre = [user.favorite_genre] if isinstance(user.favorite_genre, str) else user.favorite_genre
        user.ignored_books = [user.ignored_books] if isinstance(user.ignored_books, str) else user.ignored_books       
        user_exists = False             # флаг что пользователь не найден
        for data_block in self.data:
            if data_block.user_id == user.user_id:
                # проверка на дубликаты любимых книг
                for user_book in user.favorite_books:
                    if user_book != "":                    
                        if user_book not in data_block.favorite_books:
                            data_block.favorite_books.append(user_book)
                # проверка на дубликаты категорий
                for user_ganre in user.favorite_genre:
                    if user_ganre != "":
                        if user_ganre not in data_block.favorite_genre:
                            data_block.favorite_genre.extend(user.favorite_genre)
                # проверка на дубликаты игнорируемых книг
                for user_ignore in user.ignored_books:
                    if user_ignore != "":
                        if user_ignore not in data_block.ignored_books:
                            data_block.ignored_books.extend(user.ignored_books)
                self.save_to_json()
                user_exists = True
                break   
        if not user_exists:
            self.data.append(user)
            self.save_to_json()
            print(f"Создана запись для пользователя id:{user.user_id}")
            Logger.info(f"Создана запись для пользователя id:{user.user_id}")
        else:
            print(f"Добавлена запись для пользователя {user.user_id}")
            Logger.info(f"Добавлена запись для пользователя id:{user.user_id}")
            
    def clear_book(self, user_id, i_category, i_item):
        '''удаление записи'''
        i_item = i_item -1
        self.load_from_json()
        try:
            for data_block in self.data:
                if data_block.user_id == user_id:
                    if i_category == 1:
                        data_block.favorite_books.pop(i_item)
                        self.save_to_json()
                    elif i_category == 2:
                        data_block.favorite_genre.pop(i_item)
                        self.save_to_json()
                    elif i_category == 3:
                        data_block.ignored_books.pop(i_item)
                        self.save_to_json()                    
                    else:
                        print("Неверный диапазон!\n Введите значение от 1 до 3, где: \n 1- Удаление любимой книги\n 2- Удаление любимого жанра\n 3- Удаление игнорируемой книги")
        except:
            print("Введите категории номерами")
            Logger.exception('Произошла ошибка', sep=' | ')
            

db1 = Database()
user_id_number = 6574345

users = []
Logger.info('Программа была запущена', is_traceback=True)



while True:
    try:
        m0 = int(input("\n--Генератор интересного чтива-- Автор Чуян А.А. \n--Выберите задачу: \n 1- Добавление интересов\n 2- Удаление интересов\n 3- Отчет по интересам\n 4- Подготовить подборку книг по интересам\n   0 - Выход\n    : "))
        # подменю добавления
        if m0 == 1:     
            m1 = int(input("\n----Выберите задачу: \n 1- Добавление любимой книги\n 2- Добавление любимого жанра\n 3- Добавление игнорируемой книги\n 0 - Переход в меню\n  : "))
            if m1 == 1:
                print("Список ваших любимых книг: ")
                db1.generate_report_books(user_id_number)
                m1_m1 = input('Введите название любимой книги: ')
                user = User(user_id_number, m1_m1, "", "")
                db1.add_data(user)
                users.append(user)
                print("Добавлено")
                print("Список ваших любимых книг: ")
                db1.generate_report_books(user_id_number)
                pass
            elif m1 == 2:
                print("Список ваших любимых жанров: ")
                db1.generate_report_ganre(user_id_number)
                m1_m2 = input('Введите название любимого жанра: ')
                user = User(user_id_number, "", m1_m2, "")
                db1.add_data(user)
                users.append(user)
                print("Добавлено")
                print("Список ваших любимых жанров: ")
                db1.generate_report_ganre(user_id_number)
                pass
            elif m1 == 3:
                print("Список ваших игнорируемых книг: ")
                db1.generate_report_ignore(user_id_number)
                m1_m3 = input('Введите название игнорируемых книг: ')
                user = User(user_id_number, "", "", m1_m3)
                db1.add_data(user)
                users.append(user)
                print("Добавлено")
                print("Список ваших игнорируемых книг: ")
                db1.generate_report_ignore(user_id_number)
                pass
            elif m1 == 0:
                print("Выход в меню")
                break
            else:
                print("Неправильный ввод. Пожалуйста, выберите существующую задачу.")
                Logger.error('Неверный ввод!', is_traceback=True)
        # подменю удаления
        elif m0 == 2:     
            m2 = int(input("\n----Выберите задачу: \n 1- Удаление любимой книги\n 2- Удаление любимого жанра\n 3- Удаление игнорируемой книги\n 0 - Переход в меню\n  : "))
            if m2 == 1:
                print("Список ваших любимых книг: ")
                db1.generate_report_books(user_id_number)
                m2_m1 = int(input("\nВыберите номер книги для удаления: \n  : "))
                db1.clear_book(user_id_number, 1, m2_m1)
                print("Удалено")
                print("Список ваших любимых книг: ")
                db1.generate_report_books(user_id_number)
                pass
            elif m2 == 2:
                print("Список ваших любимых жанров: ")
                db1.generate_report_ganre(user_id_number)
                m2_m2 = int(input("\nВыберите жанр для удаления: \n  : "))
                db1.clear_book(user_id_number, 2, m2_m2)
                print("Удалено")
                print("Список ваших любимых жанров: ")
                db1.generate_report_ganre(user_id_number)
                pass
            elif m2 == 3:
                print("Список ваших игнорируемых книг: ")
                db1.generate_report_ignore(user_id_number)
                m2_m3 = int(input("\nВыберите игнорируемую книгу для удаления: \n  : "))
                db1.clear_book(user_id_number, 3, m2_m2)
                print("Удалено")
                print("Список ваших игнорируемых книг: ")
                db1.generate_report_ignore(user_id_number)
                pass
            elif m2 == 0:
                print("Выход в меню")
                break
            else:
                print("Неправильный ввод. Пожалуйста, выберите существующую задачу.")
                Logger.error('Неверный ввод!', is_traceback=True)
        # подменю отчета
        elif m0 == 3: 
            print("----Генерация полного отчета----")
            print("----Список ваших любимых книг: ")
            db1.generate_report_books(user_id_number)
            print("----Список ваших любимых жанров: ")
            db1.generate_report_ganre(user_id_number)
            print("----Список ваших игнорируемых книг: ")
            db1.generate_report_ignore(user_id_number)            
            continue
        # подменю бота
        elif m0 == 4: 
            question = f"Подбери мне книги, которые бы мне понравились, учитывая мои любимые книги, которые я уже прочитал: {db1.generate_str_books(user_id_number)} \nУчти, что мои любимые жанры: {db1.generate_str_genre(user_id_number)} \nНе предлагай мне книги: {db1.generate_str_ignored(user_id_number)} \nВыдай результат по паре книг на каждый жанр в формате: Жанр: Книга, Автор"
            print(question)
            print(question_ai(question))

        elif m0 == 0:
            print("Программа завершена.")
            Logger.info('Программа была завершена', is_traceback=True)
            break
    except:
        print("Ошибка")
        Logger.exception('Произошла ошибка', sep=' | ')



# @bot.message_handler(commands=['start', 'help', 'asd'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")


# @bot.message_handler(func=lambda m: True)
# def answer_all(message):
#     print(message.from_user)
#     completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": message.text,
#             }
#         ],
#         model="gpt-3.5-turbo",
#     )
#     result = completion.choices[0].message.content
#     bot.reply_to(message, result)


# if __name__ == "__main__":
#     bot.polling()