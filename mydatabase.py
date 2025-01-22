import mysql.connector


def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="user_commands_db"
    )


def save_command_to_db(command, response=None):
    try:
        db = connect_to_db()
        cursor = db.cursor()
        query = "INSERT INTO commands (command, response) VALUES (%s, %s)"
        cursor.execute(query, (command, response))
        db.commit()
        cursor.close()
        db.close()
        print("Command saved successfully!")
    except Exception as e:
        print(f"Error saving command to database: {e}")


def fetch_commands_from_db():
    try:
        db = connect_to_db()
        cursor = db.cursor()
        query = "SELECT * FROM commands"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return results
    except Exception as e:
        print(f"Error fetching commands from database: {e}")
        return []
