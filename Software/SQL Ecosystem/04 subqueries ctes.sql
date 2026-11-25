-- Scalar subquery
SELECT emp_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Derived table
SELECT dept_id, avg_salary
FROM (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
) t
WHERE avg_salary > 70000;

-- IN / NOT IN (NOT IN is unsafe if the subquery can return NULL)
SELECT emp_name
FROM employees
WHERE emp_id IN (SELECT emp_id FROM orders);

-- NOT EXISTS (NULL-safe alternative)
SELECT e.emp_name
FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.emp_id = e.emp_id);

-- Correlated subquery
SELECT e.emp_name, e.salary
FROM employees e
WHERE e.salary > (
    SELECT AVG(e2.salary) FROM employees e2 WHERE e2.dept_id = e.dept_id
);

-- CTE
WITH dept_stats AS (
    SELECT dept_id, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
)
SELECT d.dept_name, ROUND(s.avg_salary, 2) AS avg_salary
FROM dept_stats s
JOIN departments d ON d.dept_id = s.dept_id;

-- Chained CTEs
WITH order_totals AS (
    SELECT emp_id, SUM(amount) AS total FROM orders GROUP BY emp_id
),
ranked AS (
    SELECT emp_id, total FROM order_totals WHERE total > 2000
)
SELECT e.emp_name, r.total
FROM ranked r
JOIN employees e ON e.emp_id = r.emp_id;

-- Recursive CTE
WITH RECURSIVE counter(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM counter WHERE n < 10
)
SELECT n FROM counter;
