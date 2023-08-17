def execute(csv_folder, db_host, db_port, db_name, db_usr, db_pwd, db_schema, db_table, tb_columns):
    """
    Import CSV files into an Oracle database.

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
        
    Notes:
        - This function assumes that the first row of each CSV file is a header and will be skipped during import.
        - The Oracle connection is managed using SQLAlchemy and the cx_Oracle driver.

    Example:
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
    """
    
    # Import necessary libraries
    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import SQLAlchemyError
    import os
    import cx_Oracle
    import pandas as pd
    import csv
    from datetime import datetime
    
    # Prepare table columns for SQL insertion
    tb_columns = str(tb_columns).replace("'", "")
    
    # Get a list of CSV files in the specified folder
    csv_files = [file for file in os.listdir(csv_folder) if file.endswith(".csv")]
    
    try:
        # Connect to Oracle using SID (if possible)
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}')
        conn = conn.connect()
    except SQLAlchemyError as e:
        # If SID connection fails, use Service Name
        error = str(e.__dict__['orig'])
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/?service_name={db_name}')
        conn = conn.connect()

    # Loop through each CSV file and import its data
    for csv_file_name in csv_files:
        csv_path = os.path.join(csv_folder, csv_file_name)

        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Skip header row

            for row in csv_reader:
                # Generate current timestamp for insertion
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                now = f'to_timestamp(\'{str(now)}\', \'YYYY-MM-DD HH24:MI:SS.XFF\')'
                
                # Prepare SQL insert statement
                sql_insert = f'INSERT INTO {db_schema}.{db_table} ({tb_columns}) VALUES ({str(row[1:]).replace("  ","")},{now})'
                sql_insert = str(sql_insert).replace("[", "").replace("]", "")
                
                try:
                    # Execute SQL insert statement
                    conn.execute(text(sql_insert))
                    # Additional logic to delete the CSV file can be added here
                except SQLAlchemyError as e:
                    error = str(e.__dict__['orig'])
                    # Additional logic to insert the error log into Oracle database can be added here
                    print(f'######## ERROR!!! ########\n{error}\nConnecton-> {conn}') 

    # Close the Oracle connection
    conn.close()
