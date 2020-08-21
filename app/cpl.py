import sqlite3
from os import path
import sys

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
        #Grab all tables that do not start with 'sqlite_' or '_'.
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
            
    def __del__(self):
        if self._conn != None:
            self._conn.close()
