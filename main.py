import os
import json
import logging
from src.my_loguru import Logger
import telebot

# относительные пути поддиректорий
script_dir = os.path.dirname(os.path.abspath(__file__))
# Путь к директории, где будет храниться база данных
file_db = "db.json"
dir_db = "db"
dir_path_db = os.path.join(script_dir, dir_db)
DB_PATH = os.path.join(dir_path_db, file_db)

# определение классов
class BookBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.users = {}                     #словарь пользователей

    def start(self):                                        #функция старта 
        @self.bot.message_handler(commands=['start'])       #сообщение старта 
        def start(message):
            self.bot.send_message(message.chat.id, "Привет! Поделись своими любимыми книгами и жанрами с ботом.")

        @self.bot.message_handler(func=lambda message: True)       # отработчик сообщений вызывается при сообщениии от пользователя (П)
        def handle_message(message):                          # М - обработки сообщений
            user_id = message.chat.id                               # получаем id П
            if message.text.lower() == "готово":                    # если получен "Готово"
                if user_id in self.users:                           # если П в словаре
                    self.save_user_data(user_id)                    # М - добавление П в словарь
                    recommendations = self.get_recommendations(user_id)     # сосотавление списка рекомендаций
                    self.send_recommendations(user_id, recommendations)     # М - отправка списка книг API
                else:
                    self.bot.send_message(user_id, "Пожалуйста, поделитесь своими любимыми книгами и жанрами сначала.")
            else:
                self.process_user_data(user_id, message.text)       # М - создание записи П
                self.bot.send_message(user_id, "Поделись еще любимыми книгами и жанрами или напиши 'Готово'.")

        self.bot.polling()      # цикл бота

    def save_user_data(self, user_id):
        with open(f"user_{user_id}.json", 'w') as file:
            json.dump(self.users[user_id], file)
        self.bot.send_message(user_id, "Спасибо! Список любимых книг и жанров сохранен.")

    def get_recommendations(self, user_id):
        with open(f"user_{user_id}.json', 'r') as file:
            data = json.load(file)

        payload = {
            "user_id": user_id,
            "books": data['books'],
            "genres": data['genres']
        }
        response = requests.post("https://api.poenai.com/recommendations", json=payload)
        return response.json()

    def send_recommendations(self, user_id, recommendations):               # М - отправка списка книг API
        self.bot.send_message(user_id, "Вот рекомендуемая подборка книг:")
        for book in recommendations['books']:
            self.bot.send_message(user_id, book['title'])

    def process_user_data(self, user_id, text):                             # М - создание записи П
        if user_id not in self.users:
            self.users[user_id] = {"books": [], "genres": []}

        if text.startswith("Книга:"):
            book = text.replace("Книга:", "").strip()
            self.users[user_id]['books'].append(book)
        elif text.startswith("Жанр:"):
            genre = text.replace("Жанр:", "").strip()
            self.users[user_id]['genres'].append(genre)

# Замените "YOUR_BOT_TOKEN" на ваш настоящий токен бота
if __name__ == "__main__":
    book_bot = BookBot("YOUR_BOT_TOKEN")
    book_bot.start()