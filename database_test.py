import sqlite3
import random

def fill_random_values(database_connection, value_count):
    db_cursor = database_connection.cursor()

    stmt = "INSERT INTO birthdays (userid, username, birthday, timezone) VALUES(?, ?, ?, NULL);"

    for _ in range(0, value_count):
        db_cursor.execute(stmt, (str(random.randrange(0, 1000000000)), "examplename", f"{random.randrange(1, 32)}-{random.randrange(1, 13)}-{random.randrange(1900, 9999)}"))
        
    database_connection.commit()

def delete_table(database_connection):
    db_cursor = database_connection

    stmt1 = "DELETE FROM birthdays;"
    db_cursor.execute(stmt1)

    database_connection.commit()



