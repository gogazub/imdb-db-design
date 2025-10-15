import psycopg2
from faker import Faker
import random

# Инициализация Faker
fake = Faker()

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="mydb",
    user="vasilijkireenkov",  # замените на ваше имя пользователя
    password="3570",  # замените на ваш пароль
    host="localhost"
)
cur = conn.cursor()

# Очистка всех таблиц
tables = ['Reviews', 'Ratings', 'Media', 'TitleGenres', 'Film', 'Series', 'Seasons',
          'Episodes', 'TitleCompany', 'TitleLanguage', 'TitleAwards', 'TitlePersons',
          'Photo', 'Persons', 'PersonAwards', 'Awards', 'Company', 'Language',
          'Genres', 'Countries', 'Users', 'Title']
for table in tables:
    cur.execute(f"TRUNCATE TABLE {table} CASCADE;")

# Users

# Вставка 10 000 пользователей
unique_emails = set()
while len(unique_emails) < 10000:
    unique_emails.add(fake.email())

# Вставка пользователей в базу данных
existing_users = []
for email in unique_emails:
    username = fake.user_name()
    password_hash = fake.sha256()
    try:
        cur.execute("""
            INSERT INTO Users (username, email, password_hash, reviews_count)
            VALUES (%s, %s, %s, 0);
        """, (username, email, password_hash))
        cur.execute("SELECT id FROM Users ORDER BY id DESC LIMIT 1;")
        user_id = cur.fetchone()[0]
        existing_users.append(user_id)
    except Exception as e:
        print(f"Error inserting {email}: {e}")
        conn.rollback()

# Подтверждаем изменения и закрываем соединение
conn.commit()

print(f"Successfully inserted {len(existing_users)} users.")

# Genres
# Очистка таблицы Genres и сброс последовательности ID
cur.execute("TRUNCATE TABLE Genres RESTART IDENTITY CASCADE;")

# Добавление ровно 25 записей в таблицу Genres
genres = [
    "Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Thriller", "Documentary",
    "Fantasy", "Animation", "Adventure", "Crime", "Biography", "Mystery", "War", "Western",
    "Musical", "History", "Sport", "Family", "Reality-TV", "Short", "News", "Talk-Show", "Anime"
]

for genre in genres:
    cur.execute("INSERT INTO Genres (name, description) VALUES (%s, %s)", 
                (genre, fake.text(max_nb_chars=100)))

# Проверка добавленных данных
cur.execute("SELECT COUNT(*) FROM Genres;")
count = cur.fetchone()[0]
print(f"Genres заполнена: {count} записей.")



# Заполнение таблицы Title
for title_id in range(1, 5001):  # title_id совпадает с порядковым номером записи
    # Генерация названия фильма
    if random.random() < 0.15:  # 15% вероятность добавления цифр
        name = f"{fake.word()} {random.randint(1, 99)}"  # Добавляем случайное число к слову
    else:
        name = fake.sentence(nb_words=3).rstrip('.')  # Генерация обычного названия

    # Генерация остальных полей
    description = fake.text()
    slogan = fake.sentence(nb_words=5).rstrip('.')
    budget = random.randint(10000, 5000000)
    box_office = random.randint(50000, 20000000)
    poster = fake.url()
    age_restriction = random.choice(["PG", "PG-13", "R", "NC-17"])

    # Вставка данных в таблицу Title
    cur.execute("""
        INSERT INTO Title (name, description, slogan, budget, box_office, rating, rate_count, poster, age_restriction)
        VALUES (%s, %s, %s, %s, %s, NULL, 0, %s, %s);
    """, (name, description, slogan, budget, box_office, poster, age_restriction))

conn.commit()
print("Таблица Title успешно заполнена.")

# Ratings
# Очистка и заполнение таблицы Ratings
cur.execute("TRUNCATE TABLE Ratings RESTART IDENTITY CASCADE;")

