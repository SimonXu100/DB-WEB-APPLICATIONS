import src.data_service.RDBDataTable as RDBDataTable
import json

#test for get_primary_key_columns(self)
def t_get_primary_key_columns():
    table_name = 'appearances'
    db_name = 'lahman2019clean'
    result = RDBDataTable.RDBDataTable(table_name, db_name, key_columns=None)
    data = result.get_primary_key_columns()
    print("the result of get_primary_key_columns:   ", json.dumps(data, indent=2))

#t_get_primary_key_columns()


# test for get_row_count():
def t_get_row_count():
    table_name = 'appearances'
    db_name = 'lahman2019clean'
    result = RDBDataTable.RDBDataTable(table_name, db_name, key_columns=None)
    data = result.get_row_count()
    print("the result of get_primary_key_columns:   ", json.dumps(data, indent=2))

#t_get_row_count()
















