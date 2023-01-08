from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def checkPostedData(data):
    if "x" not in data or "y" not in data:
        return 301
    else:
        return 200

class Addition(Resource):
    def post(self):
        reqData = request.get_json()
        status = checkPostedData(reqData)

        if status != 301:

            number_1 = int(reqData["x"])
            number_2 = int(reqData["y"])

            retJson = {
                "Addition Result": (number_1 + number_2),
                "Status Code": status
            }

            return jsonify(retJson)
        else:
            return jsonify({
                "Message":"Please Verify the Paramteres as x and y expected",
                "Status":status
            })

class Subtraction(Resource):
    def post(self):
        reqData = request.get_json()
        status = checkPostedData(reqData)

        if status != 301:

            number_1 = int(reqData["x"])
            number_2 = int(reqData["y"])

            retJson = {
                "Subtraction Result": (number_1 - number_2),
                "Status Code": status
            }

            return jsonify(retJson)
        else:
            return jsonify({
                "Message":"Please Verify the Paramteres as x and y expected",
                "Status":status
            })

class Multiplication(Resource):
    def post(self):
        reqData = request.get_json()
        status = checkPostedData(reqData)

        if status != 301:

            number_1 = int(reqData["x"])
            number_2 = int(reqData["y"])

            retJson = {
                "Multiplication Result": (number_1 * number_2),
                "Status Code": status
            }

            return jsonify(retJson)
        else:
            return jsonify({
                "Message":"Please Verify the Paramteres as x and y expected",
                "Status":status
            })

class Division(Resource):
    def post(self):
        reqData = request.get_json()
        status = checkPostedData(reqData)

        if status != 301 and reqData["y"] != 0:

            number_1 = int(reqData["x"])
            number_2 = int(reqData["y"])

            retJson = {
                "Division Result": (number_1 / number_2),
                "Status Code": status
            }

            return jsonify(retJson)
        elif reqData["y"] == 0:
            return jsonify({
                "Message": "Division By 0 is not Valid",
                "Status Code": 301
            })
        else:
            return jsonify({
                "Message":"Please Verify the Paramteres as x and y expected",
                "Status":status
            })

# Routing Data to /add for the Addition POST operation using Api
api.add_resource(Addition, "/add")
api.add_resource(Subtraction, "/sub")
api.add_resource(Multiplication, "/multi")
api.add_resource(Division, "/div")

@app.route('/')
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run(debug=True)
