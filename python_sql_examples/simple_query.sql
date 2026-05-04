-- Advanced SQL queries for user analytics

-- Create a view for active users with profile info
CREATE VIEW active_users AS
SELECT u.id, u.name, u.email, p.city, p.age
FROM users u
JOIN profiles p ON u.id = p.user_id
WHERE u.active = 1 AND p.age BETWEEN 18 AND 65;

-- Query to get user activity summary
SELECT au.name, COUNT(l.login_time) AS login_count,
       AVG(DATEDIFF('day', l.login_time, CURRENT_DATE)) AS avg_days_since_login
FROM active_users au
LEFT JOIN login_logs l ON au.id = l.user_id
WHERE l.login_time >= DATE('now', '-30 days')
GROUP BY au.id, au.name
HAVING login_count > 5
ORDER BY login_count DESC;

-- Insert sample data (for demo)
INSERT INTO users (id, name, email, active) VALUES
(1, 'Alice', 'alice@example.com', 1),
(2, 'Bob', 'bob@example.com', 1);

INSERT INTO profiles (user_id, city, age) VALUES
(1, 'NYC', 30),
(2, 'LA', 25);