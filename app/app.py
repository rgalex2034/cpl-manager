#!/usr/bin/env python3
from flask import Flask, escape, request, render_template
from cpl import Cpl
import json
import sys

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

@app.route("/api/update/<string:table>/<string:column>/<int:id>", methods = ['POST'])
def update_field(table, column, id):
    cpl = Cpl.get_default()
    new_value = json.loads(request.data)["data"]
    if cpl.update_field(table, column, id, new_value):
        return "", 200
    else:
        return "", 404

@app.route("/api/sync/<int:id>")
def sync_database():
    return json.dumps("Error: not implemented yet"), 501, {"Content-Type": "application/json"}

if __name__ == "__main__":
    app.run()
