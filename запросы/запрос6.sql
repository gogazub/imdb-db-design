SELECT t.id, t.name, MIN(g.name) AS genre_name
FROM Title t
JOIN Film f ON t.id = f.titleID 
JOIN TitleGenres tg ON t.id = tg.titleID
JOIN Genres g ON tg.genreID = g.id
GROUP BY t.id, t.name
HAVING COUNT(tg.genreID) = 1;