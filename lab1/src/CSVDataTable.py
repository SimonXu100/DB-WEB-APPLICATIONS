#by Shusen Xu 9/20

from src.BaseDataTable import BaseDataTable
import copy
import csv
import logging
import json
import os
import pandas as pd

pd.set_option("display.width", 256)
pd.set_option('display.max_columns', 20)


class CSVDataTable(BaseDataTable):
    """
    The implementation classes (XXXDataTable) for CSV database, relational, etc. with extend the
    base class and implement the abstract methods.
    """

    _rows_to_print = 10
    _no_of_separators = 2

    def __init__(self, table_name, connect_info, key_columns, debug=True, load=True, rows=None):
        """

        :param table_name: Logical name of the table.
        :param connect_info: Dictionary of parameters necessary to connect to the data.
        :param key_columns: List, in order, of the columns (fields) that comprise the primary key.
        """
        self._data = {
            "table_name": table_name,
            "connect_info": connect_info,
            "key_columns": key_columns,
            "debug": debug
        }

        self._logger = logging.getLogger()

        self._logger.debug("CSVDataTable.__init__: data = " + json.dumps(self._data, indent=2))

        # by Shusen Xu OH
        #self._indexes = {'PRIMARY', K}

        if rows is not None:
            self._rows = copy.copy(rows)
        else:
            self._rows = []
            self._load()

    def __str__(self):

        result = "CSVDataTable: config data = \n" + json.dumps(self._data, indent=2)

        no_rows = len(self._rows)
        if no_rows <= CSVDataTable._rows_to_print:
            rows_to_print = self._rows[0:no_rows]
        else:
            temp_r = int(CSVDataTable._rows_to_print / 2)
            rows_to_print = self._rows[0:temp_r]
            keys = self._rows[0].keys()

            for i in range(0,CSVDataTable._no_of_separators):
                tmp_row = {}
                for k in keys:
                    tmp_row[k] = "***"
                rows_to_print.append(tmp_row)

            rows_to_print.extend(self._rows[int(-1*temp_r)-1:-1])

        df = pd.DataFrame(rows_to_print)
        result += "\nSome Rows: = \n" + str(df)

        return result
    def _add_row(self, r):
        if self._rows is None:
            self._rows = []
        self._rows.append(r)

    def _load(self):

        dir_info = self._data["connect_info"].get("directory")
        file_n = self._data["connect_info"].get("file_name")
        full_name = os.path.join(dir_info, file_n)

        with open(full_name, "r") as txt_file:
            csv_d_rdr = csv.DictReader(txt_file)
            for r in csv_d_rdr:
                self._add_row(r)

        self._logger.debug("CSVDataTable._load: Loaded " + str(len(self._rows)) + " rows")

    def save(self):
        """
        Write the information back to a file.
        :return: None
        """

        dir_info = self._data["connect_info"].get("directory")
        file_n = self._data["connect_info"].get("file_name")
        full_name = os.path.join(dir_info, file_n)

        with open(full_name, 'w') as csvFile:
            fields = self._rows[0].keys()
            writer = csv.DictWriter(csvFile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self._rows)
        
        self._logger.debug("CSVDataTable._save: Saved " + str(len(self._rows)) + " rows")

    @staticmethod
    def matches_template(row, template):

        result = True
        if template is not None:
            for k, v in template.items():
                if v != row.get(k, None):
                    result = False

                    break
        return result

    def key_to_template(self, key):
        tmp = {}
        key_cols = self._data['key_columns']
        tmp = dict(zip(key_cols, key))
        return tmp

    #project the result into specific field_list
    @staticmethod
    def project(row, field_list):
        result = {}
        if field_list is None:
            return row
        for f in field_list:
            result[f] = row[f]
        return result

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
        # by Shusen Xu:  selected based on field_list
        result = []
        for r in self._rows:
            if CSVDataTable.matches_template(r, template):
                new_r = CSVDataTable.project(r, field_list)
                result.append(new_r)
        return result

    def find_by_primary_key(self, key_fields, field_list=None):

        key_cols = self._data['key_columns']
        tmp = dict(zip(key_cols, key_fields))

        result = self.find_by_template(template=tmp, field_list=field_list)
        '''
        if result is not None and len(result) > 0:
            result = result[0]
        else:
            result = None
        '''
        return result

    def delete_by_key(self, key_fields):
        """

        Deletes the record that matches the key.

        :param template: A template.
        :return: A count of the rows deleted.
        """
        #pass
        # the number of rows being affected
        count = 0
        if key_fields is None:
            print('0  ' + "has been deleted")
            return count

        key_cols = self._data['key_columns']
        tmp = dict(zip(key_cols, key_fields))

        result = self.delete_by_template(tmp)

        return result

    def delete_by_template(self, template):
        """

        :param template: Template to determine rows to delete.
        :return: Number of rows deleted.
        """
        count = 0
        result = self._rows
        for r in self._rows:
            if CSVDataTable.matches_template(r, template):
                result.remove(r)
                count = count + 1
        print(str(count) + "  rows have been deleted.")
        return count

    def update_by_key(self, key_fields, new_values):
        """

        :param key_fields: List of value for the key fields.
        :param new_values: A dict of field:value to set for updated row.
        :return: Number of rows updated.
        """
        # duplicate error
        #condition 1: no primary key value were updated
        # updated key_fields template: a dictionary
        #represent whether any value belong to primary key columns were updated
        flag = False
        key_cols = self._data['key_columns']
        key_fields_updated = dict(zip(key_cols, key_fields))
        for k, v in new_values.items():
            if k in self._data['key_columns']:
                key_fields_updated[k] = v
                flag = True
        # condition 1: updated values belong to primary key columns
        # recursively check if duplicate primary key
        if flag:
            for r in self._rows:
                if CSVDataTable.matches_template(r, key_fields_updated):
                    print("Error: duplicate key update error!!!")
                    print('0 ' + "row has been updated")
                    return 0
        # condition 2: the values belong to primary key columns were not updated
        # no need any additional handling

        count = 0
        # find the specified row
        tmp_key = self.key_to_template(key_fields)

        # store the current result
        result = self._rows

        # update
        for r in result:
            if CSVDataTable.matches_template(r, tmp_key):
                for k, v in new_values.items():
                    r[k] = v
                count = count + 1
        print(str(count) + "  rows have been updated")
        return count

    def update_by_template(self, template, new_values):
        """

        :param template: Template for rows to match.
        :param new_values: New values to set for matching fields.
        :return: Number of rows updated.
        """
        if template is None or new_values is None:
            return 0

        key_cols = self._data['key_columns']
        result = self._rows

        # duplicate error
       
        flag = False
        key_fields = []
        for r in result:
            if CSVDataTable.matches_template(r, template):
                for k in self._data['key_columns']:
                    key_fields.append(r[k])
                key_template = dict(zip(key_cols, key_fields))
                for k, v in new_values.items():
                    if k in self._data['key_columns']:
                        key_template[k] = v
                        flag = True
                # condition 1: updated values belong to primary key columns
                # recursively check if duplicate primary key
                if flag:
                    for r1 in self._rows:
                        if CSVDataTable.matches_template(r1, key_template):
                            print("Error: duplicate key update error!!!")
                            print('0 ' + "row has been updated")
                            return 0
                flag = False


        # no duplicate error
        count = 0
        # store the current result
        # update
        for r in result:
            if CSVDataTable.matches_template(r, template):
                for k, v in new_values.items():
                    r[k] = v
                count = count + 1
        print(str(count) + "  rows have been updated")
        return count

    def insert(self, new_record):
        """

        :param new_record: A dictionary representing a row to add to the set of records.
        :return: None
        """
        temp = {}
        # duplicate error
        for k, v in new_record.items():
            if k in self._data['key_columns']:
                temp[k] = v
        flag = False
        for r in self._rows:
            if CSVDataTable.matches_template(r, temp):
                flag = True
                break
        if flag:
            print("Error: duplicate key update error!!!")
            print('0 ' + "row has been updated")
            return

        # store the current result
        result = self._rows
        # insert
        result.append(new_record)
        print(" 1 row have been inserted")

    def get_rows(self):
        return self._rows

