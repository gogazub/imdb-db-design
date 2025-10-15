SELECT c.name AS country_name, AVG(r.rating_value) AS avg_rating
FROM Title t
JOIN Film f ON t.id = f.titleID  
JOIN TitleCountries tc ON t.id = tc.titleID
JOIN Countries c ON tc.countryID = c.id
JOIN Ratings r ON t.id = r.titleID
GROUP BY c.id, c.name
ORDER BY avg_rating DESC;