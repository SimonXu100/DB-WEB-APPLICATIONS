import src.data_service.data_table_adaptor as dta
import json
# test for get_rdb_table()

def t_get_rdb_table():
    r = dta.get_rdb_table("people", "lahman2019clean")
    print(r)

#t_get_rdb_table()

# test for get_databases()
def t_get_databases():
    data = dta.get_databases()
    print("the result of get_databases:   ", json.dumps(data, indent=2))


#t_get_databases()

# test for get_tables
def t_get_tables(dbname):
    data = dta.get_tables(dbname)
    print("the result of get_tables:   ", json.dumps(data, indent=2))

#t_get_tables("lahman2019clean")
