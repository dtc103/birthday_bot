import sqlite3
import datetime

def save_birthday(database_connection, userid: int, username: str, day: int, month: int, timezone: str=None):
    db_cursor = database_connection.cursor()

    #date = f"{day}-{month}-{year}"
    birthday = datetime.datetime(2000, month, day).strftime("%d-%m")

    if timezone is not None:
        stmt = "INSERT INTO birthdays (userid, username, birthday, is_congratulated, timezone) VALUES(?, ?, ?, false, NULL);"
        db_cursor.execute(stmt, (str(userid), username, birthday))
    else:
        stmt = "INSERT INTO birthdays (userid, username, birthday, is_congratulated, timezone) VALUES(?, ?, ?, false, ?);"
        db_cursor.execute(stmt, (str(userid), username, birthday, timezone))

    database_connection.commit()

def edit_birthday(database_connection, userid: int, day: int, month: int, timezone: str=None):
    db_cursor = database_connection.cursor()
    
    #birthday = f"{day}-{month}-{year}"
    birthday = datetime.datetime(2000, month, day).strftime("%d-%m")

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
    
    stmt = "SELECT userid, birthday, is_congratulated, timezone FROM birthdays;"
    db_cursor.execute(stmt)

    userids = []

    for userinfo in db_cursor:
        userids.append((userinfo[0], userinfo[1], userinfo[2], userinfo[3]))

    return userids

def get_admin_roles(database_connection):
    db_curosr = database_connection.cursor()

    stmt = "SELECT roleid FROM admin_roles;"
    db_cursor.execute(stmt)

    roleids = []

    for roleid in db_cursor:
        roleids.append(roleid[0])
    
    return roleids

def set_congratulated(database_connection, userid:int, state: bool):
    db_cursor = database_connection.cursor()

    stmt = """UPDATE birthdays SET is_congratulated=? WHERE userid=?;"""
    db_cursor.execute(stmt, (state, userid))

    database_connection.commit()

def get_bd_channel(database_connection):
    db_cursor = database_connection.cursor()

    stmt = """SELECT messageid, channelid FROM message_info;"""
    db_cursor.execute(stmt)

    messageids = []

    for messagid, channelid in db_cursor:
        messageids.append((messagid, channelid))

    return messageids

def set_bd_channel(database_connection, messageid, former_messageid, channelid):
    db_cursor = database_connection.cursor()

    if former_messageid is not None:
        stmt = """UPDATE message_info SET messageid=?, channelid=? WHERE messageid=?;"""
        db_cursor.execute(stmt, (str(messageid), str(channelid), str(former_messageid)))
    else:
        stmt = """INSERT INTO message_info (messageid, channelid) VALUES(?, ?);"""
        db_cursor.execute(stmt, (str(messageid), str(channelid)))

    database_connection.commit()

