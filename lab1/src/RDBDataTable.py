# by Shusen Xu 09/20
from src.BaseDataTable import BaseDataTable
import pymysql
import logging
import json
logger = logging.getLogger()


class RDBDataTable(BaseDataTable):

    """
    The implementation classes (XXXDataTable) for CSV database, relational, etc. with extend the
    base class and implement the abstract methods.
    """

    @staticmethod
    def _get_default_connection():
        result = pymysql.connect(host='localhost',
                                 user='dbuser',
                                 password='dbuserdbuser',
                                 db='lahman2019raw',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        return result

    def __init__(self, table_name, connect_info, key_columns):
        """

        :param table_name: Logical name of the table.
        :param connect_info: Dictionary of parameters necessary to connect to the data.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
        """
        self._data = {
            "table_name": table_name,
            "connect_info": connect_info,
            "key_columns": key_columns,
        }
        self.conn = RDBDataTable._get_default_connection()

        print("RDBDataTable link status:   " + str(self.conn))
        self._logger = logging.getLogger()

        self._logger.debug("RDBDataTable.__init__: data = " + json.dumps(self._data, indent=2))


    def find_by_primary_key(self, key_fields, field_list=None):
        """
        :param key_fields: The list with the values for the key_columns, in order, to use to find a record.
        :param field_list: A subset of the fields of the record to return.
        :return: None, or a dictionary containing the requested fields for the record identified
            by the key.
        """
        key_cols = self._data['key_columns']
        tmp = dict(zip(key_cols, key_fields))

        result = self.find_by_template(tmp, field_list)
        return result

    def run_q(self, sql, args=None, fetch=True, cur=None, commit=True):
        '''
        Helper function to run an SQL statement.

        :param sql: SQL template with placeholders for parameters.
        :param args: Values to pass with statement.
        :param fetch: Execute a fetch and return data.
        :param conn: The database connection to use. The function will use the default if None.
        :param cur: The cursor to use. This is wizard stuff. Do not worry about it for now.
        :param commit: This is wizard stuff. Do not worry about it.

        :return: A tuple of the form (execute response, fetched data)
        '''

        cursor_created = False
        connection_created = False
        try:

            if cur is None:
                cursor_created = True
                cur = self.conn.cursor()

            if args is not None:
                log_message = cur.mogrify(sql, args)
            else:
                log_message = sql

            logger.debug("Executing SQL = " + log_message)

            res = cur.execute(sql, args)

            if fetch:
                data = cur.fetchall()
            else:
                data = None

            # Do not ask.
            if commit == True:
                self.conn.commit()

        except Exception as e:
            raise e

        return res, data

    @staticmethod
    def template_to_where_clause(template):
        """

        :param template: One of those weird templates
        :return: WHERE clause corresponding to the template.
        """

        if template is None or template == {}:
            result = (None, None)
        else:
            args = []
            terms = []

            for k, v in template.items():
                terms.append(" " + k + "=%s ")
                args.append(v)
            
            w_clause = "AND".join(terms)
            w_clause = " WHERE " + w_clause

            result = (w_clause, args)

        return result

    def create_select(self, table_name, template, fields, order_by=None, limit=None, offset=None):
        """
        Produce a select statement: sql string and args.

        :param table_name: Table name: May be fully qualified dbname.tablename or just tablename.
        :param fields: Columns to select (an array of column name)
        :param template: One of Don Ferguson's weird JSON/python dictionary templates.
        :param order_by: Ignore for now.
        :param limit: Ignore for now.
        :param offset: Ignore for now.
        :return: A tuple of the form (sql string, args), where the sql string is a template.
        """
        if fields is None:
            field_list = " * "
        else:
            field_list = " " + ",".join(fields) + " "

        w_clause, args = self.template_to_where_clause(template)

        sql = "select " + field_list + " from " + table_name + " " + w_clause

        return sql, args

    def find_by_template(self, template, field_list=None, limit=None, offset=None, order_by=None):
        """

        :param template: A dictionary of the form { "field1" : value1, "field2": value2, ...}
        :param field_list: A list of request fields of the form, ['fielda', 'fieldb', ...]
        :param limit: Do not worry about this for now.
        :param offset: Do not worry about this for now.
        :param order_by: Do not worry about this for now.
        :return: A list containing dictionaries. A dictionary is in the list representing each record
            that matches the template. The dictionary only contains the requested fields.
        """
        sql, args = self.create_select(self._data['table_name'], template, field_list)

        result = self.run_q(sql, args)

        return result

    def delete_by_key(self, key_fields):
        """

        Deletes the record that matches the key.

        :param template: A template.
        :return: A count of the rows deleted.
        """
        key_cols = self._data['key_columns']
        tmp = dict(zip(key_cols, key_fields))

        result = self.delete_by_template(tmp)
        return result

    def create_delete(self, table_name, template):

        w_clause, args = self.template_to_where_clause(template)

        sql = "delete " + " from " + table_name + " " + w_clause

        return sql, args

    def delete_by_template(self, template):
        """
        :param template: Template to determine rows to delete.
        :return: Number of rows deleted.
        """
        sql, args = self.create_delete(self._data['table_name'], template)
        result = self.run_q(sql, args)
        print(str(result[0])+"  rows have been deleted")
        return result[0]

    def update_by_key(self, key_fields, new_values):
        """

        :param key_fields: List of value for the key fields.
        :param new_values: A dict of field:value to set for updated row.
        :return: Number of rows updated.
        """
        key_cols = self._data['key_columns']
        tmp = dict(zip(key_cols, key_fields))

        result = self.update_by_template(tmp, new_values)
        #print(str(result) + " rows have been updated ")
        return result

    def create_update(self, table_name, template, new_values):

        set_terms = []
        args = []

        for k, v in new_values.items():
            set_terms.append(k + "=%s")
            args.append(v)

        s_clause = ",".join(set_terms)
        w_clause, w_args = self.template_to_where_clause(template)

        # There are %s in the SET clause and the WHERE clause. We need to form
        # the combined args list.
        args.extend(w_args)

        sql = "update " + table_name + " set " + s_clause + " " + w_clause
        return sql, args

    def update_by_template(self, template, new_values):
        """

        :param template: Template for rows to match.
        :param new_values: New values to set for matching fields.
        :return: Number of rows updated.
        """
        # notes: run the sql, the DBMS will check duplicate error
        sql, args = self.create_update(self._data['table_name'], template, new_values)

        result = self.run_q(sql, args)
        print(str(result[0]) + " rows have been updated ")
        return result[0]

    def create_insert(self, table_name, row):
        result = "Insert into " + table_name + " "
        cols = []
        vals = []

        # This is paranoia. I know that calling keys() and values() should return in matching order,
        # but in the long term only the paranoid survive.
        for k, v in row.items():
            cols.append(k)
            vals.append(v)

        col_clause = "(" + ",".join(cols) + ") "

        no_cols = len(cols)
        terms = ["%s"] * no_cols
        terms = ",".join(terms)
        value_clause = " values (" + terms + ")"

        result += col_clause + value_clause

        return result, vals

    def insert(self, new_record):
        """
        :param new_record: A dictionary representing a row to add to the set of records.
        :return: None
        """
        sql, args = self.create_insert(self._data['table_name'],new_record)

        result = self.run_q(sql, args)
        print(str(result[0]) + " rows have been inserted ")
        return result[0]


    def get_rows(self):
        return self._rows



