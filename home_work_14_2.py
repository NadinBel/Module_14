import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

cursor.execute("DELETE FROM Users WHERE id = ?", ('6',))
cursor.execute('SELECT COUNT(*) FROM Users')
count_users = cursor.fetchone()[0]
cursor.execute('SELECT SUM(balance) FROM Users')
sum_balance = cursor.fetchone()[0]
cursor.execute('SELECT AVG(balance) FROM Users')
avg_balance = cursor.fetchone()[0]
print(avg_balance)
print(sum_balance/count_users)

connection.commit()
connection.close()