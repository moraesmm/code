from operators.oracle_query_to_csv import execute as OracleQueryToCSVExecute
from operators.oracle_query import execute as OracleQueryExecute
from operators.oracle_import_csv import execute as OracleImportCSVExecute
import os
from urllib.parse import quote_plus

# define OracleQueryToCSVExecute args
origin_db_host = os.getenv("")
origin_db_port = str(os.getenv(""))
origin_db_name = os.getenv("")
origin_db_usr = os.getenv("")
origin_db_pwd = quote_plus(os.getenv(""))
origin_sql_query = open('').read()
origin_output_folder = ''
origin_output_file_name = __file__ # full path of the current file
origin_output_file_name = os.path.basename(origin_output_file_name) # File name
origin_output_file_name = os.path.splitext(origin_output_file_name)[0] # Remove extrension

# define OracleImportCSVExecute args
destination_csv_folder = f'.\\automation\\{origin_output_folder}\\output'
destination_db_host = os.getenv("")
destination_db_port = str(os.getenv(""))
destination_db_name = os.getenv("")
destination_db_usr = os.getenv("")
destination_db_pwd = quote_plus(os.getenv(""))
destination_db_schema = ''
destination_db_table = ''
destination_tb_columns = []

# define OracleImportCSVExecute args
delete_sql_query = open('.\\automation\\sql\\delete_by_period.sql').read()
delete_sql_params = {
    "db_schema": '',
    "db_table": '',
    "tb_dt_filter": '',
    "start_date": '',
    "end_date": ''
}

#OracleQueryToCSVExecute(origin_db_host,origin_db_port,origin_db_name,origin_db_usr,origin_db_pwd,origin_sql_query,origin_output_folder,origin_output_file_name)
# test how to filter the period to delete old data
#OracleQueryExecute(destination_db_host,destination_db_port,destination_db_name,destination_db_usr,destination_db_pwd,delete_sql_query,delete_sql_params)
OracleImportCSVExecute(destination_csv_folder,destination_db_host,destination_db_port,destination_db_name,destination_db_usr,destination_db_pwd,destination_db_schema,destination_db_table,destination_tb_columns)