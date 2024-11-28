import pymysql as mq

myobj=mq.connect(host="localhost:3307",user="root",password="12345678")
cursorobj=myobj.cursor()
try:
    db = "create database pythonproject"
    cursorobj.execute(db)
    print("Database Created")
except:
    print("Database error")