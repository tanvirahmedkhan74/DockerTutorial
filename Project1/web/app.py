from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017") # Setting the port and adjacent location of docker mongo
db = client.aNewDB  # Creating a Database
UserNum = db["UserNum"] # Creating a Collection

UserNum.insert_one({
    'num_of_user': 0
})      # Inserting a Document to the Collection [insert] is deprecated

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_user'] # UserNum.find({}) returns an array of documents
        prev_num += 1
        UserNum.update_one({}, {"$set":{'num_of_user':prev_num}})

        return str("Hello User " + str(prev_num))

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

# Routing Data to Paths for POST and GET operation using Api
api.add_resource(Addition, "/add")
api.add_resource(Subtraction, "/sub")
api.add_resource(Multiplication, "/multi")
api.add_resource(Division, "/div")
api.add_resource(Visit, "/hello")

@app.route('/')
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run(host ='0.0.0.0')
