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
        return  json.dumps("Table not found"), 404

if __name__ == "__main__":
    app.run()
