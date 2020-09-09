import pymysql  # connect to your root server
import json  # json object
import copy
# purpose:
# Creating a new schema in the local database that holds tables containing the DB definitions
# Homework instructions
'''You are storing ONLY the definition information for tables, columns and indexes.  
You can create the tables holding this metadata in MySQL Workbench or in a csv file or
some other tool before running your code.'''

'''
 The table(s) will be blank after being created, but should have primary keys, 
 foreign keys, data types, etc. all defined between the table(s). You might have no foreign keys, 
 you may only have 1 table, you may have 50 tables (probably not that many), etc., but that is a 
 crucial part of the assignment to figure out and structure. 

With the blank tables, the Python code will store the metadata that are inputted by the code.
So if someone adds a table called "A" with an index and 27 columns with text and 3 with numbers,
you must store somewhere there is a table called A, with 30 columns with their respective data types 
and in index on two of the columns. If there is a primary key or not null, that needs to be stored. Etc. 

The CSV file is only to get data for describing the table. You are not storing it anywhere. 

The definition of 'COLUMN' has been completed for you. There are other methods in Index and Table 
that require completion denoted by #YOUR CODE HERE '''

'''
1. run q definition
2. Class Column Definition
3. Class Index Definition
4. Class Table Definition
5. CSV Catalog Definition
'''


def run_q(cnx, q, args, fetch=False):
    '''If you decide to store the metadata in sql this will be useful'''
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result


class ColumnDefinition:
    # example of what column types are acceptable
    column_types = ("text", "number")

    def __init__(self, column_name, column_type="text", not_null=False):
        """
        :param column_name: Cannot be None.
        :param column_type: Must be one of valid column_types.
        :param not_null: True or False
        """

        if column_name is None:
            raise ValueError('Column name necessary')

        else:
            self.column_name = column_name

        if column_type in self.column_types:
            self.column_type = column_type

        else:
            raise ValueError('That column type is not accepted. Please try again.')

        if not_null == False:
            self.not_null = not_null
        elif not_null == True:
            self.not_null = not_null
        else:
            raise ValueError('should be T/F')

    def __str__(self):
        # returns the table object in json format
        return json.dumps(self.to_json(), indent=2)

    def to_json(self):
        """
        :return: A JSON object, not a string, representing the column and it's properties.
        """
        result = {
            "column_name": self.column_name,
            "column_type": self.column_type,
            "not_null": self.not_null
        }
        return result


class IndexDefinition:
    """
    Represents the definition of an index.
    """
    index_types = ("PRIMARY", "UNIQUE", "INDEX")

    # modified by OH
    def __init__(self, index_name, index_type, columns):
        """
        :param index_name: Name for index. Must be unique name for table.
        :param index_type: Valid index type.
        :param column_names: list of column names assc with that index
        """
        # YOUR CODE GOES HERE#
        self.index_name = index_name
        #self.table_name = table_name
        # Should check index here but DB will do it.
        self.index_type = index_type
        self.column_names = copy.copy(columns)

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self):
        # YOUR CODE GOES HERE#
        # created by OH

        result = {
            "index_name": self.index_name,
            "index_type": self.index_type,
            "column_names": self.column_names,
        }
        return result


