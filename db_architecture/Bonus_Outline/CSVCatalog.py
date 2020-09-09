import pymysql  # connect to your root server
import json  # json object

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

    #example of what column types are acceptable
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

    def __init__(self, index_name: object, index_type: object, column_names: object) -> object:
        """
        :param index_name: Name for index. Must be unique name for table.
        :param index_type: Valid index type.
        :param column_names: list of column names assc with that index
        """
        #YOUR CODE GOES HERE#


    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    def to_json(self):

        #YOUR CODE GOES HERE#


        return


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

        if not load:

            if t_name is None or csv_f is None:
                raise ValueError("Table and file must both have a name")

            self.file_name = csv_f
            self.save_core_definition()

            if column_definitions is not None:
                for c in column_definitions:
                    self.add_column_definition(c)

            if index_definitions is not None:
                for idx in index_definitions:
                    self.define_index(idx)

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
    def load_indexes(self):
        '''
        #YOUR CODE HERE
        '''

    def save_core_definition(self):
        '''
        #YOUR CODE HERE
        '''

    def load_core_definition(self):
        '''
        #YOUR CODE HERE
        '''

    def __str__(self):
        return json.dumps(self.to_json(), indent=2)

    @classmethod  # classmethod means method that can be called by objects of this class
    def add_column_definition(self, c):
        """
        Add a column definition.
        :param c: New column. Cannot be duplicate or column not in the file.
        :return: None
        """
        '''
        #YOUR CODE HERE
        '''

    def get_column(self, cn):
        """
        Returns a column of the current table so that it can be deleted from the columns list
        :param cn: name of the column you are trying to get.
        :return:
        """
        '''
        #YOUR CODE HERE
        '''
    def drop_column_definition(self, c):
        """
        Remove from definition and catalog tables.
        :param c: Column name (string)
        :return:
        """

        '''
        #YOUR CODE HERE
        '''


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
            for c in self.columns:
                result['columns'].append(c.to_json())

        if self.indexes is not None:
            result['indexes'] = []
            for idx in self.indexes:
                result['indexes'].append(idx.to_json())
        return result

    def define_primary_key(self, columns):
        """
        Define (or replace) primary key definition.
        :param columns: List of column values in order.
        :return:
        """
        pass

    def save_index_definition(self, i_name, cols, type):
        # changed kind to type

        '''
        #YOUR CODE HERE
        '''

    def define_index(self, index_name, columns, kind="index"):
        """
        Define or replace and index definition.
        :param index_name: Index name, must be unique within a table.
        :param columns: Valid list of columns.
        :param kind: One of the valid index types.
        :return:
        """
        self.save_index_definition(index_name, columns, kind)
        if self.indexes is None:
            self.indexes = []
        for i in range(0, len(columns)):
            new_idx = IndexDefinition(index_name, kind, columns[i].column_name)
            self.indexes.append(new_idx)

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
        pass

    def create_table(self, table_name, file_name, column_definitions=None, primary_key_columns=None):
        result = TableDefinition(table_name, file_name, cnx=self.cnx)
        return result

    def drop_table(self, table_name):
        '''
        #YOUR CODE HERE
        '''


    def get_table(self, table_name):
        '''
        #YOUR CODE HERE
        '''

