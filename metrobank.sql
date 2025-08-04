-- create all tables (customer, transaction, employee, loan, branches)
-- REMEMBER COLUMN CREATION SEQUENCE: column name, data type, constraint
-- DATA DEFINITION LANGUAGES (DDL)
CREATE TABLE Customer (
	customer_id int primary key,
	first_name varchar(255) null,
	last_name varchar(255) null,
	date_of_birth date not null,
	address text null,
	phone_number varchar(20) null,
	city varchar(50) null
);

SELECT * FROM customer;

CREATE TABLE accounts(
	account_number int primary key,
	customer_id int,
	account_type varchar(255) not null,
	balance decimal(15,2) not null,
	date_opened timestamp not null,
	foreign key (customer_id) references customer (customer_id)
);

CREATE TABLE branches (
	branch_id int primary key,
	branch_name varchar(255) not null,
	branch_address text not null,
	branch_phone_number varchar(20) null
);

CREATE TABLE transactions (
	transaction_id int primary key,
	account_number int, 
	transaction_type varchar(50) not null,
	amount decimal(15,2) not null,
	transaction_date timestamp not null,
	foreign key (account_number) references accounts (account_number)
);

CREATE TABLE employees (
	employee_id int primary key,
	name varchar(255) not null,
	position varchar(255) not null,
	branch_id int,
	hire_date date not null,
	foreign key (branch_id) references branches (branch_id)
);

CREATE TABLE loan (
	loan_id int primary key,
	customer_id int, 
	loan_amount decimal(15,2) not null,
	loan_type varchar(50) null,
	issue_date date not null,
	interest_rate decimal(3,2) not null,
	foreign key (customer_id) references customer (customer_id)
);



ALTER TABLE customer
	Add email varchar(100) not null;

ALTER TABLE loan
	ALTER COLUMN interest_rate TYPE float;

-- You can use either of the two below
ALTER TABLE customer
	DROP column phone_number,
	Add column phone_number varchar(45) UNIQUE; 

ALTER TABLE customer 
	ADD UNIQUE (phone_number); 

ALTER TABLE accounts
	ADD COLUMN branch_id int,
	ADD foreign key (branch_id) references branches (branch_id);


-- DATA MANIPULATION LANGUAGE (DML)
SELECT * FROM customer;
INSERT INTO customer (customer_id, first_name, last_name, date_of_birth, address, city, email, phone_number) 
	VALUES
	(1, 'MUSA', 'AJIYA', '1999-01-04', 'MUSAWA ADDRESS', 'ABUJA', 'musa@gmail.com', '+234908809087'),
	(2, 'ISA', 'KB', '1914-01-01', 'LAGOS STATE', 'LAGOS', 'isalagos@gmail.com', '+234904014044');

TRUNCATE customer;

SELECT * FROM branches;
INSERT INTO branches VALUES (1, 'Ikeja Branch', '101, 2A, Ikeja', '+234090908765');

SELECT * FROM accounts;
INSERT INTO accounts VALUES ('123123223', 1, 'current', '500', '2001-01-02', 1)

UPDATE accounts SET balance = '2420' WHERE customer_id = 1;

DELETE FROM accounts WHERE customer_id = '20';

TRUNCATE TABLE loan;

-- NOTE: 
-- Data in a parent (upstream) table cannot be deleted if there are related rows in a child (downstream) 
-- table that reference it via a foreign key constraint, unless:
-- You first delete the dependent rows in the child table, or
-- The foreign key is defined with ON DELETE CASCADE, or
-- You temporarily drop or disable the constraint.

-- You can delete rows in a downstream (child) table that reference an upstream (parent) table, 
-- without affecting the parent table.


-- IMPORTING DATA
-- Use the Import/Export function after right clicking the table on the GUI 

