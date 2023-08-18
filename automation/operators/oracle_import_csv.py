import os
import csv
import cx_Oracle
from sqlalchemy import create_engine,text,insert
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(filename='csv_import.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect_to_database(db_host, db_port, db_name, db_usr, db_pwd):
    """
    Establishes a connection to the Oracle database.

    Args:
        db_host (str): The hostname or IP address of the Oracle database.
        db_port (int): The port number of the Oracle database.
        db_name (str): The SID or Service Name of the Oracle database.
        db_usr (str): The username for connecting to the Oracle database.
        db_pwd (str): The password for the Oracle user.

    Returns:
        Connection: A SQLAlchemy database connection object.
    """
    try:
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}')
        conn = conn.connect()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/?service_name={db_name}')
        conn = conn.connect()
    return conn

def execute_sql_insert(conn, sql_insert,data):
    """
    Executes a SQL insert statement on the database.

    Args:
        conn (Connection): A SQLAlchemy database connection object.
        sql_insert (str): The SQL insert statement to execute.
    """
    try:
        conn.execute(sql_insert, data)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        logging.error(f'Error executing SQL: {error}')

def execute(csv_folder, db_host, db_port, db_name, db_usr, db_pwd, db_schema, db_table, tb_columns):
    """
    Imports CSV files into an Oracle database.

    This function reads CSV files from a specified folder and inserts their data into an Oracle database table.
    
    Args:
        csv_folder (str): The folder path containing the CSV files to be imported.
        db_host (str): The hostname or IP address of the Oracle database.
        db_port (int): The port number of the Oracle database.
        db_name (str): The SID or Service Name of the Oracle database.
        db_usr (str): The username for connecting to the Oracle database.
        db_pwd (str): The password for the Oracle user.
        db_schema (str): The schema of the Oracle database where the table resides.
        db_table (str): The name of the Oracle table where data will be inserted.
        tb_columns (str): A comma-separated list of columns in the Oracle table.
    """
    # Prepare table columns for SQL insertion
    tb_columns = str(tb_columns).replace("'", "").replace("[", "").replace("]", "") 

    # Get a list of CSV files in the specified folder
    csv_files = [file for file in os.listdir(csv_folder) if file.endswith(".csv")]

    # Connect to the database
    conn = connect_to_database(db_host, db_port, db_name, db_usr, db_pwd)

    logging.info('Starting CSV import process')

    try:
        for csv_file_name in csv_files:
            csv_path = os.path.join(csv_folder, csv_file_name) 

            with open(csv_path, "r", encoding="utf-8-sig") as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Skip header row
                data = []
                batch_nbr=0

                for row in csv_reader:
                    bind_variables = [f":{i}" for i in range(1, len(row)+1)]
                    bind_variables_string = ", ".join(bind_variables)
                    
                    # Construct SQL insert statement
                    sql_insert = f"INSERT INTO {db_schema}.{db_table} ({tb_columns}) VALUES ({bind_variables_string}, to_timestamp(to_char(sysdate, 'YYYY-MM-DD HH24:MI:SS') ,'YYYY-MM-DD HH24:MI:SS'))"
                    array_without_whitespace = [element.strip() for element in row]

                    # Execute SQL insert statement
                    data.append(array_without_whitespace)
                    if len(data) % 20000 == 0:
                        try:
                            execute_sql_insert(conn, sql_insert, data)
                            batch_nbr += 1
                            data = []
                        except Exception as e:
                            logging.error(f'Error executing SQL insert: {e}')                                    


    finally:
        # Close the database connection
        conn.close()
        logging.info('CSV import process completed')

"""
# Usage example
if __name__ == '__main__':
    logging.info('CSV import script started')
    execute(
        csv_folder='/path/to/csv_files',
        db_host='localhost',
        db_port=1521,
        db_name='ORCL',
        db_usr='myuser',
        db_pwd='mypassword',
        db_schema='myschema',
        db_table='mytable',
        tb_columns='col1, col2, col3'
    )
    logging.info('CSV import script completed')
"""