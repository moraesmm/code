def execute(db_host,db_port,db_name,db_usr,db_pwd,sql_query,sql_arg={}):

    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import SQLAlchemyError
    import cx_Oracle

    """
        Use this function to connect to oracle db and execute query.
        
        Args:
            db_host: Oracle host
            db_port: Oracle port
            db_name: Oracle SID or Service Name
            db_usr: Oracle user
            db_pwd: Oracle password
            sql_query: SQL statement to execute
    """

    # study the best way to handle with oracle conn and implement it
    try:
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}')
        conn = conn.connect()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        conn = create_engine(f'oracle+cx_oracle://{db_usr}:{db_pwd}@{db_host}:{db_port}/?service_name={db_name}')
        conn = conn.connect()

    try:
        conn.execute(text(sql_query, sql_arg))
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        # create function to insert the log msg into oracle db
        print(f'######## ERROR!!! ########\nSql statement-> {sql_query}\n{error}\nConnecton-> {conn}') 
    conn.close()