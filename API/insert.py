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

def add_module(id,name,year,code,userid):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO modules (moduleid, name, year, code, mark,userid)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            id,
            name,
            year,
            code,
            0,
            userid
        ))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            
def add_Assingment(name,desc,date,userid,Assign_id,module_id,weighting):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO assignments (assignid, name, description, duedate, userid,moduleid,mark,weighting)
        VALUES (%s, %s, %s, %s, %s, %s,%s,%s)
        """
        cursor.execute(insert_query, (
            Assign_id,
            name,
            desc,
            date,
            userid,
            module_id,
            0,
            weighting
        ))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            
def add_test(name,date,test_id,module_id,user_id,weighting):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO tests (testid, name, date, userid, moduleid,mark,weighting)
        VALUES (%s, %s, %s, %s, %s, %s,%s)
        """
        cursor.execute(insert_query, (
            test_id,
            name,
            date,
            user_id,
            module_id,
            0,
            weighting
        ))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            
def update_Assignment(assign_id,module_id,user_id,mark,name):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        update_query = """
        UPDATE assignments 
        SET mark = %s
        WHERE name = %s AND assignid = %s AND userid = %s AND moduleid = %s
        """
        cursor.execute(update_query, (
            mark,
            name,
            assign_id,
            user_id,
            module_id
        ))
        connection.commit()
        cursor.execute("SELECT * FROM assignments WHERE assignid = %s", (assign_id,))
        updated_data = cursor.fetchone()
        print("Updated Data:", updated_data)
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")
        
def update_Test(mark,name,test_id,user_id,module_id):
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        update_query = """
        UPDATE tests
        SET mark = %s
        WHERE name = %s AND testid = %s AND userid = %s AND moduleid = %s
        """
        cursor.execute(update_query, (
            mark,
            name,
            test_id,
            user_id,
            module_id
        ))
        connection.commit()
        cursor.execute("SELECT * FROM assignments WHERE assignid = %s", (assign_id,))
        updated_data = cursor.fetchone()
        print("Updated Data:", updated_data)
    except (Exception, psycopg2.Error) as error:
        print(f"Error: {error}")        