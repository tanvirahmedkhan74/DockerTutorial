from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hellow_world():
    return "Hello World"

@app.route('/hithere')
def hi_there_mes():
    return "Good to see you guys here!"

"""
# Web service - returns json / Web App - return page or rendered template

# Server-Server, Browser-Browser, Server-Browser Communication happens in TEXT with TCP protocol

ex: rep of image in text -> 2x4 pixel
[
122 123 122 111
222 121 211 233
]

JSON file can represent ->
Number , String, Boolean, Array (Homogenious and Non Homo), Array of JSON objects, Multi dim Array
"""
@app.route('/bye')
def bye():
    retJsn = {
        'Whats the color of the sky':'ai mia mor mia mor',
        'Where should i put them shoes':'Ai mia mor mia mor',
        'You make me go':'Un poco loco'
    }

    retJsn2 = {
        'name':'Tanvir Ahmed Khan',
        'age' : 22,
        'Experience':[
            {
                'framework':'Spring boot',
                'Language and Build': ['Java', 'Maven', 'Gradel']
            },
            {
                'framework':'Django',
                'Language and Build': ['Python']
            },
            {
                'framework':'Flask',
                'Language and Build': ['Python']
            }
        ]
    }

    return jsonify(retJsn2)

"""
# Method for handling post request
# request.get_json() can parse the post req and then Using dictionary
# indexing to access the arrived data
"""
@app.route('/add_two_number', methods=["POST"])
def add_two_number():
    data = request.get_json()

    x = data["x"]
    y = data["y"]

    retJson = {
        'z': x + y
    }

    return jsonify(retJson), 200


#before running, export FLASK_APP = demo.py
if __name__ == "__main__":
    app.run(debug=True)
