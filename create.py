import pymysql as mq

conn=mq.connect(host="localhost",user="root",password="12345678",database="pythonproject")

mysqlc=conn.cursor()

tc="create table teacher(teacher_id varchar(10),name varchar(50), age varchar(20), gender varchar(15),branch varchar(50),dateOfBirth varchar(20))"

mysqlc.execute(tc)