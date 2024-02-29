# import os
# import json
# import logging

# file_db = "db.json"
# current_dir = os.getcwd()
# DB_PATH = os.path.join(current_dir, file_db)
# print(DB_PATH)

# # индексация строк
# def split_words_with_index(items_list):
#     for index, item in enumerate(items_list, start=1):
#         words = item.split(",")
#         for i, word in enumerate(words, start=1):
#             print(f"{index} - {word}")
            
# def split_words(items_list):
#     my_string = ' '.join(items_list)
#     return my_string

# class User:
#     def __init__(self, user_id, favorite_books, favorite_genre, ignored_books):
#         self.user_id = user_id
#         self.favorite_books = favorite_books
#         self.favorite_genre = favorite_genre
#         self.ignored_books = ignored_books


# class Database:
#     def __init__(self):
#         self.data = []      #список пользователей   

#     def save_to_json(self):
#         '''сохранение в БД'''
#         with open(DB_PATH, 'w', encoding='utf-8') as file:
#             json.dump([vars(data_block) for data_block in self.data], file, ensure_ascii=False, indent=4)

#     def load_from_json(self):
#         '''извлечение из БД'''
#         try:
#             with open(DB_PATH, 'r', encoding='utf-8') as file:
#                 data_db = json.load(file)
#                 self.data = [User(**data) for data in data_db]
#         except FileNotFoundError:
#             print("Не загружены данные: Файл базы данных не найден.") 

#     def generate_report(self, user_id):
#         '''печать отчета по пользователю'''
#         self.load_from_json()
#         for data_block in self.data:
#             if data_block.user_id == user_id:        
#                 print(f"[ОТЧЕТ] ")
#                 print(f"Пользователь id: {data_block.user_id}")
#                 print(f"Любимые книги: {data_block.favorite_books}")
#                 print(f"Любимые жанры: {data_block.favorite_genre}")
#                 print(f"Игнорируемые книги: {data_block.ignored_books}")
#             else:
#                 print("Записей нет, добавьте книги")

#     def generate_report_books(self, user_id):
#         '''печать отчета по любимым книгам'''
#         self.load_from_json()
#         for data_block in self.data:
#             if data_block.user_id == user_id:        
#                 split_words_with_index(data_block.favorite_books)
#             else:
#                 print("Записей нет, добавьте книги")
                

#     def generate_report_ganre(self, user_id):
#         '''печать отчета по любимым книгам'''
#         self.load_from_json()
#         for data_block in self.data:
#             if data_block.user_id == user_id:        
#                 split_words_with_index(data_block.favorite_genre)
#             else:
#                 print("Записей нет, добавьте книги")
                
#     def generate_report_ignore(self, user_id):
#         '''печать отчета по любимым книгам'''
#         self.load_from_json()
#         for data_block in self.data:
#             if data_block.user_id == user_id:        
#                 split_words_with_index(data_block.ignored_books)
#             else:
#                 print("Записей нет, добавьте книги")                                

#     def generate_str_books(self, user_id):
#         '''печать строки по любимым книгам'''
#         self.load_from_json()
#         for data_block in self.data:
#             if data_block.user_id == user_id:        
#                 my_string = ', '.join(data_block.favorite_books)
#                 return my_string

#     def generate_str_genre(self, user_id):
#         '''печать строки по любимым жанрам'''
#         self.load_from_json()
#         for data_block in self.data:
#             if data_block.user_id == user_id:        
#                 my_string = ', '.join(data_block.favorite_genre)
#                 return my_string
    
#     def generate_str_ignored(self, user_id):
#         '''печать строки по игнорируемым'''
#         self.load_from_json()
#         for data_block in self.data:
#             if data_block.user_id == user_id:        
#                 my_string = ', '.join(data_block.ignored_books)
#                 return my_string

#     def add_data(self, user):
#         '''добавить запись пользователя'''
#         self.load_from_json()
#         user.favorite_books = [user.favorite_books] if isinstance(user.favorite_books, str) else user.favorite_books
#         user.favorite_genre = [user.favorite_genre] if isinstance(user.favorite_genre, str) else user.favorite_genre
#         user.ignored_books = [user.ignored_books] if isinstance(user.ignored_books, str) else user.ignored_books       
#         user_exists = False             # флаг что пользователь не найден
#         for data_block in self.data:
#             if data_block.user_id == user.user_id:
#                 # проверка на дубликаты любимых книг
#                 for user_book in user.favorite_books:
#                     if user_book != "":                    
#                         if user_book not in data_block.favorite_books:
#                             data_block.favorite_books.append(user_book)
#                 # проверка на дубликаты категорий
#                 for user_ganre in user.favorite_genre:
#                     if user_ganre != "":
#                         if user_ganre not in data_block.favorite_genre:
#                             data_block.favorite_genre.extend(user.favorite_genre)
#                 # проверка на дубликаты игнорируемых книг
#                 for user_ignore in user.ignored_books:
#                     if user_ignore != "":
#                         if user_ignore not in data_block.ignored_books:
#                             data_block.ignored_books.extend(user.ignored_books)
#                 self.save_to_json()
#                 user_exists = True
#                 break   
#         if not user_exists:
#             self.data.append(user)
#             self.save_to_json()
#             print(f"Создана запись для пользователя id:{user.user_id}")
#             Logger.info(f"Создана запись для пользователя id:{user.user_id}")
#         else:
#             print(f"Добавлена запись для пользователя {user.user_id}")
#             Logger.info(f"Добавлена запись для пользователя id:{user.user_id}")
            
#     def clear_book(self, user_id, i_category, i_item):
#         '''удаление записи'''
#         i_item = i_item -1
#         self.load_from_json()
#         try:
#             for data_block in self.data:
#                 if data_block.user_id == user_id:
#                     if i_category == 1:
#                         data_block.favorite_books.pop(i_item)
#                         self.save_to_json()
#                     elif i_category == 2:
#                         data_block.favorite_genre.pop(i_item)
#                         self.save_to_json()
#                     elif i_category == 3:
#                         data_block.ignored_books.pop(i_item)
#                         self.save_to_json()                    
#                     else:
#                         print("Неверный диапазон!\n Введите значение от 1 до 3, где: \n 1- Удаление любимой книги\n 2- Удаление любимого жанра\n 3- Удаление игнорируемой книги")
#         except:
#             print("Введите категории номерами")
#             Logger.exception('Произошла ошибка', sep=' | ')