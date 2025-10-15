WITH CareerDiversity AS (
    SELECT 
        p.id AS person_id,
        p.name AS person_name,
        COUNT(DISTINCT r.name) AS unique_roles_count,
        ARRAY_AGG(DISTINCT r.name) AS roles
    FROM Persons p
    JOIN TitlePersons tp ON p.id = tp.personID
    JOIN Roles r ON tp.roleID = r.id
    GROUP BY p.id, p.name
),
MaxDiversity AS (
    SELECT 
        MAX(unique_roles_count) AS max_roles
    FROM CareerDiversity
)
SELECT 
    cd.person_id,
    cd.person_name,
    cd.unique_roles_count,
    cd.roles
FROM CareerDiversity cd
JOIN MaxDiversity md ON cd.unique_roles_count = md.max_roles
ORDER BY cd.person_name;