SELECT t.id, t.name, STRING_AGG(DISTINCT l.name, ', ') AS available_languages
FROM Title t
JOIN Film f ON t.id = f.titleID  
JOIN TitleLanguage tl ON t.id = tl.titleID
JOIN Language l ON tl.languageID = l.id
GROUP BY t.id, t.name
HAVING COUNT(CASE WHEN l.name = 'English' THEN 1 END) > 0
   AND COUNT(CASE WHEN l.name = 'Spanish' THEN 1 END) > 0
   AND COUNT(CASE WHEN l.name = 'Italian' THEN 1 END) > 0;