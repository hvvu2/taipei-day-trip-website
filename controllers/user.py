from flask import Blueprint, request, session
from models.database import db
from .module import errorHandler, emailPattern, namePattern, invalidFormat, incorrectSignIn, emptyInput, emailRegistered, sameUserName, salt
import json, re, hashlib

# ===================================================================================== #

user = Blueprint("user_api_bp", __name__)

@user.route("/api/user", methods=["GET", "POST", "PATCH", "PUT", "DELETE"])
def authUser():
    if request.method == "GET":
        try:
            response = {
                "data": {
                    "id": session["signed"][0],
                    "name": session["signed"][1],
                    "email": session["signed"][2]
                }
            }

        except:
            response = {
                "data": None
            }

        finally:
            return json.dumps(response)

    elif request.method == "POST":
        try:
            data = request.get_json()
            name = data["name"]
            email = data["email"]
            pwd = data["password"]

            if name and email and pwd:
                if re.match(namePattern, name) and re.match(emailPattern, email):
                    if db.checkEmail(email):
                        shaPwd = hashlib.sha256((pwd + salt).encode("utf-8")).hexdigest()
                        db.insertUser(name, email, shaPwd)
                        response = {
                            "ok": True
                        }
                        return json.dumps(response)

                    else:
                        return errorHandler(400, emailRegistered)

                else:
                    return errorHandler(400, invalidFormat)

            else:
                return errorHandler(400, emptyInput)
        
        except:
            return errorHandler(500)

    elif request.method == "PATCH":
        try:
            data = request.get_json()
            email = data["email"]
            pwd = data["password"]
            shaPwd = hashlib.sha256((pwd + salt).encode("utf-8")).hexdigest()
            result = db.getUserInfo(email)

            if result:
                dbId = result[0]
                dbName = result[1]
                dbEmail = result[2]
                dbPwd = result[3]

                if (shaPwd == dbPwd):
                    session["signed"] = [dbId, dbName, dbEmail]
                    response = {
                        "ok": True
                    }
                    return json.dumps(response)
                
                else:
                    return errorHandler(400, incorrectSignIn)

            else:
                return errorHandler(400, incorrectSignIn)

        except:
            return errorHandler(500)

    elif request.method == "PUT":
        try:
            memberId = session["signed"][0]

        except:
            return errorHandler(403)

        else:
            data = request.get_json()
            newName = data["new_name"]

            if newName:
                if re.match(namePattern, newName):
                    if db.checkUserName(memberId, newName):
                        db.changeUserName(memberId, newName)

                        session["signed"][1] = newName
                        response = {
                            "ok": True,
                            "new_name": newName
                        }
                        return json.dumps(response)

                    else:
                        return errorHandler(400, sameUserName)

                else:
                    return errorHandler(400, invalidFormat)

            else:
                return errorHandler(400, emptyInput)

    elif request.method == "DELETE":
        session.clear()

        response = {
            "ok": True
        }
        return json.dumps(response)