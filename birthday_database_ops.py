import sqlite3

def save_birthday(database_connection, userid: int, username: str, day: int, month: int, year: int, timezone: str=None):
    db_cursor = database_connection.cursor()

    date = f"{day}-{month}-{year}"

    if timezone is not None:
        stmt = "INSERT INTO birthdays (userid, username, birthday, timezone) VALUES(?, ?, ?, NULL);"
        db_cursor.execute(stmt, (str(userid), username, date))
    else:
        stmt = "INSERT INTO birthdays (userid, username, birthday, timezone) VALUES(?, ?, ?, ?);"
        db_cursor.execute(stmt, (str(userid), username, date, timezone))

    self.birthday_database_connection.commit()

def edit_birthday(database_connection, userid: int, day: int, month: int, year: int, timezone: str=None):
    db_cursor = database_connection.cursor()
    
    if timezone is not None:
        stmt = """UPDATE birthdays SET day=?, month=?, year=?, timezone=? WHERE userid=?;"""
        db_cursor.execute(stmt, (day, month, year, timezone, str(userid)))
    else:
        stmt = """UPDATE birthdays SET day=?, month=?, year=?, timezone=NULL WHERE userid=?;"""
        db_cursor.execute(stmt, (day, month, year, str(userid)))
    
    self.database_connections.commit()

def remove_birthday(database_connection, userid: int):
    db_cursor = database_connection.cursor()

    stmt = """DELETE FROM birthdays WHERE userid=?;"""
    db_cursor.execute(stmt, (str(user)))

    self.birthday_database_connection.commit()

def get_birthday_users(database_connection):
    db_cursor = database_connection.cursor()
    
    stmt = "SELECT userid FROM birthdays;"
    cursor.execute(stmt)

    userids = []

    for userid in cursor.fetchall():
        users.append(userid[0])

    return userids

