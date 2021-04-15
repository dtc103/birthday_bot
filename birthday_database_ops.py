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

    database_connection.commit()

def edit_birthday(database_connection, userid: int, day: int, month: int, year: int, timezone: str=None):
    db_cursor = database_connection.cursor()
    
    birthday = f"{day}-{month}-{year}"

    if timezone is not None:
        stmt = """UPDATE birthdays SET birthday=?, timezone=? WHERE userid=?;"""
        db_cursor.execute(stmt, (birthday, timezone, str(userid)))
    else:
        stmt = """UPDATE birthdays SET birthday=?, timezone=NULL WHERE userid=?;"""
        db_cursor.execute(stmt, (birthday, str(userid)))
    
    database_connection.commit()

def remove_birthday(database_connection, userid: int):
    db_cursor = database_connection.cursor()

    stmt = """DELETE FROM birthdays WHERE userid=?;"""
    db_cursor.execute(stmt, (str(userid), ))

    database_connection.commit()

def get_birthday_users(database_connection):
    db_cursor = database_connection.cursor()
    
    stmt = "SELECT userid FROM birthdays;"
    db_cursor.execute(stmt)

    userids = []

    for userid in db_cursor:
        userids.append(userid[0])

    return userids

def get_admin_roles(databse_connection):
    db_curosr = database_connection.cursor()

    stmt = "SELECT roleid FROM admin_roles;"
    db_cursor.execute(stmt)

    roleids = []

    for roleid in db_cursor:
        roleids.append(roleid[0])
    
    return roleids
