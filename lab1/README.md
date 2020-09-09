# W4111_F19_HW1
Implementation template for homework 1.

By Shusen Xu


####Structure
#####1 Function:
CSVDataTable.py: manipulation for csv files 

RDBDataTable.py: manipulation for csv files

#####2 Testfiles:
test_csv.py: test for CSVDataTable.py
<br>test data: People.csv/Batting.csv
<br>
<br>test_rdb.py: test for RDBDataTable.py
<br>test tables: People/Batting

#####3 Test functions
test_csv.py:<br><br>
test_init()<br>
test_match(): test for matches_template()<br>
test_k_to_template: test for key_to_template()<br>
t_load(): test for load()<br>
t_project(): test for poject()<br
t_find_by_template(): test for find_by_template()<br>
t_find_by_pk: test for find_by_primary_key()<br>
t_delete_by_template: test for delete_by_template(template)<br>
t_delete_by_key(): test for delete_by_key(key_vals)<br>
t_update_by_template: test for update_by_template(template, new_values)
(test under normal case and duplicate error case)
<br>
t_update_by_key: test for update_by_key(key_vals, new_values)
(test under normal case and duplicate error case)
<br>
t_insert(): test for insert(new_record):
(test under normal case and duplicate error case)
<br>
t_save(): test for save()(save the modified csv file into original file)

<br><br>
test_rdb.py:<br><br>
test_rdb_init()<br>
test_rdb_find_by_template(): test for find_by_template(template, fields_list)<br>
test_rdb_find_by_primary_key(): test for find_by_primary_key(key_valus)
test_rdb_delete_by_template(): test for delete_by_template(template)<br>
test_rdb_delete_by_key(): test for delete_by_key(key_vals)<br>
test_rdb_update_by_template(): test for update_by_template(template,new_values)<br>
(test under normal case and duplicate error case)
<br>
test_rdb_update_by_key(): test for update_by_key(key_valsm,new_values)<br>
(test under normal case and duplicate error case)
<br>
test_rdb_insert(): test for insert(new_record)<br>
(test under normal case and duplicate error case)
<br>


####Reminder:<br>
1 RDB connection info:
connect_info = {<br>
        'host': 'localhost',<br>
        'user': 'dbuser',<br>
        'password': 'dbuserdbuser',<br>
        'db': 'lahman2019raw',<br>
        'charset': 'utf8mb4',<br>
        'cursorclass': 'pymysql.cursors.DictCursor'
    }
2 



#####Contact Information
sx2261@columbia.edu
<br>if you have questions, please feel free to emial me

