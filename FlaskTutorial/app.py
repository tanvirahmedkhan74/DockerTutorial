from flask import Flask, jsonify

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
"""
@app.route('/bye')
def bye():
    retJsn = {
        'Whats the color of the sky':'ai mia mor mia mor',
        'Where should i put them shoes':'Ai mia mor mia mor',
        'You make me go':'Un poco loco'
    }

    return jsonify(retJsn)

#before running, export FLASK_APP = demo.py
if __name__ == "__main__":
    app.run(debug=True)
