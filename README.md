# bot_booker
## Бот предназначен для подбора рекомендаций книг для чтения, основываясь на ваших интересах в литературе
### Инструкция по пользованию:
- составляем список люимых книг в формате:
    Книга - Автор (чем больше, тем точнеее будет выборка)
    список любимых жанров из:
        1. Роман 
        2. Детектив 
        3. Фэнтези
        4. Научная фантастика 
        5. Приключения 
        7. Любовный роман 
- просим получить рекомендации и получаем их по выбранным жанрам и новизне:

Кнопки:
    - добавить любимую книгу
    - убрать любимую книгу

    - добавить любимый жанр
    - убрать любимы жанр

    - сгенерировать рекомендации
    - обновить рекомендации

    -

Под капотом:
    база данныж json
    [
    {
        "user_id": 46588932456565,
        "favorite_books": ["Задача трех тел, Лю Цысинь", "Спин, Роберт Чарльз Уилсон", "Гиперион, Дэн Симмонс"],
        "favorite_genre": ["Научная фантастика", "Приключения"],
        "negativ_books": ["Задача трех тел, Лю Цысинь", "Спин, Роберт Чарльз Уилсон", "Гиперион, Дэн Симмонс"]
    }
    ]

парсить ответ 