# Получаем существующие userID из таблицы Users
cur.execute("SELECT id FROM Users;")
existing_users = [row[0] for row in cur.fetchall()]  # Список всех существующих userID

if not existing_users:
    print("Ошибка: Таблица Users пуста. Заполните таблицу Users перед выполнением этого скрипта.")
    exit()

# Генерация 20 000 уникальных рейтингов
existing_combinations = set()

while len(existing_combinations) < 20000:
    title_id = random.randint(1, 5000)  # ID тайтлов от 1 до 5000
    user_id = random.choice(existing_users)  # Случайный userID из существующих

    combination = (title_id, user_id)
    if combination not in existing_combinations:  # Проверка уникальности пары
        rating_value = round(random.uniform(1, 10))  # Рейтинг от 1 до 10 с шагом

        cur.execute("""
            INSERT INTO Ratings (titleID, userID, rating_value)
            VALUES (%s, %s, %s);
        """, (title_id, user_id, rating_value))

        existing_combinations.add(combination)  # Добавляем пару в множество

conn.commit()
print("Таблица Ratings успешно заполнена 20 000 уникальными записями.")

cur.execute("""
    UPDATE Title
    SET rating = subquery.avg_rating,
        rate_count = subquery.total_ratings
    FROM (
        SELECT 
            titleID,
            ROUND(CAST(AVG(r.rating_value) AS NUMERIC), 2) AS avg_rating,
            COUNT(r.rating_value) AS total_ratings
        FROM Ratings r
        GROUP BY r.titleID
    ) AS subquery
    WHERE Title.id = subquery.titleID;
""")

conn.commit()
print("Рейтинги в таблице Title успешно обновлены.")

# TitleGenres
# TitleGenres (8000 связей)
cur.execute("TRUNCATE TABLE TitleGenres RESTART IDENTITY CASCADE;")
# TitleGenres (каждому тайтлу от 1 до 3 жанров)
cur.execute("TRUNCATE TABLE TitleGenres RESTART IDENTITY CASCADE;")
for title_id in range(1, 5001):  # Перебираем все titleID
    genres_assigned = random.sample(range(1, 26), random.randint(1, 3))  # Случайные 1-3 жанра из 25
    for genre_id in genres_assigned:
        cur.execute("""
            INSERT INTO TitleGenres (titleID, genreID) VALUES (%s, %s)
        """, (title_id, genre_id))
# Film
for i in range(1, 2501):
    cur.execute("INSERT INTO Film (titleID, year, duration) VALUES (%s, %s, %s)", (i, random.randint(1990, 2024), random.randint(60, 180)))

# Series
# Series (ID от 2501 до 5000, связанные с Title)
cur.execute("TRUNCATE TABLE Series RESTART IDENTITY CASCADE;")
for i in range(2501, 5001):
    cur.execute("""
        INSERT INTO Series (titleID, years, seasons_count, episode_duration)
        VALUES (%s, %s, %s, %s)
    """, (i, f"{random.randint(2000, 2015)}-{random.randint(2016, 2024)}",
          random.randint(2, 5), random.randint(20, 60)))
# Seasons и Episodes
cur.execute("TRUNCATE TABLE Seasons RESTART IDENTITY CASCADE;")
cur.execute("TRUNCATE TABLE Episodes RESTART IDENTITY CASCADE;")

for series_id in range(1, 2501):  # ID сериалов в таблице Series
    for _ in range(random.randint(2, 5)):  # Случайное количество сезонов
        # Вставка сезона с сохранением его ID
        cur.execute("""
            INSERT INTO Seasons (seriesID, year, episodes_count)
            VALUES (%s, %s, %s) RETURNING id;
        """, (series_id, random.randint(2010, 2024), random.randint(8, 12)))
        
        season_id = cur.fetchone()[0]  # Сохраняем ID вставленного сезона

        # Генерация эпизодов для сезона
        for _ in range(random.randint(8, 12)):  # Случайное количество эпизодов
            cur.execute("""
                INSERT INTO Episodes (seasonID, name, date, description, duration)
                VALUES (%s, %s, %s, %s, %s);
            """, (season_id, fake.sentence(nb_words=3), fake.date(), fake.text(), random.randint(20, 60)))
