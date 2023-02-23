SELECT * FROM HR.EMPLOYEES;
select * from HR.departments;

CREATE TABLE STG_EMPLOYEES as select * from hr.employees where 1=2;
CREATE TABLE STG_DEPARTMENT AS SELECT * FROM HR.DEPARTMENTS WHERE 1=2;

select * from stg_employees;
SELECT * FROM STG_DEPARTMENT;

insert into stg_employees 
select * from HR.EMPLOYEES where employee_id between 100 and 110;

commit;

insert into stg_employees 
select Employee_id,INITCAP(first_name),initcap(last_name),email||'@test.com',
substr(phone_number,1,3)||'-'||substr(phone_number,5,3)||'-'||substr(phone_number,9,4) as phone_number,
hire_date,job_id,salary,commission_pct,manager_id,department_id
from HR.EMPLOYEES 
where employee_id between 111 and 121;

commit;

INSERT INTO STG_DEPARTMENT
SELECT * FROM HR.departments;

COMMIT;



