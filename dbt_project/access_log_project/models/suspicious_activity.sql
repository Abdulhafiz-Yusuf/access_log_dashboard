SELECT
    username,
    branch_name,
    role,
    COUNT(*) AS login_count,
    COUNT(DISTINCT ip_address) AS distinct_ip_count,
    COUNT(*) FILTER (WHERE EXTRACT(HOUR FROM login_time) < 6 OR EXTRACT(HOUR FROM login_time) > 21) AS off_hour_logins
FROM {{ ref('stg_access_logs') }}
GROUP BY username, branch_name, role
HAVING COUNT(DISTINCT ip_address) > 3
   OR COUNT(*) FILTER (WHERE EXTRACT(HOUR FROM login_time) < 6 OR EXTRACT(HOUR FROM login_time) > 21) > 2