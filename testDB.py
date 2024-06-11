import sqlite3

def access_db():
    # Connect to the database
    conn = sqlite3.connect('database.db')
    # Create a cursor
    cur = conn.cursor()

    # users data
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    print('users table data')
    print('----------------')
    for row in rows:
        print(row)

    # bookings data
    print(' ')
    print('bookings table data')
    print('----------------')
    cur.execute('SELECT * FROM bookings')
    rows = cur.fetchall()
    for row in rows:
        print(row)

    # print(' ')
    # print('deleting bookings table data')
    # print('----------------')
    # cur.execute('DELETE FROM bookings')
    # conn.commit()
    # print('bookings table data Deleted !!!')

    # # bookings data
    # print(' ')
    # print('deleting the booking table')
    # print('----------------')
    # cur.execute('DROP TABLE IF EXISTS bookings')
    # print('bookings table Deleted !!!')

    conn.close()

if __name__ == '__main__':
    access_db()