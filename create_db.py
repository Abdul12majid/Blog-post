import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "Non12$ense")

my_cursor = mydb.cursor()
my_cursor.execute("CREATE DATABASE fits")
my_cursor.execute("SHOW DATABASES")

for db in my_cursor:
	print(db)