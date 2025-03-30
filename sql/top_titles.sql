SELECT job_title,
    COUNT(*) as count
FROM jobs
WHERE job_title LIKE :filter
GROUP BY job_title
ORDER BY count DESC
LIMIT 10;