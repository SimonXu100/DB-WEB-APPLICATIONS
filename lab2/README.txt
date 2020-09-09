Structure

1 Implement Files:
app.py: 
implemented functions: 
@application.route("/api/databases", methods=["GET"])
def dbs() : GET a list of databases 

@application.route("/api/databases/<dbname>", methods=["GET"])
def tbls(dbname): GET A list of tables with specified a database

@application.route('/api/<dbname>/<resource>/<primary_key>', methods=['GET', 'PUT', 'DELETE'])
def resource_by_id(dbname, resource, primary_key): 
GET : retrived information by primairy key(mapping to select by primary key)
PUT method: update the resources(tables) with new values(mapping to update by primary key)
DELETE method:  delete the specified columns in resources(tables)(mapping to delete by primary key)

@application.route('/api/<dbname>/<resource_name>', methods=['GET', 'POST'])
def get_resource(dbname, resource_name):
GET method: retrived information by template using query_parameters
POST methods: insert a record passed by body into a resource(table) by template using query_parameters


RDBDataTable.py: 
inplemented functions:
def get_primary_key_columns(self): find a list of the primary key columns ordered by their position in the key
def get_row_count(self): compute the count of the number of rows in the table
def get_sample_rows(self, no_of_rows=_rows_to_print): print ou a Pandas dataframe containing the first _row_to_print number of rows


data_table_adapter.py:
inplemented functions:
def get_databases(): find a list of databases/schema at this endpoint.
def get_tables(dbname): find a list of databases/schema/tables at this endpoint.


2 Testfiles:

test_RDBDataTable.py: test for RDBDataTable.py


test_data_table_adapter.py: test for data_table_adapter.py 


Testing_Document.pdf: contains more details and screeshots of testing result of app.py using postman

test_document_RDBDataTable.pdf: contains more details and testing outputs of test_RDBDataTable.py

test_document_data_table_adapter.pdf: contains more details and testing outputs of test_data_table_adapter.py



Reminder:

1  connection info: connect_info = {
'host': 'localhost',
'user': 'root',
'password': 'dbuserdbuser',
'db': 'lahman2019clean',
'charset': 'utf8mb4',
'cursorclass': 'pymysql.cursors.DictCursor' } 



Contact Information

sx2261@columbia.edu 
if you have questions, please feel free to email me