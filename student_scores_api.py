
from flask import Flask, jsonify

app = Flask(__name__)

students = [
    {"name": "Asha", "score": 82},
    {"name": "Ravi", "score": 74},
    {"name": "Meera", "score": 91},
    {"name": "John", "score": 65},
    {"name": "Sara", "score": 88}
]

@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)

if __name__ == "__main__":
    app.run(debug=True)