class TableDefinition:
    """
    Represents the definition of a table in the CSVCatalog.
    """

    def __init__(self, t_name=None, csv_f=None, column_definitions=None, index_definitions=None, cnx=None,
                 load=False):

        """
        :param t_name: Name of the table.
        :param csv_f: Full path to a CSV file holding the data.
        :param column_definitions: List of column definitions to use from file. Cannot contain invalid column name.
            May be just a subset of the columns.
        :param index_definitions: List of index definitions. Column names must be valid.
        :param cnx: Database connection to use. If None, create a default connection.
        """
        self.cnx = cnx
        self.table_name = t_name
        self.columns = None
        self.indexes = None

        # created by OH
        self.file_name = None
        if not load:

            if t_name is None or csv_f is None:
                raise ValueError("Table and file must both have a name")

            self.file_name = csv_f
            # insert operation
            self.save_core_definition()
            self.columns = []
            if column_definitions is not None:
                for c in column_definitions:
                    self.add_column_definition(c)
            # modified by shusen xu
            if index_definitions is not None:
                for idx in index_definitions.keys():
                    self.define_index(idx, index_definitions[idx].column_names, index_definitions[idx].index_type)

        else:
            self.load_core_definition()
            self.load_columns()
            self.load_indexes()

    def is_file(self, fn):
        try:
            with open(fn, "r") as a_file:
                return True
        except:
            return False

    def load_columns(self):
        '''
        #YOUR CODE HERE
        '''
        # created by shusen xu:
        # load the columns info specified by table_name
        q = "select * from CSVCatalog.columns where table_name=%s"
        res = run_q(self.cnx, q, args=self.table_name, fetch=True)

        # for correct description of columns, here load the objects of columns
        self.columns = []
        for column_info in res:
            c_def = ColumnDefinition(column_info['column_name'], column_info['type'], column_info['nullable'])
            self.columns.append(c_def)
        return None

    def load_indexes(self):
        '''
        #YOUR CODE HERE
        '''
        # may have multiple indexes, every index may consist of multiple columns
        # and every index only have on kind
        q = "select distinct(index_name) as index_name, kind from CSVCatalog.index_info where table_name=%s"
        res = run_q(self.cnx, q, args=self.table_name, fetch=True)

        for index in res:
            q1 = "select * from CSVCatalog.index_info where table_name=%s and index_name=%s"
            res1 = run_q(self.cnx, q1, args=(self.table_name, index['index_name']), fetch=True)
            column_names = []
            for c in res1:
                column_names.append(c['column_name'])
            self.indexes = {}
            new_idx = IndexDefinition(index["index_name"], index['kind'], column_names)
            self.indexes[index["index_name"]] = new_idx
        return None
    def save_core_definition(self):
        '''
        #YOUR CODE HERE
        '''
        # by OH
        # This saves the core information about the table in the table but the info
        # about the table of tables is not in this catalog it is information schema.
        # The table here that I am using is just the table about tables not the table
        # about tables about tables

        q = "insert into CSVCatalog.tables values(%s, %s)"
        res = run_q(self.cnx, q, args=(self.table_name, self.file_name), fetch=False)
        return res

    def load_core_definition(self):
        '''
        #YOUR CODE HERE
        '''
        # by OH
        q = "select * from CSVCatalog.tables where table_name=%s"
        res = run_q(self.cnx, q, args=self.table_name, fetch=True)
        if len(res)==0:
            raise ValueError('the table does not exists')
        t_info = res[0]
        self.table_name = t_info['table_name']
        self.file_name = t_info['file_location']
        return None

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    # remove by OH
    #@classmethod  # classmethod means method that can be called by objects of this class

    def add_column_definition(self, c):
        """
        Add a column definition.
        :param c: New column. Cannot be duplicate or column not in the file.
        :return: None
        """
        '''
        #YOUR CODE HERE
        '''
        # c: a instance of column definition
        # the DB will do the duplicate check
        self.columns.append(c)
        q = "insert into CSVCatalog.columns values(%s, %s, %s, %s)"
        res = run_q(self.cnx, q, args=(self.table_name, c.column_name, c.column_type, c.not_null), fetch=False)
        return None

    def get_column(self, cn):
        """
        Returns a column of the current table so that it can be deleted from the columns list
        :param cn: name of the column you are trying to get.
        :return:
        """
        '''
        #YOUR CODE HERE
        '''
        for c in self.columns:
            if c.column_name == cn:
                return c
        print("there does not exist the column you required")
        return None
    def drop_column_definition(self, c):
        """
        Remove from definition and catalog tables.
        :param c: Column name (string)
        :return:
        """
        #YOUR CODE HERE
        # remove from the catalog tables
        q = "delete from CSVCatalog.columns where table_name=%s and column_name=%s"
        res = run_q(self.cnx, q, args=(self.table_name, c), fetch=False)

        return None
    def to_json(self):
        """
        :return: A JSON representation of the table and it's elements.
        """
        result = {
            "table_name": self.table_name,
            "file_name": self.file_name
        }

        if self.columns is not None:
            result['columns'] = []
            for c in range(0, len(self.columns)):
                result['columns'].append(self.columns[c].to_json())

        if self.indexes is not None:
            result['indexes'] = []
            for idx in self.indexes.keys():
                result['indexes'].append(self.indexes[idx].to_json())
        return result

    def define_primary_key(self, columns):
        """
        Define (or replace) primary key definition.
        :param columns: List of column values in order.
        :return:
        """
        pass

    # modified by OH
    def save_index_definition(self, i_name, column_names, index_kind):
        # changed kind to type
        '''
        #YOUR CODE HERE
        '''
        q = "insert into CSVCatalog.index_info values(%s, %s ,%s, %s, %s)"

        for i in range(0, len(column_names)):
            res = run_q(self.cnx, q, args=(self.table_name, column_names[i], index_kind, i, i_name), fetch=False)
    # modified version by OH
    def define_index(self, index_name, column_names, kind="index"):
        """
        Define or replace and index definition.
        :param index_name: Index name, must be unique within a table.
        :param columns: Valid list of columns.
        :param kind: One of the valid index types.
        :return:
        """
        self.save_index_definition(index_name, column_names, kind)
        if self.indexes is None:
            #self.indexes = []
            self.indexes = {}
        new_idx = IndexDefinition(index_name, kind, column_names)
        self.indexes[index_name] = new_idx


    def get_index_cols(self, index_name):
        q = "select column_name, string_i from CSVCatalog.csvindexes where index_name = '" + index_name + "';"
        result = run_q(self.cnx, q, None, fetch=True)
        # ordering statements! debugged with prints!
        # print("RESULT:", result)
        c_list = []
        # print("RESULT", result)
        for r in (0, len(result) - 1):
            # c_list.append(result[r]['column_name'])
            for x in (0, len(result) - 1):
                # print("HERE", result[x]['string_i'])
                if int(result[r]['string_i']) == int(x):
                    # print("NAME")
                    # print(result[x]['column_name'])
                    c_list.append(result[x]['column_name'])
        return c_list

    def get_index(self, ind_name):
        """
        Returns a column of the current table so that it can be deleted from the columns list
        :param cn: name of the column you are trying to get.
        :return:
        """
        for index in self.indexes:
            if index.index_name == ind_name:
                return index
        print("Index '" + ind_name + "' not found")
        return

    def drop_index(self, index_name):
        """
        Remove an index.
        :param index_name: Name of index to remove.
        :return:
        """
        '''
        #YOUR CODE HERE
        '''
        # remove from the catalog tables(index_info) in sql
        q = "delete from CSVCatalog.index_info where table_name=%s and index_name=%s"
        res = run_q(self.cnx, q, args=(self.table_name, index_name), fetch=False)

    def describe_table(self):
        """
        Simply wraps to_json()
        :return: JSON representation.
        """
        result = self.to_json()
        return result


