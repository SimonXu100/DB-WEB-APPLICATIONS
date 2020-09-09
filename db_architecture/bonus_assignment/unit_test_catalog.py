import CSVCatalog
import json


# testing examples:
# select * from tables where table_name ='cool';
# create a table
# using class CSVCatalog: create_table()
'''
def test_build_CSVCatalog():
    c_cat = CSVCatalog.CSVCatalog()
    print("the catalog = ", c_cat)
test_build_CSVCatalog()
'''

def test_create_table():
    c_cat = CSVCatalog.CSVCatalog()
    table_name = "batting"
    file_name = "/Users/xushusen/Desktop/bonus_assignment/Batting.csv"
    # create columns
    ColumnDefinitions = []
    c_def1 = CSVCatalog.ColumnDefinition('playerID', "text", True)
    c_def2 = CSVCatalog.ColumnDefinition('yearID', "number", True)
    c_def3 = CSVCatalog.ColumnDefinition('stint', "number", True)
    c_def4 = CSVCatalog.ColumnDefinition('teamID', "text", True)
    c_def5 = CSVCatalog.ColumnDefinition('lgID', "text", True)
    ColumnDefinitions.append(c_def1)
    ColumnDefinitions.append(c_def2)
    ColumnDefinitions.append(c_def3)
    ColumnDefinitions.append(c_def4)
    ColumnDefinitions.append(c_def5)

    # create index
    index_definitions = {}
    i_def = CSVCatalog.IndexDefinition('Batting_index', 'PRIMARY', ['playerID', 'yearID', 'stint', 'teamID'])
    index_definitions['Batting_index'] = i_def
    result = c_cat.create_table(table_name, file_name, ColumnDefinitions, index_definitions)
    print("Result = ", result)

test_create_table()


# first run test_create_table, do not run two times, otherwise duplicate key issues will arise
# this function also tested for load_core_definition(), self.load_columns(),self.load_indexes() since
# get_table() function call all these three function above
#test for get_table()
def test_get_table():
    c_cat = CSVCatalog.CSVCatalog()
    result = c_cat.get_table("batting")
    print("get_table_result = ", result)

#test_get_table()


# test for drop_table()
def test_drop_table():
    c_cat = CSVCatalog.CSVCatalog()
    result = c_cat.drop_table("batting")

test_drop_table()
#test_get_table()



# test for column definition
def test_column_definition():
    c_cat = CSVCatalog.CSVCatalog()
    c_def = CSVCatalog.ColumnDefinition("AB", 'number', True)
    print("c_def = ", c_def)

#test_column_definition()


# test for index definition
def test_index_definition():
    c_cat = CSVCatalog.CSVCatalog()
    i_def = CSVCatalog.IndexDefinition('Batting_index', 'PRIMARY', ['playerID', 'teamID', 'yearID', 'stint'])
    print("c_def = ", i_def)












