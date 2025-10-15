SELECT p.id, p.name
FROM Persons p
WHERE NOT EXISTS (
    SELECT 1
    FROM PersonAwards pa
    WHERE pa.personID = p.id
);