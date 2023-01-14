from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentenceDB # Db name
users = db["users"] # CollectionCreation

def valid_reg_verifier(data):
    if "username" not in data and "password" not in data:
        return 310
    elif "username" not in data:
        return 311
    elif "password" not in data:
        return 312
    else:
        return 200


def valid_store_verifier(data):
    if "username" not in data and "password" not in data and "sentence" not in data:
        return 310
    elif "username" not in data:
        return 311
    elif "password" not in data:
        return 312
    elif "sentence" not in data:
        return 315
    else:
        return 200

def verifyPw(username, password):
    hashed_pass = users.find({"Username": username})[0]["Password"]

    return bcrypt.hashpw(password.encode('utf8'), hashed_pass) == hashed_pass

def verifyToken(username):
    tokens = users.find({"Username":username})[0]["Tokens"]
    return tokens

class Register(Resource):
    def post(self):
        fetchedData = request.get_json()

        stats = valid_reg_verifier(fetchedData)

        if stats == 200:
            username = fetchedData["username"]
            password = fetchedData["password"]

            # Encrypting the Password
            hashed_pass = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

            # Searching for Existing user with the same name
            exist = users.find({"Username": username})
            exist_list = list(exist)

            if  len(exist_list) != 0:
                message = "User with name " + username + " Already Exists!\nTry Logging In"
                return jsonify({
                    'message': message,
                    'status': 313
                })

            # Inserting new user to the DB
            users.insert_one({
                "Username": username,
                "Password": hashed_pass,
                "Sentences": "",
                "Tokens": 6
            })

            return jsonify({
                'message': "Registration Successful!",
                'status': 200
            })

        else:                           # Unsuccessful Registration Try
            message = ""
            if stats == 310:
                message = "Please Enter Username & Password"
            elif stats == 311:
                message = "Please Enter a Username -_-"
            else:
                message = "Please Enter a Password -_-"

            return jsonify({
                'message': message,
                'status': stats
            })

class Store(Resource):
    def post(self):
        fetchedData = request.get_json()
        stats = valid_store_verifier(fetchedData)

        if stats == 200:
            username = fetchedData["username"]
            password = fetchedData["password"]
            sentence = fetchedData["sentence"]

            # Verifying the Credentials
            logIn_stats = verifyPw(username, password)

            if not logIn_stats:
                return jsonify({
                    "message": "Credentials does not match!"
                })

            # Verifying how many Token Left
            token = verifyToken(username)

            if token <= 0:
                return jsonify({
                    "message":"You ran out of tokens!"
                })

            # Updating the Sentence and the token value
            users.update_one({"Username":username},
            {"$set":{
                "Sentences": sentence,
                "Tokens": token - 1
            }})

            return jsonify({
                "message":"Sentence Saved Succesfully",
                "Token Left": token - 1
            })


        else:
            message = ""
            if stats == 310:
                message = "Please Enter Username & Password"
            elif stats == 311:
                message = "Please Enter a Username -_-"
            elif stats == 315:
                message = "Please Enter a Sentence!"
            else:
                message = "Please Enter a Password -_-"

            return jsonify({
                'message': message,
                'status': stats
            })

class GetSentence(Resource):
    def post(self):
        fetchedData = request.get_json()
        stats = valid_reg_verifier(fetchedData)

        if stats == 200:
            username = fetchedData["username"]
            password = fetchedData["password"]

            # Verifying the Credentials
            logIn_stats = verifyPw(username, password)

            if not logIn_stats:
                return jsonify({
                    "message": "Credentials does not match!"
                })

            # Verifying how many Token Left
            token = verifyToken(username)

            if token <= 0:
                return jsonify({
                    "message":"You ran out of tokens!"
                })

            # Fetching the sentence from the DB
            retSent = users.find({"Username": username})[0]["Sentences"]

            # Updating the token value
            users.update_one({"Username":username},
            {"$set":{
                "Tokens": token - 1
            }})

            return jsonify({
                "Sentence": retSent,
                "Token Left": token - 1,
                "Status": 200
            })


        else:
            message = ""
            if stats == 310:
                message = "Please Enter Username & Password"
            elif stats == 311:
                message = "Please Enter a Username -_-"
            else:
                message = "Please Enter a Password -_-"

            return jsonify({
                'message': message,
                'status': stats
            })


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(GetSentence, '/sentence')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
