#!/usr/bin/env python3
from flask import Flask, escape, request, render_template
from cpl import Cpl
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tables")
def get_tables():
    cpl = Cpl.get_default()
    return json.dumps(cpl.get_tables()), 200, {"Content-Type": "application/json"}

@app.route("/api/table/<string:name>")
def get_table_rows(name):
    cpl = Cpl.get_default()
    tables = cpl.get_tables()
    if name in tables:
        return json.dumps(cpl.get_table_data(name)), 200, {"Content-Type": "application/json"}
    else:
        return json.dumps("Table not found"), 404

@app.route("/api/update/<string:table>/<int:id>/<string:column>", methods = ['POST'])
def update_field(table, id, column):
    cpl = Cpl.get_default()
    new_value = request.data
    return new_value, 200, {"Content-Type": "text/plain"}
#    res = cpl.update_field(table, id, column)
#    if res == true:
#        return "{'result': 'ok'}", 200, {"Content-Type": "application/json"}
#    else:
#        return  json.dumps("Table not found"), 404

@app.route("/api/sync/<int:id>")
def sync_database():
    return json.dumps("Error: not implemented yet"), 501, {"Content-Type": "application/json"}

if __name__ == "__main__":
    app.run()
