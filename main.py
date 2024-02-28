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
# import os
# os.environ['http_proxy'] = 'http://ifk:3f0gns1AZ@46.17.105.102:3128'
# os.environ['https_proxy'] = 'http://ifk:3f0gns1AZ@46.17.105.102:3128'

#создаем экземпляры
# bot = telebot.TeleBot(TOKEN_TELEGRAM)
# client = OpenAI(api_key=TOKEN_OPENAI)

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
            if data_block.user_id == user_id:        #для бота указать текущего пользователя
                print(f"[ОТЧЕТ] ")
                print(f"Пользователь id: {data_block.user_id}")
                print(f"Любимые книги: {data_block.favorite_books}")
                print(f"Любимые жанры: {data_block.favorite_genre}")
                print(f"Игнорируемые книги: {data_block.ignored_books}")
            else:
                print("Записей нет, добавьте книги")
       
    def add_data(self, user):
        '''добавить запись пользователя'''
        self.load_from_json()
        user.favorite_books = [user.favorite_books] if isinstance(user.favorite_books, str) else user.favorite_books
        user.favorite_genre = [user.favorite_genre] if isinstance(user.favorite_genre, str) else user.favorite_genre
        user.ignored_books = [user.ignored_books] if isinstance(user.ignored_books, str) else user.ignored_books       
        user_exists = False             # флаг что пользователь не найден
        for data_block in self.data:
            if data_block.user_id == user.user_id:
                # проверка на отсутствие дубликатов
                data_block.favorite_books.extend(user.favorite_books)
                # for user_db_book in data_block.favorite_books:
                #     for user_book in user.favorite_books:
                #         if user_book != user_db_book:
                #             data_block.favorite_books.extend(user.favorite_books)
                #         else:
                #             print("Выберите книгу, не выбранную ранее")
                # проверка на отсутствие категорий
                for user_db_ganre in data_block.favorite_genre:
                    for user_ganre in user.favorite_genre:
                        if user_ganre != user_db_ganre:
                            data_block.favorite_genre.extend(user.favorite_genre)
                        else:
                            print("Выберите жанр, не выбранный ранее")                    
                # проверка на отсутствие игнорируемых книг
                for user_db_ignore in data_block.ignored_books:
                    for user_ignore in user.ignored_books:
                        if user_ignore != user_db_ignore:
                            print("нашлось")
                            data_block.ignored_books.extend(user.ignored_books)
                        else:
                            print("Выберите игнорируемую книгу, не выбранный ранее")                      
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
            
    def clear_data(self, user_id, i_category, i_item):
        '''удаление записи'''
        self.load_from_json()
        try:
            for data_block in self.data:
                if data_block.user_id == user_id:
                    if i_category == 1:
                        data_block.favorite_books.pop(i_item+1)
                        self.save_to_json()
        except:
            print("Введите категории номерами")
            Logger.exception('Произошла ошибка', sep=' | ')


                
                
        # user.favorite_books = [user.favorite_books] if isinstance(user.favorite_books, str) else user.favorite_books
        # user.favorite_genre = [user.favorite_genre] if isinstance(user.favorite_genre, str) else user.favorite_genre
        # user.ignored_books = [user.ignored_books] if isinstance(user.ignored_books, str) else user.ignored_books       
        # user_exists = False             # флаг что пользователь не найден
        # for data_block in self.data:
        #     if data_block.user_id == user.user_id:
        #         data_block.favorite_books.extend(user.favorite_books)
        #         data_block.favorite_genre.extend(user.favorite_genre)
        #         data_block.ignored_books.extend(user.ignored_books)
        #         self.save_to_json()
        #         user_exists = True
        #         break   
        # if not user_exists:
        #     self.data.append(user)
        #     self.save_to_json()
        #     print(f"Создана запись для пользователя id:{user.user_id}")
        #     Logger.info(f"Создана запись для пользователя id:{user.user_id}")
        # else:
        #     print(f"Добавлена запись для пользователя {user.user_id}")
        #     Logger.info(f"Добавлена запись для пользователя id:{user.user_id}")
    
    
    
    
    
    
db1 = Database()
# db1.load_from_json()
user1 = User(6574345, "Задача трех тел", "Фантастика", "Маугли")
user2 = User(6574345, "Задача трех тел2", "Фантастика2", "Маугли2")
db1.add_data(user1)
db1.add_data(user2)
db1.generate_report(6574345)
# db1.clear_data(6574345, 1, 1)
db1.generate_report(6574345)
    
    
    





# if __name__ == "__main__":
#     bot.polling()






# # определение классов
# class BookBot:
#     def __init__(self, token):
#         self.bot = telebot.TeleBot(token)
#         self.users = {}                                     #словарь пользователей

#     def start(self):                                        #функция старта 
#         @self.bot.message_handler(commands=['start'])       #сообщение старта 
#         def start(message):
#             self.bot.send_message(message.chat.id, "Привет! Поделись своими любимыми книгами и жанрами с ботом.")

#         @self.bot.message_handler(func=lambda message: True)       # отработчик сообщений вызывается при сообщениии от пользователя (П)
#         def handle_message(message):                              # М - обработки сообщений
#             user_id = message.chat.id                               # получаем id П
#             if message.text.lower() == "готово":                    # если получен "Готово"
#                 if user_id in self.users:                           # если П в словаре
#                     self.save_user_data(user_id)                    # М - добавление П в словарь
#                     recommendations = self.get_recommendations(user_id)     # сосотавление списка рекомендаций
#                     self.send_recommendations(user_id, recommendations)     # М - отправка списка книг API
#                 else:
#                     self.bot.send_message(user_id, "Пожалуйста, поделитесь своими любимыми книгами и жанрами сначала.")
#             else:
#                 self.process_user_data(user_id, message.text)       # М - создание записи П
#                 self.bot.send_message(user_id, "Поделись еще любимыми книгами и жанрами или напиши 'Готово'.")


# #цикл программы
#         self.bot.polling()      # цикл бота

#     def save_user_data(self, user_id):
#         with open(f"user_{user_id}.json", 'w') as file:
#             json.dump(self.users[user_id], file)
#         self.bot.send_message(user_id, "Спасибо! Список любимых книг и жанров сохранен.")

#     def get_recommendations(self, user_id):
#         with open(f"user_{user_id}.json", 'r') as file:
#             data = json.load(file)

#         payload = {
#             "user_id": user_id,
#             "books": data['books'],
#             "genres": data['genres']
#         }
#         response = requests.post("https://api.poenai.com/recommendations", json=payload)
#         return response.json()

#     def send_recommendations(self, user_id, recommendations):               # М - отправка списка книг API
#         self.bot.send_message(user_id, "Вот рекомендуемая подборка книг:")
#         for book in recommendations['books']:
#             self.bot.send_message(user_id, book['title'])

#     def process_user_data(self, user_id, text):                             # М - создание записи П
#         if user_id not in self.users:
#             self.users[user_id] = {"books": [], "genres": []}

#         if text.startswith("Книга:"):
#             book = text.replace("Книга:", "").strip()
#             self.users[user_id]['books'].append(book)
#         elif text.startswith("Жанр:"):
#             genre = text.replace("Жанр:", "").strip()
#             self.users[user_id]['genres'].append(genre)

# # Замените "YOUR_BOT_TOKEN" на ваш настоящий токен бота
# if __name__ == "__main__":
#     book_bot = BookBot(TOKEN_TELEGRAM)
#     book_bot.start()