WITH RECURSIVE OptimizedRolesHierarchy AS (
    SELECT 
        p.id AS person_id,
        p.name AS person_name,
        r.name AS role_name,
        t.name AS title_name,
        1 AS level
    FROM Persons p
    JOIN TitlePersons tp ON p.id = tp.personID
    JOIN Roles r ON tp.roleID = r.id
    JOIN Title t ON tp.titleID = t.id
    WHERE r.name = 'Actor' 
    
    UNION ALL
    SELECT 
        prh.person_id,
        prh.person_name,
        r.name AS role_name,
        t.name AS title_name,
        prh.level + 1 AS level
    FROM OptimizedRolesHierarchy prh
    JOIN TitlePersons tp ON prh.person_id = tp.personID
    JOIN Roles r ON tp.roleID = r.id
    JOIN Title t ON tp.titleID = t.id
    WHERE r.name != 'Actor' 
      AND prh.level < 5    
)
SELECT DISTINCT person_id, person_name, role_name, title_name, level
FROM OptimizedRolesHierarchy
ORDER BY person_id, level;