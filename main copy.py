import os
import json
import logging
from src.my_loguru import Logger 

# относительные пути поддиректорий
script_dir = os.path.dirname(os.path.abspath(__file__))
# Путь к директории, где будет храниться база данных
file_db = "db.json"
dir_db = "db"
dir_path_db = os.path.join(script_dir, dir_db)
DB_PATH = os.path.join(dir_path_db, file_db)

class Transaction:
    def __init__(self, amount, category, date):
        self.amount = amount        #значение транзакции
        self.category = category    #категория
        self.date = date            #дата

class FinanceManager:
    def __init__(self):
        self.transactions = []      #список транзакций

    def add_transaction(self, transaction):
        '''добавить транзакцию (имя транзакции)'''
        self.transactions.append(transaction)
        self.save_to_json()
        print(f"Добавлена транзакция: {transaction.category} - {transaction.amount}")
        Logger.info(f'Добавлена транзакция: {transaction.category} - {transaction.amount}', is_traceback=True)

    def view_transactions(self, start_date, end_date):
        '''показать транзакции (дата начала, дата окончания)'''
        self.load_from_json()
        filtered_transactions = [t for t in self.transactions if start_date <= t.date <= end_date]
        print(f"[ИНФО] - Транзакции за период: {start_date} - {end_date}")
        for transaction in filtered_transactions:
            print(f"Дата: {transaction.date}, Значение: {transaction.amount}, Категория: {transaction.category}")

    def generate_report(self):
        '''печать отчета по транзакциям'''
        self.load_from_json()
        total_income = sum(t.amount for t in self.transactions if t.amount > 0)
        total_expenses = sum(t.amount for t in self.transactions if t.amount < 0)
        print(f"[ОТЧЕТ] ")
        print(f"Общий доход: {total_income}")
        print(f"Общий расход {total_expenses}")
        print(f"Итоговый баланс: {total_income + total_expenses}")

    def save_to_json(self):
        '''сохранение в БД'''
        with open(DB_PATH, 'w', encoding='utf-8') as file:
            json.dump([vars(transaction) for transaction in self.transactions], file, ensure_ascii=False, indent=4)

    def load_from_json(self):
        '''извлечение из БД'''
        try:
            with open(DB_PATH, 'r', encoding='utf-8') as file:
                data_db = json.load(file)
                self.transactions = [Transaction(**data) for data in data_db]
        except FileNotFoundError:
            print("Не загружены данные: Файл не найден.")   

# Пример использования
manager = FinanceManager()
manager.load_from_json()
# transaction1 = Transaction(500, "Зарплата", "2022-10-15")
# transaction2 = Transaction(-340, "Еда", "2022-10-17")
# manager.add_transaction(transaction1)
# manager.add_transaction(transaction2)
# manager.view_transactions("2022-10-01", "2022-10-31")
# manager.generate_report()

transactions = []
Logger.info('Программа была запущена', is_traceback=True)
while True:
    try:
        m1 = int(input("\n--Личный финансист-- Автор Чуян А.А. \nВыберите задачу:\n   1 - Задать транзакцию\n   2 - Вывод отчета за период\n   3 - Сводный отчет\n   0 - Выход\n    : "))
        if m1 == 1:
            m1_m1 = input('Введите транзакцию в формате: <сумма>, <категория>, <дата> (500, "Зарплата", "2022-10-15") : ')
            list_m1_m1 = m1_m1.replace(" ", "").replace('"', '').split(",")
            transaction = Transaction(int(list_m1_m1[0]), list_m1_m1[1], list_m1_m1[2])
            manager.add_transaction(transaction)
            transactions.append(transaction)
            pass
        elif m1 == 2:
            m1_m2 = input('Введите период в формате: <дата начала>, <дата окончания> (2022-10-01, 2022-10-31) : ')
            list_m1_m2 = m1_m2.replace(" ", "").split(",")
            manager.view_transactions(list_m1_m2[0], list_m1_m2[1])
        elif m1 == 3:
            manager.generate_report()
            pass
        elif m1 == 0:
            print("Программа завершена.")
            Logger.info('Программа была завершена', is_traceback=True)
            break
        else:
            print("Неправильный ввод. Пожалуйста, выберите существующую задачу.")
            Logger.error('Неверный ввод!', is_traceback=True)

    except:
        print("Ошибка")
        Logger.exception('Произошла ошибка', sep=' | ')