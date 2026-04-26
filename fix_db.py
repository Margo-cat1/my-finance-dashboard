import sqlite3

# Принудительно создаем файл и таблицу
conn = sqlite3.connect('finance.db')
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
print("Файл finance.db успешно создан!")