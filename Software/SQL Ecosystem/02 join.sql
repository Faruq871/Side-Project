-- INNER JOIN
SELECT e.emp_name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.dept_id;

-- LEFT JOIN
SELECT e.emp_name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;

-- FULL OUTER JOIN
SELECT e.emp_name, d.dept_name
FROM employees e
FULL OUTER JOIN departments d ON e.dept_id = d.dept_id;

-- CROSS JOIN
SELECT d.dept_name, o.order_id
FROM departments d
CROSS JOIN orders o;

-- Multi-table join
SELECT e.emp_name, d.dept_name, o.amount
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
JOIN orders o      ON o.emp_id  = e.emp_id;

-- Anti-join (departments with no employees)
SELECT d.dept_name
FROM departments d
LEFT JOIN employees e ON e.dept_id = d.dept_id
WHERE e.emp_id IS NULL;

-- Semi-join (employees with at least one order)
SELECT e.emp_name
FROM employees e
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.emp_id = e.emp_id);

-- SELF JOIN via manager-style pairing
SELECT a.emp_name AS emp_a, b.emp_name AS emp_b, a.dept_id
FROM employees a
JOIN employees b ON a.dept_id = b.dept_id AND a.emp_id < b.emp_id;
