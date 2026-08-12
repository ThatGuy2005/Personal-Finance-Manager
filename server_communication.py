import pyodbc

import os
from dotenv import load_dotenv

load_dotenv()
connection_string = (
    f"Driver={os.getenv('DB_DRIVER')};"
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')};"
    f"TrustServerCertificate={os.getenv('DB_TRUST_SERVER_CERTIFICATE')};"
)

def execute(command: str):
    """Connects to the database and executes a procedure with the given
    arguments. It returns the query results, but not the labels."""
    results = list()
    try:
                # Establish connection
                conn = pyodbc.connect(connection_string)
                cursor = conn.cursor()
        
                # Execute a SQL query
                cursor.execute(command)

                cursor.commit()

    except pyodbc.Error as ex:
                print("An error occurred:", ex)
                return results

    finally:
        # Close the connection
        if 'conn' in locals():
            conn.close()
        return results

def connect_and_execute(command: str, *args):
    """Connects to the database and executes a procedure with the given
    arguments. It returns the query results, but not the labels."""
    results = list()
    try:
                # Establish connection
                conn = pyodbc.connect(connection_string)
                cursor = conn.cursor()
        
                # Execute a SQL query
                cursor.execute(command,
                           *args)

                # Fetch results
                for row in cursor:
                    results.append(row)

                cursor.commit()

    except pyodbc.Error as ex:
                print("An error occurred:", ex)
                return results

    finally:
        # Close the connection
        if 'conn' in locals():
            conn.close()
        return results
    
def connect_and_execute_with_labels(command: str, *args):
    """Connects to the database and executes a procedure with the given
    arguments. It returns the query results and the labels."""
    results = list()
    labels = list()
    try:
                # Establish connection
                conn = pyodbc.connect(connection_string)
                cursor = conn.cursor()
                

                # Execute a SQL query
                cursor.execute(command,
                           *args)

                # Fetch results
                labels = [column[0] for column in cursor.description]

                for row in cursor:
                    results.append(row)

                cursor.commit()

    except pyodbc.Error as ex:
                print("An error occurred:", ex)
        
                return results,labels

    finally:
        # Close the connection
        if 'conn' in locals():
            conn.close()
        return results,labels

def connect_and_insert(command: str, *args):
    """Connects to the database and executes a insert with the given
    arguments."""
    try:
                # Establish connection
                conn = pyodbc.connect(connection_string)
                cursor = conn.cursor()
        
                # Execute a SQL query
                cursor.execute(command,
                           *args)

                # Fetch results

                cursor.commit()

    except pyodbc.Error as ex:
                print("An error occurred:", ex)

    finally:
        # Close the connection
        if 'conn' in locals():
            conn.close()

def read_data(email, command):
    data, labels = connect_and_execute_with_labels(command, email)
    return data, labels
    
def get_currency_options():
    results = list()
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENCY_ID, NAME FROM Currency")
        results = [(row[0], str(row[1])) for row in cursor]
    except pyodbc.Error as ex:
        print("SQL Error fetching currencies:", ex)
    finally:
        if 'conn' in locals(): conn.close()
        return results

def get_account_options(email):
    results = list()
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        cursor.execute("EXEC GetAccountCurrency @EMAIL=?", email)
        results = [(row[0], str(row[1])) for row in cursor]
    except pyodbc.Error as ex:
        print("SQL Error fetching accounts:", ex)
    finally:
        if 'conn' in locals(): conn.close()
        return results   
    
def get_goal_options():
    results = list()
    try:
         conn = pyodbc.connect(connection_string)
         cursor = conn.cursor()
         cursor.execute("SELECT SAVING_GOAL_ID, NAME FROM SavingGoals")
         results = [(row[0], str(row[1])) for row in cursor]
    except pyodbc.Error as ex:
         print("SQL Error fetching goals:",ex)
    finally:
         if 'conn' in locals(): conn.close()
         return results
    
def get_categories():
    results = list()
    try:
         conn = pyodbc.connect(connection_string)
         cursor = conn.cursor()
         cursor.execute("SELECT CATEGORY_ID, NAME FROM Categories")
         results = [(row[0], str(row[1])) for row in cursor]
    except pyodbc.Error as ex:
         print("SQL Error fetching categories:",ex)
    finally:
         if 'conn' in locals(): conn.close()
         return results

def get_frequencies():
    results = list()
    try:
         conn = pyodbc.connect(connection_string)
         cursor = conn.cursor()
         cursor.execute("SELECT FREQUENCY_ID, NAME FROM Frequencies")
         results = [(row[0], str(row[1])) for row in cursor]
    except pyodbc.Error as ex:
         print("SQL Error fetching frequencies:",ex)
    finally:
         if 'conn' in locals(): conn.close()
         return results

def get_account_currencies(email):
    results = list()
    results = connect_and_execute("EXEC GetAccountCurrency @EMAIL=?",email)
    return results

def get_purpose_options():
     results = list()
     results = connect_and_execute("EXEC GetPurposes")
     return results

def get_account_currency_with_id(acc_id):
    results = list()
    results = connect_and_execute("SELECT CURRENCY_ID FROM accounts WHERE ACCOUNT_ID=?",acc_id)
    if results:
        return results[0][0]
    else:
        return ""
    
def get_subcategories():
    results = list()
    try:
         conn = pyodbc.connect(connection_string)
         cursor = conn.cursor()
         cursor.execute("SELECT SUBCATEGORY_ID, NAME FROM Subcategories")
         results = [(row[0], str(row[1])) for row in cursor]
    except pyodbc.Error as ex:
         print("SQL Error fetching subcategories:",ex)
    finally:
         if 'conn' in locals(): conn.close()
         return results
    
def get_directions():
    results = list()
    try:
         conn = pyodbc.connect(connection_string)
         cursor = conn.cursor()
         cursor.execute("SELECT DIRECTION_ID, TYPE FROM Direction")
         results = [(row[0], str(row[1])) for row in cursor]
    except pyodbc.Error as ex:
         print("SQL Error fetching subcategories:",ex)
    finally:
         if 'conn' in locals(): conn.close()
         return results
    
def connect_and_delete(command, *args):
    try:
         conn = pyodbc.connect(connection_string)
         cursor = conn.cursor()
         # expand args so parameters are passed correctly to pyodbc
         cursor.execute(command, *args)
         cursor.commit()
    except pyodbc.Error as ex:
         print("SQL Error in connect_and_delete:", ex)
    finally:
         if 'conn' in locals(): conn.close()