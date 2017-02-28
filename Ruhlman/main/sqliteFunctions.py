#sqliteFunctions.py

# two functions to easily execute sql code from sqlite

# code copied from the following url
# http://code.runnable.com/Ur8myPOxx4hmAARP/using-full-text-search-with-python-and-sqlite-for-tutorial-beginner-sqlite3-fts-database-query-and-fts4
# July 13, 2016

def exeSql(sql,conn):
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()


def selectSql(sql,conn,params=None):
    c = conn.cursor()
    if params:
        c.execute(sql, params)
    else:
        c.execute(sql)

    return c.fetchall()
