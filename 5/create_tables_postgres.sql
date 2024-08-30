CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    namef VARCHAR(100),
    position VARCHAR(100),
    salary NUMERIC
);
INSERT INTO employees (namef, position, salary) VALUES
('Vasja', 'Software Engineer', 600),
('Misha', 'Data Scientist', 77000),
('Katja Johnson', 'Product Manager', 800);
