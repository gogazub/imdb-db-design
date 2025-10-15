SELECT t.id, t.name, f.year, t.description
FROM Title t
JOIN Film f ON t.id = f.titleID
WHERE f.year > 2017;
