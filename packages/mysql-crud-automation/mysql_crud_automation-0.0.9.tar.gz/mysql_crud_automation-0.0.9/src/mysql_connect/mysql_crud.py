import mysql.connector
from mysql.connector import Error
import pandas as pd
import json
from ensure import ensure_annotations
from typing import Tuple, Optional , List , Union


class mysql_operation:
    @ensure_annotations 
    def __init__(self, host: str, user: str, password: str):
        self.host = host
        self.user = user
        self.password = password
    
    @ensure_annotations 
    def create_connection(self):
        """Create a MySQL connection."""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
            )
            if connection.is_connected():
                print("Connected to MySQL database")
            return connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            return None

    @ensure_annotations 
    def create_database(self,database_name:Optional[str] = None):
        """Create a MySQL database if it doesn't exist."""
        connection = None
        cursor = None
        
        try:
            # Connect to the MySQL server (no specific database mentioned yet)
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                print("Connected to MySQL server")

            cursor = connection.cursor()

            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
            print(f"Database '{database_name}' created or already exists.")

        except Error as e:
            print(f"Error creating database: {e}")

        finally:
            # Close cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            print("MySQL connection is closed.")
            
    @ensure_annotations 
    def create_table(self, create_table_sql: str,database_name:Optional[str] = None):
        """Create a table in the specified MySQL database using a SQL query."""
        connection = None
        cursor = None
        
        try:
            # Connect to the MySQL server (specify the database now)
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=database_name  # Now include the database name
            )
            if connection.is_connected():
                print(f"Connected to MySQL database: {database_name}")

            cursor = connection.cursor()
            cursor.execute(create_table_sql)
            print("Table created successfully.")
            return True
            
        except Error as e:
            print(f"Error creating table: {e}")
            return None 
            
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
            print("MySQL connection is closed.")
            
    @ensure_annotations 
    def insert_single_record(self, record: dict,table_name: Optional[str] = None,database_name:Optional[str] = None):
        """Insert a single record into the specified MySQL table."""
        # Connect to MySQL
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=database_name
        )
        cursor = connection.cursor()

        # Prepare SQL for inserting a single record
        columns = ', '.join(record.keys())
        placeholders = ', '.join(['%s'] * len(record))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Extract the values as a tuple
        values = tuple(record.values())

        cursor.execute(sql, values)

        # Commit the transaction
        connection.commit()
        print(f"Single record inserted into {table_name}.")

        # Close the cursor and connection
        cursor.close()
        connection.close()
    
    @ensure_annotations 
    def insert_multiple_records(self, records: List[dict], table_name: Optional[str] = None,database_name:Optional[str] = None):
        """Insert multiple records into the specified MySQL table."""
        if not records:
            print("No records provided to insert.")
            return

        # Connect to MySQL
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=database_name
        )
        cursor = connection.cursor()

        # Prepare SQL for inserting multiple records
        columns = ', '.join(records[0].keys())
        placeholders = ', '.join(['%s'] * len(records[0]))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Extract the values for each record as tuples
        values_list = [tuple(record.values()) for record in records]

        cursor.executemany(sql, values_list)

        # Commit the transaction
        connection.commit()
        print(f"Multiple records inserted into {table_name}.")

        # Close the cursor and connection
        cursor.close()
        connection.close()

    @ensure_annotations 
    def bulk_insert(self, datafile: str, table_name: Optional[str] = None, database_name:Optional[str] = None,unique_field: Optional[str] = None):
        """Bulk insert records from a CSV or Excel file."""
        connection = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.password,
        database=database_name  # Specify the database here
        )
        
        cursor = connection.cursor()

        if datafile.endswith('.csv'):
            data = pd.read_csv(datafile)
        elif datafile.endswith('.xlsx'):
            data = pd.read_excel(datafile)
        
        data_json = json.loads(data.to_json(orient='records'))

        for record in data_json:
            columns = ', '.join(record.keys())
            placeholders = ', '.join(['%s'] * len(record))
            if unique_field:
                select_query = f"SELECT COUNT(*) FROM {table_name} WHERE {unique_field} = %s"
                cursor.execute(select_query, (record[unique_field],))
                result = cursor.fetchone()
                
                if isinstance(result, tuple) and result[0] == 0:
                    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                    cursor.execute(sql, tuple(record.values()))
                else:
                    print(f"Record with {unique_field}={record[unique_field]} already exists. Skipping insertion.")
            else:
                sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, tuple(record.values()))
        
        connection.commit()
        print("Bulk insert completed.")
        cursor.close()
        connection.close()

    @ensure_annotations 
    def find(self, query: dict = {}, table_name: Optional[str] = None,database_name:Optional[str] = None):
        """Retrieve records from the specified MySQL table based on the query."""
        connection = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.password,
        database=database_name  # Specify the database here
    )
        cursor = connection.cursor(dictionary=True)  # This will return results as dictionaries

        # If no query is specified, fetch all records
        if not query:
            sql = f"SELECT * FROM {table_name}"
            cursor.execute(sql)
        else:
            # Construct the WHERE clause based on the query dictionary
            conditions = ' AND '.join([f"{key} = %s" for key in query.keys()])
            sql = f"SELECT * FROM {table_name} WHERE {conditions}"
            cursor.execute(sql, tuple(query.values()))

        # Fetch all the results
        results = cursor.fetchall()

        cursor.close()
        connection.close()

        return results


    @ensure_annotations 
    def update(self, query: dict={}, new_values: dict={},table_name: Optional[str] = None,database_name:Optional[str] = None):
        """Update records in the MySQL table based on the query and new values."""
        connection = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.password,
        database=database_name  # Specify the database here
        )
        
        cursor = connection.cursor()

        try:
            # Construct the SET clause from the new_values dictionary
            set_clause = ', '.join([f"{key} = %s" for key in new_values.keys()])

            # Construct the WHERE clause from the query dictionary
            where_clause = ' AND '.join([f"{key} = %s" for key in query.keys()])

            # Prepare the SQL UPDATE statement
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

            # Combine the values for SET and WHERE clauses
            values = tuple(new_values.values()) + tuple(query.values())

            # Execute the SQL statement
            cursor.execute(sql, values)
            connection.commit()

            print(f"Record(s) updated in {table_name} where {query}.")
            
        except Error as e:  # Make sure to replace `Error` with the relevant exception class
            print(f"Error updating record: {e}")
        
        finally:
            cursor.close()
            connection.close()

    @ensure_annotations 
    def delete(self,query: dict={},table_name: Optional[str] = None,database_name:Optional[str] = None):
        """Delete records from the MySQL table based on the query."""
        connection = mysql.connector.connect(
        host=self.host,
        user=self.user,
        password=self.password,
        database=database_name  # Specify the database here
        )
        cursor = connection.cursor()

        try:
            # Construct the WHERE clause from the query dictionary
            where_clause = ' AND '.join([f"{key} = %s" for key in query.keys()])

            # Prepare the DELETE statement
            sql = f"DELETE FROM {table_name} WHERE {where_clause}"

            # Combine the values for the WHERE clause
            values = tuple(query.values())

            # Execute the SQL statement
            cursor.execute(sql, values)
            connection.commit()

            print(f"Record(s) deleted from {table_name} where {query}.")
        
        except Error as e:  # Use the appropriate MySQL error handling class
            print(f"Error deleting record: {e}")
        
        finally:
            cursor.close()
            connection.close()
