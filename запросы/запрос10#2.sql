SELECT p.id, p.name
FROM Persons p
LEFT JOIN PersonAwards pa ON p.id = pa.personID
WHERE pa.personID IS NULL;