import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY, username TEXT NOT NULL, 
email TEXT NOT NULL, age INTEGER, balance INTEGER NOT NULL)''')

'''for item in range(1, 11):
    cursor.execute("INSERT INTO users (username, email, age, balance) VALUES (?, ?, ?, ?)", (f'User{item}',
                                         f'example{item}@gmail.com', f'{item*10}', '1000',))

for i in range(1, 11, 2):
    cursor.execute("UPDATE Users SET balance = ? WHERE id = ?", (500, f'{i}'))

for i in range(1, 11, 3):
    cursor.execute("DELETE FROM Users WHERE id = ?", (f'{i}',))'''

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
data = cursor.fetchall()
for i in data:
    print(f'Имя: {i[0]} | Почта: {i[1]} | Возраст: {i[2]} | Баланс: {i[3]}')
connection.commit()
connection.close()