CREATE TABLE DEPT(
    DEPTNO NUMBER(2) CONSTRAINT PK_DEPT PRIMARY KEY, -- код департамента
    DNAME VARCHAR(14),                               -- название департамента
    LOC VARCHAR(13) );                               -- местонахождение 
 
CREATE TABLE EMP( 
    EMPNO NUMBER(4) CONSTRAINT PK_EMP PRIMARY KEY,    -- код сотрудника
    ENAME VARCHAR(10),                                -- имя сотрудника   
    JOB VARCHAR(9),                                   -- должность 
    MGR NUMBER(4),                                    -- руководитель
    HIREDATE DATE,                                    -- дата устройства на работу  
    SAL NUMBER(7,2),                                  -- зарплата  
    COMM NUMBER(7,2),                                 -- премия
    DEPTNO NUMBER(2) CONSTRAINT FK_DEPTNO REFERENCES DEPT);  -- код департамента
 
CREATE TABLE SALGRADE( 
    GRADE NUMBER,
    LOSAL NUMBER,
    HISAL NUMBER );
 