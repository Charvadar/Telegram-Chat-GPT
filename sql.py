import sqlite3 as sq
import pandas as pd

def upd(date, user_id, request, response):
    #query = f'INSERT INTO requests VALUES (?, ?, ?);'
    con = sq.connect('tbot.db')
    c = con.cursor()
    c.execute('INSERT INTO requests VALUES (?, ?, ?, ?)', (date, user_id, request, response))
    con.commit()
    con.close()
    print(f'-----DATABASE UPDATE-----\nDate:     {date}\nUser ID:  {user_id}\nRequest:  {request}\nResponse: {response}')

def getuser(user_id):
    conn = sq.connect('tbot.db')
    query = f"SELECT * FROM users WHERE user_id ='{user_id}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    if len(df) > 0:
        return df.conversation[0], df.premium[0]
    else:
        return 'na', 'na'
    
def new_user(user_id, user_name):
    con = sq.connect('tbot.db')
    c = con.cursor()
    c.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (user_id, user_name, 'n', 'n'))
    con.commit()
    con.close()
    print(f'------NEW USER------\nUser ID:  {user_id}\nUser Name: {user_name}')

def get_conversation(user_id):
    conn = sq.connect('tbot.db')
    query = f"SELECT * FROM requests WHERE user_id ='{user_id}'"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.tail(3).reset_index(drop=True)