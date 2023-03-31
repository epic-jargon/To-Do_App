import sqlite3

# query database
def query_database(command):
    # create a database and/or connect
    conn = sqlite3.connect("data.db")

    # create instance of cursor
    c = conn.cursor()

    c.execute(command)
    records = c.fetchall()

    # commit changes
    conn.commit()

    # close connection
    conn.close()

    return records

def query_database_many(command, list):
    # create a database and/or connect
    conn = sqlite3.connect("data.db")

    # create instance of cursor
    c = conn.cursor()

    c.executemany(command, [(a,) for a in list])

    # commit changes
    conn.commit()

    # close connection
    conn.close()


