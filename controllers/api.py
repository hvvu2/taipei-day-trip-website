from flask import Blueprint, request, Response, session
from models.database import db
import json, re

def errorHandler(statusCode, message = "The argument is invalid, please retry."):
    if statusCode == 400:
        response = {
            "error": True,
            "message": message
        }
        return Response(json.dumps(response), status=400, mimetype="application/json")

    elif statusCode == 500:
        response = {
            "error": True,
            "message": "Oops! It seems that our server went wrong."
        }
        return Response(json.dumps(response), status=500, mimetype="application/json")

invalidId = "The attraction does not exist or the input is invalid, please retry."
emptyField = "All fields are required."
invalidFormat = "The format is invalid."
emailRegistered = "The email has already been registered."
incorrectSignIn = "The email or the password is incorrect."

# ===================================================================================== #

api = Blueprint("api_bp", __name__)

@api.route("/api/attractions", methods=["GET"])
def showAttractionList():
    try:
        currentPage = int(request.args.get("page"))
        keyword = request.args.get("keyword")        
        shownItems = 12

        def showNextPage(currentPage, lastPage):
            if currentPage < lastPage:
                return (currentPage + 1)
            
            else:
                return None

        def createData(i, data):
            item = data[i]
            imageList = []
            imageUrls = db.getImages(item[0])

            for imageUrl in imageUrls:
                imageList.append(imageUrl[0])

            itemInfo = {
                "id": item[0],
                "name": item[1],
                "category": item[2],
                "description": item[3],
                "address": item[4],
                "transport": item[5],
                "mrt": item[6],
                "latitude": float(item[7]),
                "longitude": float(item[8]),
                "images": imageList
            }
            itemList.append(itemInfo)

        if currentPage >= 0:
            if keyword:
                keyRawData = db.getRawDataByKeyword(keyword, currentPage, shownItems)
                totalItems = db.getKeywordCount(keyword)[0]
                lastPage = totalItems // shownItems
                restItems = totalItems % shownItems
                itemList = []

                if currentPage <= lastPage:
                    if totalItems != 0:
                        if ((currentPage + 1) * shownItems) > totalItems:
                            for item in range(restItems):
                                createData(item, keyRawData)

                        else:
                            for item in range(shownItems):
                                createData(item, keyRawData)

                        response = {
                            "nextPage": showNextPage(currentPage, lastPage),
                            "data": itemList
                        }
                        return json.dumps(response, ensure_ascii=False)

                    else:
                        response = {
                            "data": None
                        }
                        return json.dumps(response)

                else:
                    return errorHandler(400)

            else:
                rawData = db.getRawData(currentPage, shownItems)
                totalItems = db.getTotalCount()[0]
                lastPage = totalItems // shownItems
                restItems = totalItems % shownItems
                itemList = []

                if currentPage <= lastPage:
                    if ((currentPage + 1) * shownItems) > totalItems:
                        for item in range(restItems):
                            createData(item, rawData)

                    else:
                        for item in range(shownItems):
                            createData(item, rawData)

                    response = {
                        "nextPage": showNextPage(currentPage, lastPage),
                        "data": itemList
                    }
                    return json.dumps(response, ensure_ascii=False)

                else:
                    return errorHandler(400)

        else:
            return errorHandler(400)

    except (TypeError, ValueError):            
        return errorHandler(400)

    except:            
        return errorHandler(500)


@api.route("/api/attraction/<attractionId>", methods=["GET"])
def showTargetAttraction(attractionId):
    try:
        rawData = db.getRawDataById(attractionId)
        imageList = []
        imageUrls = db.getImages(attractionId)

        for imageUrl in imageUrls:
            imageList.append(imageUrl[0])

        response = {
            "data": {
                "id": rawData[0],
                "name": rawData[1],
                "category": rawData[2],
                "description": rawData[3],
                "address": rawData[4],
                "transport": rawData[5],
                "mrt": rawData[6],
                "latitude": float(rawData[7]),
                "longitude": float(rawData[8]),
                "images": imageList
            }
        }
        return json.dumps(response, ensure_ascii=False)

    except TypeError:
        return errorHandler(400, invalidId)

    except:
        return errorHandler(500)


@api.route("/api/user", methods=["GET", "POST", "PATCH", "DELETE"])
def authUser():
    pattern = r"(^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$)"

    if request.method == "GET":
        try:
            if session["logged"]:
                response = {
                    "data": {
                        "id": session["logged"][0],
                        "name": session["logged"][1],
                        "email": session["logged"][2]
                    }
                }
                return json.dumps(response)

        except:
            response = {
                "data": None
            }
            return json.dumps(response)

    elif request.method == "POST":
        try:
            data = request.get_json()
            name = data["name"]
            email = data["email"]
            pwd = data["password"]

            if name and email and pwd:
                if re.match(pattern, email):
                    if db.checkEmail(email):
                        db.insertUser(name, email, pwd)
                        response = {
                            "ok": True
                        }
                        return json.dumps(response)

                    else:
                        return errorHandler(400, emailRegistered)

                else:
                    return errorHandler(400, invalidFormat)

            else:
                return errorHandler(400, emptyField)
        
        except:
            return errorHandler(500)

    elif request.method == "PATCH":
        try:
            data = request.get_json()
            email = data["email"]
            pwd = data["password"]

            if db.getUserInfo(email):
                result = db.getUserInfo(email)
                dbId = result[0]
                dbName = result[1]
                dbEmail = result[2]
                dbPwd = result[3]

                if (pwd == dbPwd):
                    session["logged"] = [dbId, dbName, dbEmail]
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

    elif request.method == "DELETE":
        session.clear()

        response = {
            "ok": True
        }
        return json.dumps(response)
