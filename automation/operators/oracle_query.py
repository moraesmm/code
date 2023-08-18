import cx_Oracle
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logging.basicConfig(filename='execute_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def execute(db_host, db_port, db_name, db_usr, db_pwd, sql_query, sql_arg=None):
    """
    Use this function to connect to the Oracle DB and execute a query.
    
    Args:
        db_host (str): Oracle host
        db_port (int): Oracle port
        db_name (str): Oracle SID or Service Name
        db_usr (str): Oracle user
        db_pwd (str): Oracle password
        sql_query (str): SQL query to execute
        sql_arg (dict): Dictionary of parameters for the SQL query (default: None)
    """
    if sql_arg is None:
        sql_arg = {}

    try:
        # Establish database connection
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}')
        conn = conn.connect()
    except SQLAlchemyError as e:
        # Handle connection error, attempt with service_name
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/?service_name={db_name}')
        conn = conn.connect()

    try:
        # Parameterized SQL query
        sql_query = sql_query.replace(":db_schema", sql_arg["db_schema"]).replace(":db_table", sql_arg["db_table"]).replace(":tb_dt_filter", sql_arg["tb_dt_filter"]).replace(":start_date", sql_arg["start_date"]).replace(":end_date", sql_arg["end_date"])
        #formatted_query = sql_query.format(**sql_arg)
        conn.execute(text(sql_query), sql_arg)
        logging.info('SQL query executed successfully')
    except SQLAlchemyError as e:
        # Handle SQL execution error
        error = str(e)
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
        sql_query='SELECT * FROM {db_schema}.{db_table} WHERE {tb_dt_filter} BETWEEN :start_date AND :end_date',
        sql_arg={
            "db_schema": "myschema",
            "db_table": "mytable",
            "tb_dt_filter": "date_column",
            "start_date": "2023-01-01",
            "end_date": "2023-12-31"
        }
    )
"""
    logging.info('SQL execution script completed')