# Company
# Очистка таблицы Company и сброс ID
cur.execute("TRUNCATE TABLE Company RESTART IDENTITY CASCADE;")

# Вставка 30 компаний
for _ in range(30):
    cur.execute("INSERT INTO Company (name, description) VALUES (%s, %s)", 
                (fake.company(), fake.text(max_nb_chars=100)))

# Проверка количества компаний
cur.execute("SELECT COUNT(*) FROM Company;")
company_count = cur.fetchone()[0]
print(f"Таблица Company заполнена: {company_count} записей.")

# TitleCompany
# TitleCompany (каждому тайтлу от 1 до 3 компаний)
cur.execute("TRUNCATE TABLE TitleCompany RESTART IDENTITY CASCADE;")
for title_id in range(1, 5001):  # Перебираем все titleID
    companies_assigned = random.sample(range(1, 31), random.randint(1, 3))  # Случайные 1-3 компании из 30
    for company_id in companies_assigned:
        cur.execute("""
            INSERT INTO TitleCompany (titleID, companyID) VALUES (%s, %s)
        """, (title_id, company_id))

# Language
# Очистка таблицы Language и сброс ID
cur.execute("TRUNCATE TABLE Language RESTART IDENTITY CASCADE;")

# Добавление 10 фиксированных языков
languages = ["English", "Russian", "French", "Spanish", "German", 
             "Chinese", "Japanese", "Italian", "Korean", "Hindi"]

for language in languages:
    cur.execute("INSERT INTO Language (name) VALUES (%s)", (language,))

# Проверка количества записей в таблице Language
cur.execute("SELECT COUNT(*) FROM Language;")
language_count = cur.fetchone()[0]
print(f"Таблица Language заполнена: {language_count} записей.")

# TitleLanguage
cur.execute("TRUNCATE TABLE TitleLanguage RESTART IDENTITY CASCADE;")
for title_id in range(1, 5001):  # Перебираем все titleID
    languages_assigned = random.sample(range(1, 11), random.randint(2, 6))  # Случайные 2-6 языков из 10
    for language_id in languages_assigned:
        cur.execute("""
            INSERT INTO TitleLanguage (titleID, languageID) VALUES (%s, %s)
        """, (title_id, language_id))

# Awards
# Очистка таблицы Awards и сброс ID
cur.execute("TRUNCATE TABLE Awards RESTART IDENTITY CASCADE;")

# Добавление 20 наград
for _ in range(20):
    cur.execute("INSERT INTO Awards (name, description) VALUES (%s, %s)", 
                (fake.word().title(), fake.text(max_nb_chars=100)))

# Проверка количества записей в таблице Awards
cur.execute("SELECT COUNT(*) FROM Awards;")
awards_count = cur.fetchone()[0]
print(f"Таблица Awards заполнена: {awards_count} записей.")

# TitleAwards
 # TitleAwards (каждому тайтлу от 1 до 7 наград)
cur.execute("TRUNCATE TABLE TitleAwards RESTART IDENTITY CASCADE;")

existing_pairs = set()  # Множество для отслеживания уникальных пар (titleID, awardID)

for title_id in range(1, 5001):  # Перебираем все titleID
    awards_assigned = random.sample(range(1, 21), random.randint(1, 7))  # Случайные 1-7 наград из 20
    for award_id in awards_assigned:
        pair = (title_id, award_id)
        if pair not in existing_pairs:  # Проверяем, что пара уникальна
            cur.execute("""
                INSERT INTO TitleAwards (titleID, awardID, year, result)
                VALUES (%s, %s, %s, %s);
            """, (title_id, award_id, random.randint(2000, 2024), random.choice(["Won", "Nominated"])))
            existing_pairs.add(pair)  # Добавляем пару в множество
