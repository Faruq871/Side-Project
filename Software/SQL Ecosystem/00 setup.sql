DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    dept_id   INT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);

CREATE TABLE employees (
    emp_id   INT PRIMARY KEY,
    emp_name VARCHAR(50) NOT NULL,
    dept_id  INT REFERENCES departments(dept_id),
    salary   NUMERIC(10, 2),
    hired_on DATE
);

CREATE TABLE orders (
    order_id   INT PRIMARY KEY,
    emp_id     INT REFERENCES employees(emp_id),
    amount     NUMERIC(10, 2) NOT NULL,
    order_date DATE NOT NULL
);

INSERT INTO departments VALUES
    (1, 'Engineering'), (2, 'Sales'), (3, 'Finance'), (4, 'Legal');

INSERT INTO employees VALUES
    (1, 'Alice',   1, 95000, '2019-03-15'),
    (2, 'Bob',     1, 82000, '2020-07-01'),
    (3, 'Charlie', 1, 78000, '2021-01-20'),
    (4, 'Diana',   2, 68000, '2018-11-05'),
    (5, 'Ethan',   2, 72000, '2022-05-30'),
    (6, 'Fiona',   3, 88000, '2017-09-12'),
    (7, 'George',  3, 61000, '2023-02-14'),
    (8, 'Hannah', NULL, 55000, '2024-06-01');

INSERT INTO orders VALUES
    (1,  4, 1200.00, '2024-01-10'),
    (2,  4,  750.50, '2024-01-22'),
    (3,  5, 3400.00, '2024-02-03'),
    (4,  4,  980.00, '2024-02-18'),
    (5,  5, 1500.00, '2024-03-01'),
    (6,  1,  250.00, '2024-03-11'),
    (7,  5, 2100.75, '2024-03-25'),
    (8,  4,  640.00, '2024-04-02');
