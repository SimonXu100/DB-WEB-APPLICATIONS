# I write and test methods one at a time.
# This file contains unit tests of individual methods.
import time

from src.CSVDataTable import CSVDataTable
import logging
import os

import json
# The logging level to use should be an environment variable, not hard coded.
logging.basicConfig(level=logging.DEBUG)

# Also, the 'name' of the logger to use should be an environment variable.
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# This should also be an environment variable.
# Also not the using '/' is OS dependent, and windows might need `\\`
data_dir = os.path.abspath("../Data/Baseball")

def test_init():
    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }
    csv_tbl = CSVDataTable("people", connect_info, None)
    #print the loaded data
    print("Loaded table = \n", csv_tbl)

test_init()

def test_match():
    row = {"cool": 'yes', 'db': 'no'}
    t = {"cool": 'yes'}
    result = CSVDataTable.matches_template(row, t)
    print(result)
#test_match()

def test_k_to_template():
    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }
    csv_tbl = CSVDataTable("people", connect_info, key_columns=['playerID'])
    tmp = csv_tbl.key_to_template(['aardsda01'])
    print(tmp)

test_k_to_template()
#the result: {'playerID': 'aardsda01'}

def t_load():
    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }

    csv_tbl = CSVDataTable("people", connect_info, None)

    print("Created table = " + str(csv_tbl))
#t_load()


def t_project():
    rows = {
        "playerID": "worthal01",
        "teamID": "BOS",
        "yearID": "1960",
        "AB": "1",
        "H": "0",
        "HR": "0",
        "RBI": "0"
    }
    fields = ['playerID', 'yearID', 'HR']
    result = CSVDataTable.project(rows, fields)
    print("Project = ", result)

# t_project()
# the result: Project =  {'playerID': 'worthal01', 'yearID': '1960', 'HR': '0'}
# test for find_by_template

def t_find_by_template():
    connect_info = {
        "directory": data_dir,
        "file_name": "Batting.csv"
    }

    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    fields = ['playerID', 'teamID', 'yearID', 'AB', 'H', 'HR', 'RBI']
    tmp = {'teamID': 'BOS', 'yearID': '1960'}
    csv_tbl = CSVDataTable("batting", connect_info, key_columns=key_cols)

    res = csv_tbl.find_by_template(template=tmp, field_list=fields )
    print("Query result = \n", json.dumps(res, indent=2))

#t_find_by_template()

# test for find_by_primary_key
# test：find by pk
def t_find_by_pk():

    connect_info = {
        "directory": data_dir,
        "file_name": "Batting.csv"
    }
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    fields = ['playerID', 'teamID', 'yearID', 'AB', 'H', 'HR', 'RBI']
    key_vals = ['abercda01', 'TRO', '1871', '1']
    csv_tbl = CSVDataTable("batting", connect_info, key_columns=key_cols)

    res = csv_tbl.find_by_primary_key(key_vals, fields)

    print("Query result = \n", json.dumps(res, indent=2))

#t_find_by_pk()


def t_delete_by_template():
    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }

    key_cols = ['playerID']
    template = {"nameLast": "Williams", "birthCity": "San Diego"}
    csv_tbl = CSVDataTable("People", connect_info, key_columns=key_cols)
    res = csv_tbl.delete_by_template(template)

#t_delete_by_template()

def t_delete_by_key():
    connect_info = {
        "directory": data_dir,
        "file_name": "Batting.csv"
    }
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    key_vals = ['abercda01', 'TRO', '1871', '1']
    csv_tbl = CSVDataTable("batting", connect_info, key_columns=key_cols)
    res = csv_tbl.delete_by_key(key_vals)

#t_delete_by_key()

