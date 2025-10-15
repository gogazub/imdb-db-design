SELECT p.id, 
       p.name,
       CASE 
           WHEN COALESCE(film_roles, 0) > COALESCE(series_roles, 0) THEN 'Больше ролей в кино'
           WHEN COALESCE(film_roles, 0) < COALESCE(series_roles, 0) THEN 'Больше ролей в сериалах'
           ELSE 'Одинаково'
       END AS role_comparison
FROM Persons p
JOIN TitlePersons tp ON p.id = tp.personID
JOIN Roles r ON tp.roleID = r.id
LEFT JOIN (
    SELECT tp.personID, COUNT(*) AS film_roles
    FROM TitlePersons tp
    JOIN Film f ON tp.titleID = f.titleID
    WHERE tp.roleID = (SELECT id FROM Roles WHERE name = 'Actor')
    GROUP BY tp.personID
) films ON p.id = films.personID
LEFT JOIN (
    SELECT tp.personID, COUNT(*) AS series_roles
    FROM TitlePersons tp
    JOIN Series s ON tp.titleID = s.titleID
    WHERE tp.roleID = (SELECT id FROM Roles WHERE name = 'Actor')
    GROUP BY tp.personID
) series ON p.id = series.personID
WHERE r.name = 'Actor'
GROUP BY p.id, p.name, film_roles, series_roles
ORDER BY p.name;