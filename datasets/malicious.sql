DROP TABLE Employee
TRUNCATE TABLE Employee
DELETE FROM Employee WHERE ID=100
UPDATE Employee SET Name='Hacked' WHERE ID=100
INSERT INTO Employee VALUES(9999, 'Hacker', 'Attack')
ALTER TABLE Employee ADD COLUMN Password TEXT
CREATE TABLE Users(username TEXT, password TEXT)
EXEC xp_cmdshell
SELECT * FROM Employee UNION SELECT password FROM Users
SELECT * FROM Employee UNION SELECT username, password FROM Users
SELECT * FROM Employee WHERE ID=1 OR 1=1
SELECT * FROM Employee WHERE ID=1 OR TRUE
SELECT * FROM Employee WHERE ID=1 OR '1'='1'
SELECT * FROM Employee WHERE ID=100 OR 'a'='a'
SELECT * FROM Employee WHERE ID=1 -- comment
SELECT * FROM Employee /* hidden attack */
SELECT * FROM Employee WHERE ID=1; DROP TABLE Employee
SELECT * FROM Employee WHERE ID=1; DELETE FROM Employee