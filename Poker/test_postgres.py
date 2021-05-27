#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import the connect library from psycopg2
from psycopg2 import connect

table_name = "tickets"
print(1)
# declare connection instance
# conn = connect("host=172.17.0.2 dbname=demo user=postgres password=password")
conn = connect(
    dbname = "demo",
    user = "postgres",
    host = "localhost",
    password = "password",
    port=5432
)
print(2)
# declare a cursor object from the connection
cursor = conn.cursor()
print(3)
# execute an SQL statement using the psycopg2 cursor object
cursor.execute(f"SELECT * FROM {table_name};")
print(4)
# enumerate() over the PostgreSQL records
for i, record in enumerate(cursor):
    print ("\n", type(record))
    print ( record )

# close the cursor object to avoid memory leaks
cursor.close()

# close the connection as well
conn.close()