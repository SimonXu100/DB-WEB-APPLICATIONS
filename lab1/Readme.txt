W4111_F19_HW1
Implementation template for homework 1.


Structure

1 Function:

CSVDataTable.py: manipulation for csv files

RDBDataTable.py: manipulation for csv files

2 Testfiles:

test_csv.py: test for CSVDataTable.py 
test data: People.csv/Batting.csv 

test_rdb.py: test for RDBDataTable.py 
test tables: People/Batting

3 Test functions

test_csv.py:

test_init()
test_match(): test for matches_template()
test_k_to_template: test for key_to_template()
t_load(): test for load()
t_project(): test for poject()<br t_find_by_template(): test for find_by_template()
t_find_by_pk: test for find_by_primary_key()
t_delete_by_template: test for delete_by_template(template)
t_delete_by_key(): test for delete_by_key(key_vals)
t_update_by_template: test for update_by_template(template, new_values) (test under normal case and duplicate error case) 
t_update_by_key: test for update_by_key(key_vals, new_values) (test under normal case and duplicate error case) 
t_insert(): test for insert(new_record): (test under normal case and duplicate error case) 
t_save(): test for save()(save the modified csv file into original file)



test_rdb.py:

test_rdb_init()
test_rdb_find_by_template(): test for find_by_template(template, fields_list)
test_rdb_find_by_primary_key(): test for find_by_primary_key(key_valus) test_rdb_delete_by_template(): test for delete_by_template(template)
test_rdb_delete_by_key(): test for delete_by_key(key_vals)
test_rdb_update_by_template(): test for update_by_template(template,new_values)
(test under normal case and duplicate error case) 
test_rdb_update_by_key(): test for update_by_key(key_valsm,new_values)
(test under normal case and duplicate error case) 
test_rdb_insert(): test for insert(new_record)
(test under normal case and duplicate error case) 

Reminder:

1 RDB connection info: connect_info = {
'host': 'localhost',
'user': 'dbuser',
'password': 'dbuserdbuser',
'db': 'lahman2019raw',
'charset': 'utf8mb4',
'cursorclass': 'pymysql.cursors.DictCursor' } 


2 primary key
test_csv.py: 
people.csv: primary key(playerID)
Batting.csv: primary key(playerID,teamID,yearID,stint)


test_rdb.py:
should be set manually in database
people.csv: primary key(playerID)
Batting.csv: primary key(playerID,teamID,yearID,stint)


Contact Information

sx2261@columbia.edu 
if you have questions, please feel free to email me