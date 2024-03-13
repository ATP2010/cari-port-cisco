#import mysql.connector
import socket

""" mydb = mysql.connector.connect(
    host = "10.194.7.73",
    user = "contactcenter",
    password = "admin",
    database = "maincc147"
)

mycursor = mydb.cursor()

sql = "INSERT INTO `maincc147`.`sephia_logpc`(`ipAddr`, `loginTime`, `status`) VALUES ('1.1.1.1', (select now()), 'Login') ON DUPLICATE KEY UPDATE loginTime = (SELECT now()), logoutTime = 'NULL', status = 'Login'"
mycursor.execute(sql)

mydb.commit() """

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
print(s.gethostbyname())
s.close()