countries = [
    "USA", "Russia", "France", "Germany", "Italy", 
    "Japan", "South Korea", "India", "China", "Canada"
]

# Вставка стран в таблицу
for country in countries:
    cur.execute("INSERT INTO Countries (name) VALUES (%s)", (country,))

# Проверка количества записей
cur.execute("SELECT COUNT(*) FROM Countries;")
countries_count = cur.fetchone()[0]
print(f"Таблица Countries заполнена: {countries_count} записей.")

# Persons

cur.execute("TRUNCATE TABLE Persons RESTART IDENTITY CASCADE;")
print("Таблица Persons очищена и последовательности сброшены.")

# Получаем существующие countryID из таблицы Countries
cur.execute("SELECT id FROM Countries;")
existing_countries = [row[0] for row in cur.fetchall()]  # Список всех существующих countryID

if not existing_countries:
    print("Ошибка: Таблица Countries пуста. Заполните таблицу Countries перед выполнением скрипта.")
    exit()

# Генерация 1000 персон с корректным countryID
for i in range(1000):
    name = fake.name()
    birth_day = fake.date_of_birth(minimum_age=18, maximum_age=80)
    biography = fake.text()
    title_count = random.randint(1, 50)
    country_id = random.choice(existing_countries)  # Случайный countryID из существующих
    
    cur.execute("""
        INSERT INTO Persons (countryID, name, birth_day, biography, title_count)
        VALUES (%s, %s, %s, %s, %s);
    """, (country_id, name, birth_day, biography, title_count))

# Фиксация транзакции
conn.commit()
print("Таблица Persons успешно заполнена 1000 записями.")

# Roles
# Очистка таблицы Roles и сброс ID
cur.execute("TRUNCATE TABLE Roles RESTART IDENTITY CASCADE;")

# Список уникальных ролей для заполнения
roles = ["Actor", "Director", "Producer", "Writer", "Composer", "Operator"]

# Вставка ролей в таблицу
for role in roles:
    cur.execute("INSERT INTO Roles (name) VALUES (%s)", (role,))

# Проверка количества записей
cur.execute("SELECT COUNT(*) FROM Roles;")
roles_count = cur.fetchone()[0]
print(f"Таблица Roles заполнена: {roles_count} записей.")

# TitlePersons

cur.execute("TRUNCATE TABLE TitlePersons RESTART IDENTITY CASCADE;")

existing_combinations = set()  # Множество для отслеживания уникальных комбинаций

while len(existing_combinations) < 8000:  # Заполняем ровно 8000 уникальных записей
    title_id = random.randint(1, 5000)
    person_id = random.randint(1, 1000)  # Ограничиваем диапазон personID до существующих значений
    role_id = random.randint(1, 6)
    
    combination = (title_id, person_id, role_id)
    if combination not in existing_combinations:  # Проверка уникальности пары
        cur.execute("""
            INSERT INTO TitlePersons (titleID, personID, roleID) 
            VALUES (%s, %s, %s);
        """, (title_id, person_id, role_id))
        existing_combinations.add(combination)

# Photo
for person_id in range(1, 1001):
    cur.execute("INSERT INTO Photo (personID, url) VALUES (%s, %s)", (person_id, fake.image_url()))



# TitleCountries
cur.execute("TRUNCATE TABLE TitleCountries RESTART IDENTITY CASCADE;")

existing_combinations = set()  # Множество для отслеживания уникальных пар (titleID, countryID)

for title_id in range(1, 5001):  # Перебираем все titleID
    countries_assigned = random.sample(range(1, 11), random.randint(1, 3))  # Случайные 1-3 страны из 10
    for country_id in countries_assigned:
        pair = (title_id, country_id)
        if pair not in existing_combinations:  # Проверяем уникальность пары
            cur.execute("""
                INSERT INTO TitleCountries (titleID, countryID) VALUES (%s, %s);
            """, (title_id, country_id))
            existing_combinations.add(pair)

