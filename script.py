import psycopg2

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="mydb",  # Замените на имя вашей базы данных
    user="vasilijkireenkov",  # Имя пользователя PostgreSQL
    password="3570",  # Ваш пароль
    host="localhost"  # Хост
)

# Создание курсора
cur = conn.cursor()

# SQL-запросы для создания таблиц
commands = [
    """
    CREATE TABLE Users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        reviews_count INT DEFAULT 0
    );
    """,
    """
    CREATE TABLE Title (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        slogan VARCHAR(255),
        budget BIGINT,
        box_office BIGINT,
        rating FLOAT,
        rate_count INT,
        poster VARCHAR(255),
        age_restriction VARCHAR(10)
    );
    """,
    """
    CREATE TABLE Countries (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL
    );
    """,
    """
    CREATE TABLE Persons (
        id SERIAL PRIMARY KEY,
        countryID INT REFERENCES Countries(id) ON DELETE CASCADE,
        photoID INT,
        name VARCHAR(255) NOT NULL,
        birth_day DATE,
        biography TEXT,
        title_count INT
    );
    """,
    """
    CREATE TABLE Reviews (
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        userID INT REFERENCES Users(id) ON DELETE CASCADE,
        text TEXT,
        date DATE,
        likes INT DEFAULT 0,
        dislikes INT DEFAULT 0,
        PRIMARY KEY (titleID, userID)
    );
    """,
    """
    CREATE TABLE Ratings (
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        userID INT REFERENCES Users(id) ON DELETE CASCADE,
        rating_value FLOAT,
        PRIMARY KEY (titleID, userID)
    );
    """,
    """
    CREATE TABLE Media (
        id SERIAL PRIMARY KEY,
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        url VARCHAR(255)
    );
    """,
    """
    CREATE TABLE Genres (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        description TEXT
    );
    """,
    """
    CREATE TABLE TitleGenres (
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        genreID INT REFERENCES Genres(id) ON DELETE CASCADE,
        PRIMARY KEY (titleID, genreID)
    );
    """,
    """
    CREATE TABLE Film (
        id SERIAL PRIMARY KEY,
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        year INT,
        duration INT
    );
    """,
    """
    CREATE TABLE Series (
        id SERIAL PRIMARY KEY,
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        years VARCHAR(50),
        seasons_count INT,
        episode_duration INT
    );
    """,
    """
    CREATE TABLE Seasons (
        id SERIAL PRIMARY KEY,
        seriesID INT REFERENCES Series(id) ON DELETE CASCADE,
        year INT,
        episodes_count INT
    );
    """,
    """
    CREATE TABLE Episodes (
        id SERIAL PRIMARY KEY,
        seasonID INT REFERENCES Seasons(id) ON DELETE CASCADE,
        name VARCHAR(255),
        date DATE,
        description TEXT,
        duration INT
    );
    """,
    """
    CREATE TABLE Company (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT
    );
    """,
    """
    CREATE TABLE TitleCompany (
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        companyID INT REFERENCES Company(id) ON DELETE CASCADE,
        PRIMARY KEY (titleID, companyID)
    );
    """,
    """
    CREATE TABLE Language (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL
    );
    """,
    """
    CREATE TABLE TitleLanguage (
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        languageID INT REFERENCES Language(id) ON DELETE CASCADE,
        PRIMARY KEY (titleID, languageID)
    );
    """,
    """
    CREATE TABLE Awards (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT
    );
    """,
    """
    CREATE TABLE TitleAwards (
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        awardID INT REFERENCES Awards(id) ON DELETE CASCADE,
        year INT,
        result VARCHAR(20),
        PRIMARY KEY (titleID, awardID)
    );
    """,
    """
    CREATE TABLE Roles (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL
    );
    """,
    """
    CREATE TABLE TitlePersons (
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        personID INT REFERENCES Persons(id) ON DELETE CASCADE,
        roleID INT REFERENCES Roles(id) ON DELETE CASCADE,
        PRIMARY KEY (titleID, personID, roleID)
    );
    """,
    """
    CREATE TABLE Photo (
        id SERIAL PRIMARY KEY,
        personID INT REFERENCES Persons(id) ON DELETE CASCADE,
        url VARCHAR(255)
    );
    """,
    """
    CREATE TABLE TitleCountries (
        titleID INT REFERENCES Title(id) ON DELETE CASCADE,
        countryID INT REFERENCES Countries(id) ON DELETE CASCADE,
        PRIMARY KEY (titleID, countryID)
    );
    """,
    """
    CREATE TABLE PersonAwards (
        personID INT REFERENCES Persons(id) ON DELETE CASCADE,
        awardID INT REFERENCES Awards(id) ON DELETE CASCADE,
        year INT,
        result VARCHAR(20),
        PRIMARY KEY (personID, awardID)
    );
    """
]

# Выполнение всех команд для создания таблиц
try:
    for command in commands:
        cur.execute(command)
    conn.commit()
    print("База данных успешно инициализирована!")
except Exception as e:
    print(f"Ошибка при инициализации базы данных: {e}")
    conn.rollback()
finally:
    # Закрытие соединения
    cur.close()
    conn.close()