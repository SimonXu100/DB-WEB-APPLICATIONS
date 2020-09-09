# test files for RDBDataTable.py
import time
from src.RDBDataTable import RDBDataTable
import pymysql
import logging
import json

# The logging level to use should be an environment variable, not hard coded.
logging.basicConfig(level=logging.DEBUG)

# Also, the 'name' of the logger to use should be an environment variable.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def test_rdb_init():
    connect_info = {
        'host': 'localhost',
        'user': 'dbuser',
        'password': 'dbuserdbuser',
        'db': 'lahman2019raw',
        'charset': 'utf8mb4',
        'cursorclass': 'pymysql.cursors.DictCursor'
    }
    rdb_tbl = RDBDataTable("lahman2019raw.people", connect_info, None)

    print("Connection to DB", rdb_tbl)
#test_rdb_init()

def test_rdb_find_by_template():
    connect_info = {
        'host': 'localhost',
        'user': 'dbuser',
        'password': 'dbuserdbuser',
        'db': 'lahman2019raw',
        'charset': 'utf8mb4',
        'cursorclass': 'pymysql.cursors.DictCursor'
    }
    rdb_tbl = RDBDataTable("lahman2019raw.people", connect_info, None)

    fields_list = ['nameLast', 'nameFirst', 'birthYear', 'birthState', 'birthMonth']
    template = {"nameLast": "Williams", "birthCity": "San Diego"}

    result = rdb_tbl.find_by_template(template, fields_list)
    print("Query result = \n", json.dumps(result, indent=2))
test_rdb_find_by_template()

def test_rdb_find_by_primary_key():
    connect_info = {
        'host': 'localhost',
        'user': 'dbuser',
        'password': 'dbuserdbuser',
        'db': 'lahman2019raw',
        'charset': 'utf8mb4',
        'cursorclass': 'pymysql.cursors.DictCursor'
    }
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    fields_list = ['playerID', 'teamID', 'yearID', 'AB', 'H', 'HR', 'RBI']
    key_vals = ['willite01', 'BOS', '1960', '1']
    rdb_tbl = RDBDataTable("lahman2019raw.batting", connect_info, key_cols)
    result = rdb_tbl.find_by_primary_key(key_vals, fields_list)
    print("Query result = \n", json.dumps(result, indent=2))
#test_rdb_find_by_primary_key()

def test_rdb_delete_by_template():
    connect_info = {
        'host': 'localhost',
        'user': 'dbuser',
        'password': 'dbuserdbuser',
        'db': 'lahman2019raw',
        'charset': 'utf8mb4',
        'cursorclass': 'pymysql.cursors.DictCursor'
    }

    template = {"nameLast": "Williams", "birthCity": "San Diego"}
    rdb_tbl = RDBDataTable("lahman2019raw.people", connect_info, None)
    result = rdb_tbl.delete_by_template(template)

#test_rdb_delete_by_template()

def test_rdb_delete_by_key():
    connect_info = {
        'host': 'localhost',
        'user': 'dbuser',
        'password': 'dbuserdbuser',
        'db': 'lahman2019raw',
        'charset': 'utf8mb4',
        'cursorclass': 'pymysql.cursors.DictCursor'
    }
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    #key_vals = ['willite01', 'BOS', '1960', '1']
    key_vals = ['abercda01', 'TRO', '1871', '']

    rdb_tbl = RDBDataTable("lahman2019raw.batting", connect_info, key_cols)
    result = rdb_tbl.delete_by_key(key_vals)

#test_rdb_delete_by_key()

def test_rdb_update_by_template():
    connect_info = {
        'host': 'localhost',
        'user': 'dbuser',
        'password': 'dbuserdbuser',
        'db': 'lahman2019raw',
        'charset': 'utf8mb4',
        'cursorclass': 'pymysql.cursors.DictCursor'
    }
    rdb_tbl = RDBDataTable("lahman2019raw.people", connect_info, None)
    #manully set the primary key of people table: playerID
    # normal condition
    new_values = {'nameFirst': 'Shusen', 'birthYear': '1996', 'birthState': 'CN', 'birthMonth': '4'}
    template = {"nameLast": "Aardsma", "birthCity": "Denver"}

    result = rdb_tbl.update_by_template(template, new_values)
    #result:1 rows have been updated

    # duplicate error check
    # update the playerID into 'aardsda01' which is  another row's primary key
    new_values = {'playerID': 'aardsda01', 'nameFirst': 'Shusen', 'birthYear': '1996', 'birthState': 'CN', 'birthMonth': '4'}
    template = {"nameLast": "Aaron", "birthCity": "Mobile"}
    result = rdb_tbl.update_by_template(template, new_values)
    #result2: 'pymysql.err.IntegrityError: (1062, "Duplicate entry 'aardsda01' for key 'PRIMARY'")'
#test_rdb_update_by_template()

def test_rdb_update_by_key():
    connect_info = {
        'host': 'localhost',
        'user': 'dbuser',
        'password': 'dbuserdbuser',
        'db': 'lahman2019raw',
        'charset': 'utf8mb4',
        'cursorclass': 'pymysql.cursors.DictCursor'
    }
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    # manually set the batting table primary key: 'playerID', 'teamID','yearID','stint'
    # normal case
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    key_vals = ['barkeal01', 'RC1', '1871', '1']
    new_values = {'AB': '0', 'H': '0', 'HR': '0'}
    rdb_tbl = RDBDataTable("lahman2019raw.batting", connect_info, key_cols)
    result = rdb_tbl.update_by_key(key_vals, new_values)

    # duplicate error case
    # the follow case create duplicate primary key values:  {'playerID': 'barkeal01', 'teamID': 'RC1',  'yearID': '1871', 'stint': '1'}
    key_vals2 = ['addybo01', 'RC1', '1871', '1']
    new_values2 = {'playerID': 'barkeal01', 'teamID': 'RC1',  'yearID': '1871', 'stint': '1'}
    rdb_tbl = RDBDataTable("lahman2019raw.batting", connect_info, key_cols)
    result = rdb_tbl.update_by_key(key_vals2, new_values2)

# test_rdb_update_by_key()
#result:pymysql.err.IntegrityError: (1062, "Duplicate entry 'willite01-1960-BOS-1' for key 'PRIMARY'")

def test_rdb_insert():
    connect_info = {
        'host': 'localhost',
        'user': 'dbuser',
        'password': 'dbuserdbuser',
        'db': 'lahman2019raw',
        'charset': 'utf8mb4',
        'cursorclass': 'pymysql.cursors.DictCursor'
    }
    rdb_tbl = RDBDataTable("lahman2019raw.people", connect_info, None)
    # set 'playerID' as the primary key
    # normal condition
    new_record = {'playerID': 'beanxu01', 'birthYear': '1996', 'birthMonth': '4', 'birthDay': '29',
                  'birthCountry': 'CN', 'birthState': 'CN'}

    result = rdb_tbl.insert(new_record)


    # duplicate error check
    new_record2 = {'playerID': 'beanxu01', 'birthYear': '2006'}
    result2 = rdb_tbl.insert(new_record2)
    # the result
    #pymysql.err.IntegrityError: (1062, "Duplicate entry 'beanxu01' for key 'PRIMARY'")
#test_rdb_insert()
