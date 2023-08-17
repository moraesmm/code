def execute(csv_folder,db_host,db_port,db_name,db_usr,db_pwd,db_schema,db_table,tb_columns):

    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import SQLAlchemyError
    import os
    import cx_Oracle
    import pandas as pd
    import csv
    from datetime import datetime


    """
        Use this function to import a csv file into oracle db.

        Args:
            csv_folder: Define folder to read csv files
            db_host: Oracle host
            db_port: Oracle port
            db_name: Oracle SID or Service Name
            db_usr: Oracle user
            db_pwd: Oracle password
            db_schema: Oracle schema
            db_table: Oracle table (destination)
            tb_columns: Define columns to insert data
    """
    tb_columns = str(tb_columns).replace("'","")

    # get a list of csv files
    csv_files = [file for file in os.listdir(csv_folder) if file.endswith(".csv")]

    # create oracle conn 
    # study the best way to handle with oracle conn and implement it
    try:
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}')
        conn = conn.connect()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/?service_name={db_name}')
        conn = conn.connect()

    # list csv files in csv folder and insert them into oracle
    for csv_file_name in csv_files:
        csv_path = os.path.join(csv_folder,csv_file_name)

        with open(csv_path, "r") as csv_file:
            csv_reader=csv.reader(csv_file)
            next(csv_reader) # skip header row

            for row in csv_reader:
                now=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                now=f'to_timestamp(\'{str(now)}\', \'YYYY-MM-DD HH24:MI:SS.XFF\')'
                sql_insert = f'INSERT INTO {db_schema}.{db_table} ({tb_columns}) VALUES ({str(row[1:]).replace("  ","")},{now})'
                sql_insert = str(sql_insert).replace("[","").replace("]","")
                try:
                    conn.execute(text(sql_insert))
                    # create and implement function to delete csv file
                except SQLAlchemyError as e:
                    error = str(e.__dict__['orig'])
                    # create function to insert the log msg into oracle db
                    print(f'######## ERROR!!! ########\n{error}\nConnecton-> {conn}') 

    conn.close()