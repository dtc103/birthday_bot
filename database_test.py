import sqlite3
import random
import datetime

def fill_random_values(database_connection, value_count):
    db_cursor = database_connection.cursor()

    stmt = "INSERT INTO birthdays (userid, username, birthday, is_congratulated, timezone) VALUES(?, ?, ?, ?, NULL);"

    for _ in range(0, value_count):
        date = datetime.datetime(2000, random.randrange(1, 13), random.randrange(1, 32)).strftime("%d-%m")
        db_cursor.execute(stmt, (str(random.randrange(0, 1000000000)), "examplename", date, False))
        
    database_connection.commit()

def delete_table(database_connection):
    db_cursor = database_connection

    stmt1 = "DELETE FROM birthdays;"
    db_cursor.execute(stmt1)

    database_connection.commit()