print("Таблица TitleCountries заполнена: каждому тайтлу присвоено от 1 до 3 стран.")

# PersonAwards


# PersonAwards: случайным personID от 1 до 3 наград
cur.execute("TRUNCATE TABLE PersonAwards RESTART IDENTITY CASCADE;")

# Получаем существующие personID из таблицы Persons
cur.execute("SELECT id FROM Persons;")
existing_persons = [row[0] for row in cur.fetchall()]  # Список всех существующих personID

if not existing_persons:  # Проверка на пустой список
    print("Ошибка: Таблица Persons пуста. Заполните таблицу перед выполнением этого скрипта.")
    exit()

# Ограничиваем выборку случайного количества персон
num_to_select = min(len(existing_persons), random.randint(500, 800))  # Не больше количества доступных personID
random_persons = random.sample(existing_persons, num_to_select)

existing_combinations = set()  # Множество для отслеживания уникальных пар (personID, awardID)

# Назначаем от 1 до 3 наград каждому выбранному personID
for person_id in random_persons:
    awards_assigned = random.sample(range(1, 21), random.randint(1, 3))  # 1-3 награды из 20
    for award_id in awards_assigned:
        pair = (person_id, award_id)
        if pair not in existing_combinations:  # Проверяем уникальность пары
            cur.execute("""
                INSERT INTO PersonAwards (personID, awardID, year, result)
                VALUES (%s, %s, %s, %s);
            """, (person_id, award_id, random.randint(2000, 2024), random.choice(["Won", "Nominated"])))
            existing_combinations.add(pair)

print("Таблица PersonAwards заполнена: случайным personID присвоено от 1 до 3 наград.")

# Reviews
# Очистка и заполнение таблицы Reviews
cur.execute("TRUNCATE TABLE Reviews RESTART IDENTITY CASCADE;")

# Получаем существующие userID из таблицы Users
cur.execute("SELECT id FROM Users;")
existing_users = [row[0] for row in cur.fetchall()]  # Список всех существующих userID

if not existing_users:
    print("Ошибка: Таблица Users пуста. Заполните таблицу Users перед выполнением этого скрипта.")
    exit()

existing_combinations = set()  # Множество для отслеживания уникальных пар (titleID, userID)
while len(existing_combinations) < 20000:
    title_id = random.randint(1, 5000)  # Предполагается, что titleID от 1 до 5000
    user_id = random.choice(existing_users)  # Случайный userID из существующих

    combination = (title_id, user_id)
    if combination not in existing_combinations:  # Проверка уникальности пары
        review_text = fake.text(max_nb_chars=500)
        review_date = fake.date_this_decade()
        likes = random.randint(0, 1000)
        dislikes = random.randint(0, 500)

        cur.execute("""
            INSERT INTO Reviews (titleID, userID, text, date, likes, dislikes)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (title_id, user_id, review_text, review_date, likes, dislikes))
        existing_combinations.add(combination)  # Добавляем пару в множество

cur.execute("""
    UPDATE Users
    SET reviews_count = sub.review_count
    FROM (
        SELECT userID, COUNT(*) AS review_count
        FROM Reviews
        GROUP BY userID
    ) sub
    WHERE Users.id = sub.userID;
""")

# Фиксация изменений
conn.commit()
print("Таблицы Reviews и Users успешно заполнены.")



# Media
cur.execute("TRUNCATE TABLE Media RESTART IDENTITY CASCADE;")

for title_id in range(1, 5001):  # Перебираем все titleID
    cur.execute("""
        INSERT INTO Media (titleID, url) VALUES (%s, %s);
    """, (title_id, fake.image_url()))

print("Таблица Media заполнена: каждому тайтлу присвоен 1 URL.")

# Финализация транзакций
conn.commit()
print("Все таблицы успешно заполнены!")

# Закрытие соединения
cur.close()
conn.close()