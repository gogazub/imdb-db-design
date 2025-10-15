# 🎬 IMDb-like Database Design

Этот проект - **дизайн реляционной базы данных для сервиса по типу IMDB**, включающего фильмы, сериалы, актеров, компании, награды, отзывы и рейтинги.  

База реализована на **PostgreSQL**.  
Для наполнения используется **Faker**

---

## Краткая схема БД

```text
Users (id, username, email, password_hash, reviews_count)
Title (id, name, description, budget, box_office, rating, rate_count, ...)
 ├─ Film (titleID, year, duration)
 ├─ Series (titleID, years, seasons_count, episode_duration)
 ├─ TitleGenres (titleID, genreID)
 ├─ TitleLanguage (titleID, languageID)
 ├─ TitleCompany (titleID, companyID)
 ├─ TitleAwards (titleID, awardID, year, result)
 ├─ TitleCountries (titleID, countryID)
 ├─ TitlePersons (titleID, personID, roleID)
 └─ Media (titleID, url)

Genres (id, name) — жанры  
Language (id, name) — языки  
Company (id, name) — студии  
Countries (id, name) — страны  
Awards (id, name) — награды

Persons (id, countryID, name, birth_day, ...)  
 ├─ Roles (id, name)
 ├─ TitlePersons (связь с Title + Roles)
 ├─ PersonAwards (personID, awardID, year, result)
 └─ Photo (personID, url)

Ratings (titleID, userID, rating_value)  
Reviews (titleID, userID, text, likes, dislikes)
```

📌 Таблицы `TitleGenres`, `TitleLanguage`, `TitleCompany`, `TitleAwards`, `TitleCountries`, `TitlePersons` реализуют связи многие-ко-многим.

---

## Примеры SQL-запросов

| №  | Название                                        | Файл                    | Тип запроса          |
|----|-------------------------------------------------|--------------------------|-----------------------|
| 1  | Фильмы после 2017 года                          | `запрос1.sql`            | `SELECT` + `JOIN` |
| 2  | Средний рейтинг фильмов из Японии               | `запрос2.sql`            | `AVG`, `HAVING` |
| 3  | Фильмы с ENG + SPA + IT языками                 | `запрос3.sql`            | `STRING_AGG` |
| 4  | Топ-5 фильмов по рейтингу и наградам           | `запрос4.sql`            | `CTE`, `GROUP BY` |
| 5  | Средний рейтинг по странам                     | `запрос5.sql`            | `GROUP BY` |
| 6  | Фильмы с одним жанром                          | `запрос6.sql`            | `HAVING` |
| 7  | Обновление имени + выбор актёров               | `запрос7.sql`            | `UPDATE`, `SELECT` |
| 8  | Фильмы с цифрами в названии                    | `запрос8.sql`            | regex |
| 9  | Самый низкий рейтинг и макс. оценка            | `запрос9.sql`            | CTE |
| 10 | Персоны без наград                             | `запрос10#1.sql`         | `NOT EXISTS` |
| 11 | Персоны без наград (через LEFT JOIN)           | `запрос10#2.sql`         | `LEFT JOIN` |
| 12 | Сравнение ролей актёров (кино vs сериалы)     | `запрос11.sql`           | `CASE`, `JOIN` |
| 13 | Рекурсивный обход ролей                        | `запросрекурс.sql`       | `WITH RECURSIVE` |
| 14 | Актёры с наибольшим разнообразием ролей       | `мойзапрос1.sql`        | CTE, `ARRAY_AGG` |
| 15 | Топ-5 студий по окупаемости фильмов           | `мойзапрос2.sql`        | `RANK()`, агрегаты |

---

## ⚡ Быстрый старт

```bash
# 1. Создать базу данных
createdb mydb

# 2. Инициализировать структуру
python script.py

# 3. Наполнить данными (полная версия)
python insert2.py
# или быстрая версия
python insert_users.py

# 4. Выполнить запрос через psql
psql -d mydb -f запрос1.sql
```

---

## 📝 Примечания

- Все `insert`-скрипты выполняют полную очистку (`TRUNCATE CASCADE`) перед генерацией данных.  
- Faker генерирует уникальные имена, email, описания и др. для имитации реальных данных.  
- Поддерживаются фильмы и сериалы, многоязычность, жанры, актёры, студии и награды.  
- SQL-запросы ориентированы на **аналитику и демонстрацию возможностей схемы**.
