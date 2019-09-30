create table employees
(emp_no int primary key,
birth_date date,
first_name varchar,
last_name varchar,
gender varchar,
hire_date date);

create table salaries
(emp_no int,
salary int,
from_date date,
to_date date,
foreign key (emp_no) references employees(emp_no));

create table titles
(emp_no int,
 title varchar,
from_date date,
to_date date,
foreign key (emp_no) references employees(emp_no));

create table departments
(dept_no varchar(10) primary key,
dept_name varchar(30));

create table dept_manager
(dept_no varchar(10),
emp_no int,
from_date date,
to_date date,
foreign key (dept_no) references departments(dept_no),
foreign key (emp_no) references employees(emp_no));

create table dept_emp
(emp_no int,
dept_no varchar(10),
from_date date,
to_date date,
foreign key (emp_no) references employees(emp_no),
foreign key (dept_no) references departments(dept_no));

