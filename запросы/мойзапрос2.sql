SELECT 
    c.name AS studio_name,
    COUNT(t.id) AS total_films,
    ROUND(AVG((t.box_office * 1.0) / NULLIF(t.budget, 0)), 2) AS avg_profit_ratio,
    RANK() OVER (ORDER BY AVG((t.box_office * 1.0) / NULLIF(t.budget, 0)) DESC) AS rank_position
FROM Title t
JOIN TitleCompany tc ON t.id = tc.titleID
JOIN Company c ON tc.companyID = c.id
WHERE t.budget > 0 AND t.box_office IS NOT NULL
GROUP BY c.id, c.name
ORDER BY avg_profit_ratio DESC
LIMIT 5;

--выводит топ-5 студий, фильмы которых лучше всего окупились в прокате.

