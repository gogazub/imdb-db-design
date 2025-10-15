WITH FilteredFilms AS (
    SELECT 
        id AS film_id,
        name AS film_name,
        rating,
        rate_count
    FROM Title
    WHERE rate_count > 2 
),
LowestRatedFilm AS (
    SELECT 
        film_id,
        film_name,
        rating
    FROM FilteredFilms
    WHERE rating = (SELECT MIN(rating) FROM FilteredFilms) 
)
SELECT 
    lrf.film_name,
    lrf.rating AS film_rating,
    MAX(r.rating_value) AS max_user_rating
FROM LowestRatedFilm lrf
JOIN Ratings r ON lrf.film_id = r.titleID
GROUP BY lrf.film_name, lrf.rating;