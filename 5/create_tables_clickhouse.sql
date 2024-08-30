CREATE TABLE IF NOT EXISTS employees (
    id UInt32,
    name String,
    age UInt32,
    position String,
    salary Float32
) ENGINE = MergeTree()
ORDER BY id;
INSERT INTO employees (id, name, age, position, salary) VALUES (1, 'John', 10, 'Software Engineer', 600);
INSERT INTO employees (id, name, age, position, salary) VALUES (2, 'Jane', 20, 'Data Scientist', 700);
INSERT INTO employees (id, name, age, position, salary) VALUES (3, 'Alice', 30, 'Product Manager', 800);
