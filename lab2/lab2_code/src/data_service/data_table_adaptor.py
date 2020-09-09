import pymysql
import src.data_service.dbutils as dbutils
import src.data_service.RDBDataTable as RDBDataTable

# The REST application server app.py will be handling multiple requests over a long period of time.
# It is inefficient to create an instance of RDBDataTable for each request.  This is a cache of created
# instances.
# Dictionary
_db_tables = {}
# get from the OH
#db='lahman2019clean'
_conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='dbuserdbuser',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor

)



def get_rdb_table(table_name, db_name, key_columns=None, connect_info=None):
    """

    :param table_name: Name of the database table.
    :param db_name: Schema/database name.
    :param key_columns: This is a trap. Just use None.
    :param connect_info: You can specify if you have some special connection, but it is
        OK to just use the default connection.
    :return:
    """
    global _db_tables

    # We use the fully qualified table name as the key into the cache, e.g. lahman2019clean.people.
    key = db_name + "." + table_name

    # Have we already created and cache the data table?
    result = _db_tables.get(key, None)

    # We have not yet accessed this table.
    if result is None:

        # Make an RDBDataTable for this database table.
        result = RDBDataTable.RDBDataTable(table_name, db_name, key_columns, connect_info)

        # Add to the cache.
        _db_tables[key] = result

    return result


#########################################
#
#
# YOU HAVE TO IMPLEMENT THE FUNCTIONS BELOW.
#
#
# -- TO IMPLEMENT --
#########################################

def get_databases():
    """

    :return: A list of databases/schema at this endpoint.
    """
    # -- TO IMPLEMENT --
    #pass

    #get from the OH
    q = "show databases;"
    res, data = dbutils.run_q(q, conn=_conn)
    return data

def get_tables(dbname):
    """

      :return: A list of databases/schema/tables at this endpoint.
      """

    q1 = "use " + dbname + ";"
    q2 = "show tables;"

    res1, data1 = dbutils.run_q(q1, conn=_conn)
    res2, data2 = dbutils.run_q(q2, conn=_conn)
    return data2














