SELECT t.id, t.name, t.description
FROM Title t
WHERE t.name ~ '[0-9]';