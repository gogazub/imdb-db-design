UPDATE Persons
SET name = CONCAT(SPLIT_PART(name, ' ', 1), ' ', 'Black')
WHERE id = 1; 
SELECT p.id, p.name
FROM Persons p
JOIN TitlePersons tp ON p.id = tp.personID
JOIN Roles r ON tp.roleID = r.id
WHERE r.name = 'Actor'
GROUP BY p.id, p.name
ORDER BY p.id;