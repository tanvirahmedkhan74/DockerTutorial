from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.PlagarismDB # Database Creation
users = db["Users"] # Collection Creation

def valid_register_request_check(data):
    message = ""
    if "username" not in data and "password" not in data:
        message = "Plase Enter a Username and Password"
    elif "username" not in data:
        message = "Please Enter a Username"
    elif "password" not in data:
        message = "Please enter a Password"
    else:
        message = "OK"

    return message


def valid_username_check(username):
    cursor = users.find({"Username": username})
    cursor = list(cursor)

    return (len(cursor) == 0)


def valid_detect_check(data):
    message = "OK"
    if "text1" not in data or "text2" not in data:
        message = "Please Input two text for comparison"

    return message


def verifyPw(username, password):
    if not valid_username_check(username):
        hashed_pw = users.find({"Username": username})[0]["Password"]
        return (bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw)
    return False


def countTokens(username):
    return users.find({"Username":username})[0]["Tokens"]


def valid_refil_request(data):
    message = ""
    current_token = users.find({"Username": data["username"]})[0]["Tokens"]

    if "refill" not in data:
        message = "Please Enter a Valid Refill Amount"
    elif current_token == 10:
        message = "You have already reached Maximum Token Limit (10)"
    elif current_token + data["refill"] > 10:
        message = "You can request for max " + str(10 - current_token) + " Tokens! (5 at a time)"
    elif data["refill"] > 5:
        message = "You can not refill for more than 5 Token at a Time!"
    else:
        message = "OK"

    return message

class Registration(Resource):
    def post(self):
        fetchedData = request.get_json()
        req_check = valid_register_request_check(fetchedData)

        if req_check == "OK":
            username = fetchedData["username"]
            password = fetchedData["password"]

            if valid_username_check(username):
                hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
                users.insert_one({
                    "Username": username,
                    "Password": hashed_pw,
                    "Tokens": 6
                })

                return jsonify({
                    "message": "The Registration was Successful!",
                    "token_left": 6,
                    "status": 200
                })
            else:
                message = "The username " + username + " Already Exist. Log in Perhaps?"
                return jsonify({
                    "message": message,
                    "status": 315
                })
        else:
            return jsonify({
                "message": req_check
            })

class PlagarismDetection(Resource):
    def post(self):
        fetchedData = request.get_json()

        req_check_1 = valid_register_request_check(fetchedData)
        req_check_2 = valid_detect_check(fetchedData)

        retMessage = ""
        status = 0

        if req_check_1 == "OK" and req_check_2 == "OK":
            username = fetchedData["username"]
            password = fetchedData["password"]
            text1 = fetchedData["text1"]
            text2 = fetchedData["text2"]

            # Credentials Verification
            pass_verify = verifyPw(username, password)

            if pass_verify:
                tokens = countTokens(username)

                if tokens <= 0:
                    retMessage = "You have ran out of tokens! Please do Refill"
                else:
                    # Detection Phase
                    nlp = spacy.load('en_core_web_sm')

                    text1 = nlp(text1)
                    text2 = nlp(text2)

                    # More closer to 1 means more match
                    ratio = text1.similarity(text2)

                    retMessage = "Similarity Between Text1 & Text2: " + str(ratio * 100) + "%"
                    status = 200

                    # Updating Token
                    users.update_one({"Username": username},
                        {
                            "$set": {"Tokens": tokens - 1}
                        })
            else:
                retMessage = "Credentials does not match!"
                status = 301
        elif req_check_1 != "OK":
            retMessage = req_check_1
            status = 302
        else:
            status = 303
            retMessage = req_check_2

        return jsonify({
            "Message": retMessage,
            "Status": status
        })


class TokenRefil(Resource):
    def post(self):

        fetchedData = request.get_json()
        # Username and Password Check
        req_check_1 = valid_register_request_check(fetchedData)
        # Refill Request
        req_check_2 = valid_refil_request(fetchedData)

        retMessage = ""
        status = 0

        # Credentials and Refill Request Successful
        if req_check_1 == "OK" and req_check_2 == "OK":
            username = fetchedData["username"]
            password = fetchedData["password"]
            refill = fetchedData["refill"]

            # Password Verification
            pass_verify = verifyPw(username, password)

            if pass_verify:
                current_token = users.find({"Username": username})[0]["Tokens"]
                # Update Token
                users.update_one({"Username": username}, {"$set": {"Tokens": current_token + refill}})
                retMessage = "Token Refilled Successfully!"
                status = 200
            else:
                retMessage = "Credentials does not match!"
                status = 303
        elif req_check_1 != "OK":
            retMessage = req_check_1
            status = 301
        else:
            retMessage = req_check_2
            status = 302

        return jsonify({
            "Message": retMessage,
            "Status": status
        })



api.add_resource(Registration, "/register")
api.add_resource(PlagarismDetection, "/detect")
api.add_resource(TokenRefil, "/refill")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
