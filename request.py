import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="mydb",  # имя вашей базы данных
    user="vasilijkireenkov",  # ваше имя пользователя PostgreSQL
    password="3570",  # ваш пароль PostgreSQL
    host="localhost"  # хост PostgreSQL
)

# Создание курсора для выполнения SQL-запросов
cur = conn.cursor()

# Выполнение запроса для получения всех пользователей
cur.execute("SELECT * FROM users;")

# Извлечение всех результатов
users = cur.fetchall()

# Вывод результатов
for user in users:
    print(f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}")

# Закрытие соединения и курсора
cur.close()
conn.close()