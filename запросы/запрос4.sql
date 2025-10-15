WITH TopRatedFilms AS (
    SELECT t.id, t.name, AVG(r.rating_value) AS avg_rating
    FROM Title t
    JOIN Film f ON t.id = f.titleID  
    JOIN Ratings r ON t.id = r.titleID
    GROUP BY t.id, t.name
    ORDER BY avg_rating DESC
    LIMIT 5
)

SELECT trf.id, trf.name, trf.avg_rating, COUNT(ta.awardID) AS awards_count
FROM TopRatedFilms trf
LEFT JOIN TitleAwards ta ON trf.id = ta.titleID
GROUP BY trf.id, trf.name, trf.avg_rating
ORDER BY trf.avg_rating DESC;