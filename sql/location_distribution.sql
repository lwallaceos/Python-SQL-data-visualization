SELECT location,
    COUNT(*) as count
FROM jobs
WHERE location LIKE :filter
GROUP BY location
ORDER BY count DESC;