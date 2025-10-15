SELECT t.id, t.name, c.name AS country_name, AVG(r.rating_value) AS avg_rating
FROM Title t
JOIN Film f ON t.id = f.titleID  
JOIN TitleCountries tc ON t.id = tc.titleID
JOIN Countries c ON tc.countryID = c.id
JOIN Ratings r ON t.id = r.titleID
WHERE c.name = 'Japan'
GROUP BY t.id, t.name, c.name
HAVING AVG(r.rating_value) > (
    SELECT AVG(r2.rating_value)
    FROM Title t2
    JOIN Film f2 ON t2.id = f2.titleID  
    JOIN TitleCountries tc2 ON t2.id = tc2.titleID
    JOIN Countries c2 ON tc2.countryID = c2.id
    JOIN Ratings r2 ON t2.id = r2.titleID
    WHERE c2.name = 'Japan'
);