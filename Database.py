import sqlite3

conn=sqlite3.connect("Database.db")
con=conn.cursor()
athen="""CREATE TABLE  IF NOT EXISTS AUTHENTICATION(USERNAME VARCHAR(20) PRIMARY KEY,PASSWORD VARCHAR(20) NOT NULL)"""
con.execute(athen)
conn.close()