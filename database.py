import sqlite3
import pandas as pd

def create_connection():
    # Создает файл базы данных finance.db, если его нет
    conn = sqlite3.connect('finance.db', check_same_thread=False)
    return conn

def init_db():
    conn = create_connection()
    c = conn.cursor()
    # Таблица для хранения финансовых записей
    c.execute('''
        CREATE TABLE IF NOT EXISTS finance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            date TEXT,
            cash REAL,
            receivables REAL,
            inventory REAL,
            fixed_assets REAL,
            short_term_debt REAL,
            long_term_debt REAL,
            revenue REAL,
            ebitda REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_record(username, data_dict):
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO finance_records (
            username, date, cash, receivables, inventory, 
            fixed_assets, short_term_debt, long_term_debt, revenue, ebitda
        ) VALUES (?, date('now'), ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        username,
        data_dict['cash'], data_dict['receivables'], data_dict['inventory'],
        data_dict['fixed_assets'], data_dict['short_term_debt'],
        data_dict['long_term_debt'], data_dict['revenue'], data_dict['ebitda']
    ))
    conn.commit()
    conn.close()

def get_latest_record(username):
    conn = create_connection()
    # Читаем данные сразу в Pandas — так удобнее для Streamlit
    query = f"SELECT * FROM finance_records WHERE username = '{username}' ORDER BY id DESC LIMIT 1"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

  def get_balance():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    # Считаем сумму всех операций (доходы плюс, расходы минус)
    cursor.execute("SELECT SUM(amount) FROM operations")
    result = cursor.fetchone()[0]
    conn.close()
    return result if result is not None else 0
