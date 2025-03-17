import pymysql
import pymysql.cursors

def connect_to_database(user_role="student"):
    # Choose credentials based on role
    if user_role.lower() == "admin":
        username = "adminuser"      # Replace with your admin username
        password = "adminpassword"  # Replace with your admin password
    else:
        username = "clientuser"      # Replace with your student username
        password = "clientpassword"  # Replace with your student password\

    try:
        conn = pymysql.connect(
            host="172.16.1.109",    # or your server's IP
            user=username,
            password=password,
            database="sis",
            cursorclass=pymysql.cursors.DictCursor,  # Use dictionary cursors
        )
        return conn
    except Exception as e:
        print(e)
        return None
