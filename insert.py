import sqlite3

conn=sqlite3.connect("Database.db")
con=conn.cursor()

users=[("admin","admin123"),
       ("keerti","keerti123"),
       ("aniket","aniket123"),
       ("tushar","tushar123")]

conn.executemany("INSERT INTO AUTHENTICATION VALUES(?,?)", users)
conn.commit()
conn.close()