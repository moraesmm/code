DELETE :db_schema.:db_table
WHERE 1=1
    AND TO_DATE(:tb_dt_filter, 'dd/mm/yyyy')
        BETWEEN :start_date AND :end_date