class CSVCatalog:

    def __init__(self, dbhost="localhost", dbport=3306,
                 dbuser="dbuser", dbpw="dbuserdbuser", db="CSVCatalog", debug_mode=None):
        self.cnx = pymysql.connect(
            host=dbhost,
            port=dbport,
            user=dbuser,
            password=dbpw,
            db=db,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __str__(self):
        # modified by shusen xu
        return "CSVCatalog ....  cnx= " + str(self.cnx)
    ''''
    def create_table(self, table_name, file_name, column_definitions=None, primary_key_columns=None):
        result = TableDefinition(table_name, file_name, cnx=self.cnx)
        return result
    '''

    # modified by OH
    def create_table(self, table_name, file_name, column_definitions=None, index_definitions=None):
        result = TableDefinition(table_name, file_name, column_definitions,
                                 index_definitions=index_definitions, load=False, cnx=self.cnx)
        return result


    def drop_table(self, table_name):
        '''
        #YOUR CODE HERE
        '''
        res = self.get_table(table_name)
        # drop the index of the table in index_info
        for index_name in res.indexes.keys():
            res.drop_index(index_name)

        # drop the content of the table in columns
        for column in res.columns:
            res.drop_column_definition(column.column_name)

        # drop table in tables in sql
        q = "delete from CSVCatalog.tables where table_name=%s"
        res = run_q(self.cnx, q, args=res.table_name, fetch=False)
        print("drop table :", table_name, " successfully")


    def get_table(self, table_name):
        '''
        #YOUR CODE HERE
        '''
        # by OH
        result = TableDefinition(t_name=table_name, load=True, cnx=self.cnx)
        return result