def t_update_by_template():
    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }
    key_cols = ['playerID']
    csv_tbl = CSVDataTable("People", connect_info, key_columns=key_cols)

    # normal condition
    new_values = {'nameFirst': 'Shusen', 'birthYear': '1996', 'birthState': 'CN', 'birthMonth': '4'}
    template = {"nameLast": "Aardsma", "birthCity": "Denver"}

    result = csv_tbl.update_by_template(template, new_values)
    # result:1 rows have been updated

    # duplicate error check
    # update the playerID into 'aardsda01' which is  another row's primary key
    new_values = {'playerID': 'aardsda01', 'nameFirst': 'Shusen', 'birthYear': '1996', 'birthState': 'CN',
                  'birthMonth': '4'}
    template = {"nameLast": "Aaron", "birthCity": "Mobile"}
    result = csv_tbl.update_by_template(template, new_values)
    # result2: 'Error: duplicate key update error!!!
    # 0 row has been updated'

#t_update_by_template()

def t_update_by_key():
    connect_info = {
        "directory": data_dir,
        "file_name": "Batting.csv"
    }
    key_cols = ['playerID', 'teamID', 'yearID', 'stint']
    csv_tbl = CSVDataTable("Batting", connect_info, key_columns=key_cols)

    # manually set the batting table primary key: 'playerID', 'teamID','yearID','stint'
    # normal case
    key_vals = ['barkeal01', 'RC1', '1871', '1']
    new_values = {'AB': '0', 'H': '0', 'HR': '0'}
    result = csv_tbl.update_by_key(key_vals, new_values)

    # duplicate error case
    # the follow case create duplicate primary key values:  {'playerID': 'barkeal01', 'teamID': 'RC1',  'yearID': '1871', 'stint': '1'}
    key_vals2 = ['addybo01', 'RC1', '1871', '1']
    new_values2 = {'playerID': 'barkeal01', 'teamID': 'RC1', 'yearID': '1871', 'stint': '1'}
    result = csv_tbl.update_by_key(key_vals2, new_values2)
    #result:
    # Error: duplicate key update error!!!
    #0 row has been updated

#t_update_by_key()

def t_insert():
    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }
    key_cols = ['playerID']
    csv_tbl = CSVDataTable("People", connect_info, key_columns=key_cols)
    # set 'playerID' as the primary key
    # normal condition
    new_record = {'playerID': 'beanxu01', 'birthYear': '1996', 'birthMonth': '4', 'birthDay': '29',
                  'birthCountry': 'CN', 'birthState': 'CN'}
    result = csv_tbl.insert(new_record)

    # duplicate error check
    new_record2 = {'playerID': 'beanxu01', 'birthYear': '2006'}
    result2 = csv_tbl.insert(new_record2)
    # the result:
    # Error: duplicate key update error!!!
    # 0 row has been updated
#t_insert()

def t_save():
    connect_info = {
        "directory": data_dir,
        "file_name": "People.csv"
    }
    key_cols = ['playerID']
    csv_tbl = CSVDataTable("People", connect_info, key_columns=key_cols)
    csv_tbl.save()
    #the result
    #DEBUG:root:CSVDataTable._load: Loaded 19617 rows
    #DEBUG:root:CSVDataTable._save: Saved 19617 rows

#t_save()

# test the performance
def test_performance_batting():
    count = 100

    connect_info = {
        "directory": data_dir,
        "file_name": "Batting.csv"
    }
    key_cols = ['playID', 'teamID', 'yearID', 'stint']

    key_vals = ['williteo1', 'BOS', '1960', '1']
    print(key_vals)

    desired_fields = {'playerID', 'AB', 'H', 'HR', 'RBI'}
    csv_tbl = CSVDataTable("batting", connect_info, key_columns=key_cols)

    print("Number of iterations for each performance test= ", count, '\n')
    print("Starting test of find_by_primary_key normal")
    start_time = time.time()

    for i in range(0, count):
        r = csv_tbl.find_by_primary_key(key_fields=key_vals, field_list=desired_fields)
        if i == 0:
            print("Find result=  ", r)
    end_time = time.time()
    elapsed = end_time - start_time
    print("Done. Time = ", str(elapsed))

#test_performance_batting()








