#!/usr/bin/env python3
from flask import Flask, escape, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "Hola Pau! :D"

if __name__ == "__main__":
    app.run()
