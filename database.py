import sqlite3
from datetime import datetime

def create_connection():
    return sqlite3.connect('finance.db', check_same_thread=False)

def init_db():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS finance_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT, date TEXT, cash REAL, receivables REAL, 
                    inventory REAL, fixed_assets REAL, short_term_debt REAL, 
                    long_term_debt REAL, revenue REAL, ebitda REAL, 
                    own_capital REAL, initial_inv REAL
                 )''')
    conn.commit()
    conn.close()

def save_record(username, data_dict):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO finance_records 
                 (username, date, cash, receivables, inventory, fixed_assets, 
                  short_term_debt, long_term_debt, revenue, ebitda, own_capital, initial_inv)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               data_dict['cash'], data_dict['receivables'], data_dict['inventory'],
               data_dict['fixed_assets'], data_dict['short_term_debt'],
               data_dict['long_term_debt'], data_dict['revenue'], data_dict['ebitda'],
               data_dict.get('own_capital', 1000000.0), data_dict.get('initial_inv', 1500000.0)))
    conn.commit()
    conn.close()

def get_latest_record(username):
    conn = create_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    # ВНИМАНИЕ: Проверь, чтобы тут было finance_records
    c.execute("SELECT * FROM finance_records WHERE username = ? ORDER BY id DESC LIMIT 1", (username,))
    row = c.fetchone()
    conn.close()
    return row

def get_all_records(username):
    conn = create_connection()
    import pandas as pd
    # Берем данные для графиков и истории
    query = "SELECT date, cash, receivables, fixed_assets, own_capital FROM finance_records WHERE username = ? ORDER BY id DESC"
    df = pd.read_sql_query(query, conn, params=(username,))
    conn.close()
    return df