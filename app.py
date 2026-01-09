from marigold.parser import parser
from marigold.compiler import Compiler
from marigold.lambdas import *
from marigold.lcode import lambdacode
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys

sys.setrecursionlimit(1000000)

app = Flask(__name__)
CORS(app)

@app.route('/',methods=["POST"])
def main():
    try:
        print(request.get_json())

        tree = parser.parse(request.get_json().get("code"))

        print(tree.pretty())

        c = Compiler('').transform(tree)

        print("\nSending:",c)

        return jsonify({"code":lambdacode+c})
    except Exception as e:
        return e

if __name__ == '__main__':
    app.run()
