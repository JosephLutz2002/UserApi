import psycopg2

# Database connection parameters
db_params = {
    "dbname": "mkdown",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": "5432"
}
def insert_user(user_data):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO users (userid, usern, pass, email)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            user_data["userid"],
            user_data["user"],
            user_data["pass"],
            user_data["email"]
        ))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            
def get_user(username,password):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        insert_query = """
        SELECT * FROM users WHERE usern = %s  AND pass  = %s
        """
        cursor.execute(insert_query, (
            username,password
        ))
        result = cursor.fetchall()
        return result
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            
def validate_unique_user(username):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        insert_query = """
        SELECT * FROM users WHERE usern = %s
        """
        cursor.execute(insert_query, (
            username,  # Provide the username as a tuple
        ))
        result = cursor.fetchall()
        if len(result) > 0:
            return False
        return True
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

