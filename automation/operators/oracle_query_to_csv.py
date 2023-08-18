import os
import csv
import cx_Oracle
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import time
import logging

# Configure logging
logging.basicConfig(filename='execute_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute(db_host, db_port, db_name, db_usr, db_pwd, sql_query, sql_query_params, output_proj, output_name):
    """
    Connects to an Oracle database, executes a SQL query, and saves the results as a CSV file.

    Args:
        db_host (str): Oracle host
        db_port (int): Oracle port
        db_name (str): Oracle SID or Service Name
        db_usr (str): Oracle user
        db_pwd (str): Oracle password
        sql_query (str): SQL statement to execute
        sql_query_params (dict): Dictionary of parameter values for the query
        output_proj (str): Project name, defining where to save
        output_name (str): Output file name
    """
    try:
        # Establish database connection
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}')
        conn = conn.connect()
    except SQLAlchemyError as e:
        # Handle connection error, attempt with service_name
        error = str(e.__dict__['orig'])
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/?service_name={db_name}')
        conn = conn.connect()

    try:
        # Execute the SQL query and save result as CSV
        data = pd.DataFrame(conn.execute(text(sql_query), sql_query_params))
        # Construct output directory and file name with timestamp
        output_dir = os.path.join('.', 'automation', str(output_proj), 'output',
                                  f'{str(output_name)}_{str(time.strftime("%Y%m%d-%H%M%S"))}.csv')
        data.to_csv(output_dir, index=False)
        logging.info(f'Successfully executed and saved results to {output_dir}')
    except SQLAlchemyError as e:
        # Handle SQL execution error
        error = str(e.__dict__['orig'])
        # Log the error
        logging.error(f'Error executing SQL query: {error}')
    finally:
        # Close the database connection
        conn.close()
        logging.info('Database connection closed')

"""
# Usage example
if __name__ == '__main__':
    logging.info('SQL execution script started')
    execute(
        db_host='localhost',
        db_port=1521,
        db_name='ORCL',
        db_usr='myuser',
        db_pwd='mypassword',
        sql_query='SELECT * FROM your_table',
        output_proj='your_project',
        output_name='output_data'
    )
    logging.info('SQL execution script completed')
"""