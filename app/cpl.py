import sqlite3
from os import path
import sys
import json

class Cpl:

    _instance = None

    def get_default():
        if Cpl._instance == None:
            app_path = path.dirname(path.realpath(__file__))
            Cpl._instance = Cpl(app_path + "/database/cpl.db")
        return Cpl._instance

    def __init__(self, db_path):
        self.db_path = db_path
        self._conn = None

    def _get_connection(self, force = False):
        if self._conn == None or force:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def get_tables(self):
        conn = self._get_connection()
        cur = conn.cursor()
        #Grab all tables that do not start with 'sqlite_' nor '_'.
        #Also, do not present 'anyliturgic', as this table has no ID and it's based on a year column.
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT IN ('anyliturgic') AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '\_%' ESCAPE '\\'")
        tables = []
        row = cur.fetchone()
        while row:
            tables.append(row[0])
            row = cur.fetchone()
        cur.close()
        return tables

    def get_table_data(self, table):
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        cur.close()
        if len(rows) == 0:
            return {}

        #Convert rows to a dictionary
        keys = rows[0].keys()
        data = []
        for row in rows:
            row_dic = {}
            for key in keys:
                row_dic[key] = row[key]
            data.append(row_dic)
        return data

    def update_field(self, table, column, id, new_value):
        try:
            sqliteConnection = self._get_connection()
            cursor = sqliteConnection.cursor()
            query = "UPDATE {0} SET {1} = '{2}' WHERE id = {3}"
            query = query.format(table, column, new_value, id)
            cursor.execute(query)
            sqliteConnection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(e)
            return False

    def get_changes(self, id):
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM _tables_log WHERE id > {id} ORDER BY id ASC")
        rows = cur.fetchall()
        cur.close()
        if len(rows) == 0:
            return {}

        #Convert rows to a dictionary
        keys = rows[0].keys()
        data_json = []
        i = 0
        for row in rows:
            row_dic = {}
            for key in keys:

                #Add key-value
                row_dic[key] = row[key]

                #Check for action UPDATE (2) in order to add all the column-values
                if key == 'action' and row[key] == 2:
                    table_name = row_dic["table_name"]
                    row_id = row_dic["row_id"]
                    row_dic["values"] = {}
                    cur = conn.cursor()
                    cur.execute(f"SELECT * FROM {table_name} WHERE id = {row_id}")
                    values = cur.fetchall()[0]
                    value_keys = values.keys()
                    cur.close()
                    j = 0
                    for value in values:
                        row_dic["values"][value_keys[j]] = value
                        j += 1

            data_json.append(row_dic)
            i += 1

        return data_json
            
    def __del__(self):
        if self._conn != None:
            self._conn.close()
