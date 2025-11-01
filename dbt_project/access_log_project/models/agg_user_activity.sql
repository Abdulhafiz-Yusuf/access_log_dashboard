SELECT
    log_id,
    user_id,
    LOWER(TRIM(username)) AS username,
    login_time,
    logout_time,
    ip_address,
    INITCAP(device_type) AS device_type,
    UPPER(status) AS status,
    INITCAP(branch_name) AS branch_name,
    INITCAP(role) AS role,
    EXTRACT(HOUR FROM login_time) AS login_hour,
    EXTRACT(DOW FROM login_time) AS login_day
FROM {{ ref('stg_access_logs') }}