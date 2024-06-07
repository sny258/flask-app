import psycopg2

try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432",
        database="testdb"
    )

    cursor = connection.cursor()
    
    # Insert data
    cursor.execute("INSERT INTO testtable (name, age) VALUES (%s, %s)", ("Charlie", 35))
    connection.commit()
    
    # Query data
    cursor.execute("SELECT * FROM testtable;")
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"id: {row[0]}, name: {row[1]}, age: {row[2]}")
    
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
