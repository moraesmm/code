def execute(db_host,db_port,db_name,db_usr,db_pwd,sql_query,output_proj,output_name):

    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import SQLAlchemyError
    import cx_Oracle
    import pandas as pd
    import time

    """
        Use this function to connect to oracle db and save query's result as csv.
        
        Args:
            db_host: Oracle host
            db_port: Oracle port
            db_name: Oracle SID or Service Name
            db_usr: Oracle user
            db_pwd: Oracle password
            sql_query: SQL statement to execute
            output_proj: Project name, define where to save 
            output_name: Output file name
    """

    output_dir = f'.\\automation\\{str(output_proj)}\\output\\{str(output_name)}_{str(time.strftime("%Y%m%d-%H%M%S"))}.csv'

    # study the best way to handle with oracle conn and implement it
    try:
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}')
        conn = conn.connect()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/?service_name={db_name}')
        conn = conn.connect()

    try:
        data = pd.DataFrame(conn.execute(text(sql_query)))
        data.to_csv(output_dir)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        # create function to insert the log msg into oracle db
        print(f'######## ERROR!!! ########\nSql statement-> {sql_query}\n{error}\nConnecton-> {conn}') 
    conn.close()