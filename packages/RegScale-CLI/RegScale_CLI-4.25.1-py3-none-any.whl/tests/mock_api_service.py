#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mock API Service"""

# standard library imports
import os
from flask import Flask, request

app = Flask(__name__)


@app.route("/api/checkServer", methods=["GET"])
def check_server():
    """Used to check if the server is running"""
    return "True"





if __name__ == "__main__":
    app.run(debug=True, port=5050)
