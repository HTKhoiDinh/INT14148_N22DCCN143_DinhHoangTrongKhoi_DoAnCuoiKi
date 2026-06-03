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
select * from employee where id=1 or 1=1
select * from employee where id=1 or true
SELECT * FROM Employee WHERE ID=1/**/OR/**/1=1
SELECT * FROM Employee WHERE ID=1; UPDATE Employee SET Name='X'
SELECT * FROM Employee WHERE ID=2500; DROP TABLE Employee
SELECT * FROM Employee WHERE ID=2500 UNION SELECT BankAccount FROM Employee
SELECT * FROM Employee WHERE ID=2500 OR '1'='1'
SELECT * FROM Employee WHERE ID=2500 -- bypass
SELECT * FROM Employee WHERE ID=2500 /* comment */
DELETE FROM Employee
UPDATE Employee SET Salary=0
INSERT INTO Employee VALUES(1, 'Fake', 'Fake', 'Fake', 0, 'TAX', 'Fake', 'Fake')
SELECT * FROM Employee WHERE ID=1 OR 1 = 1
SELECT * FROM Employee WHERE ID=1 OR 2>1
SELECT * FROM Employee WHERE ID=1 OR TRUE
SELECT * FROM Employee WHERE ID=1 or true
SELECT * FROM Employee WHERE ID=1 OR '1'='1'
SELECT * FROM Employee WHERE ID=1 OR 'a'='a'
SELECT * FROM Employee WHERE ID=1 -- bypass
SELECT * FROM Employee WHERE ID=1/*hidden*/
SELECT * FROM Employee WHERE ID=1/**/OR/**/1=1
SELECT * FROM Employee WHERE ID=1 /* comment */ OR 1=1
SELECT * FROM Employee WHERE ID=1;DROP TABLE Employee
SELECT * FROM Employee WHERE ID=1 ; DROP TABLE Employee
SELECT * FROM Employee WHERE ID=2500;DELETE FROM Employee
SELECT * FROM Employee WHERE ID=100; UPDATE Employee SET Name='X'
SELECT * FROM Employee union SELECT password FROM Users
SELECT * FROM Employee WHERE ID=2500 UNION SELECT BankAccount FROM Employee
drop table Employee
delete from Employee where ID=100
update Employee set Name='Hacked' where ID=100
insert into Employee values(9999, 'Fake', 'Fake')
truncate table Employee