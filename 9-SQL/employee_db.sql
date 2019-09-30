--DATA ENGINEERING

drop table employees

create table employees
(emp_no int primary key,
birth_date date,
first_name varchar,
last_name varchar,
gender varchar,
hire_date date);

select * from employees

drop table salaries

create table salaries
(emp_no int,
salary int,
from_date date,
to_date date,
foreign key (emp_no) references employees(emp_no));

select * from salaries

drop table titles

create table titles
(emp_no int,
 title varchar,
from_date date,
to_date date,
foreign key (emp_no) references employees(emp_no));

select * from titles

drop table departments

create table departments
(dept_no varchar(10) primary key,
dept_name varchar(30));

select * from departments

drop table dept_manager

create table dept_manager
(dept_no varchar(10),
emp_no int,
from_date date,
to_date date,
foreign key (dept_no) references departments(dept_no),
foreign key (emp_no) references employees(emp_no));

select * from dept_manager

drop table dept_emp

create table dept_emp
(emp_no int,
dept_no varchar(10),
from_date date,
to_date date,
foreign key (emp_no) references employees(emp_no),
foreign key (dept_no) references departments(dept_no));

select * from dept_emp

--DATA ANALYSIS

--#1
select employees.emp_no, employees.last_name, employees.first_name, employees.gender, salaries.salary
from employees join salaries on employees.emp_no = salaries.emp_no;

--#2 EMPLOYEES HIRED IN 1986
select first_name, last_name, hire_date
from employees where hire_date between '1986-01-01' and '1986-12-30';

--#3
select departments.dept_no, departments.dept_name, dept_manager.emp_no, dept_manager.from_date, dept_manager.to_date,employees.last_name, employees.first_name
from departments inner join dept_manager on departments.dept_no = dept_manager.dept_no
join employees on dept_manager.emp_no = employees.emp_no;

--#4
select employees.emp_no, employees.last_name, employees.first_name, departments.dept_name
from departments join dept_manager on departments.dept_no = dept_manager.dept_no
join employees on dept_manager.emp_no = employees.emp_no;

--#5
select * from employees where first_name = 'Hercules' and last_name like 'B%'

--#6
select employees.emp_no, employees.last_name, employees.first_name, departments.dept_name
from departments
join dept_manager on departments.dept_no = dept_manager.dept_no
join dept_emp on dept_manager.dept_no = dept_emp.dept_no
join employees on dept_manager.emp_no = employees.emp_no
where dept_emp.dept_no = 'd007'

--#7
select employees.emp_no, employees.last_name, employees.first_name, departments.dept_name
from departments
join dept_manager on departments.dept_no = dept_manager.dept_no
join dept_emp on dept_manager.dept_no = dept_emp.dept_no
join employees on dept_manager.emp_no = employees.emp_no
where dept_emp.dept_no = 'd005' or dept_emp.dept_no = 'd007'

--#8
select employees.last_name, count(employees.last_name)
from employees group by last_name
order by count desc
