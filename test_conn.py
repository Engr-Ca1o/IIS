from db_connector import connect_to_database

print("Testing connection to database...")

conn = connect_to_database()

if conn:
    print("Connection successful!")
    conn.close()
else:
    print("Connection failed.")

print("Test complete.")
