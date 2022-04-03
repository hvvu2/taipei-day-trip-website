from flask import Blueprint, request, Response, session
from datetime import datetime
from models.database import db
import json, re

invalidId = "The attraction does not exist or the input is invalid."
emptyInput = "All inputs are required."
invalidFormat = "The format is invalid."
emailRegistered = "The email has already been registered."
incorrectSignIn = "The email or the password is incorrect."

def errorHandler(statusCode, message = "The argument is invalid."):
    if statusCode == 400:
        response = {
            "error": True,
            "message": message
        }
        return Response(json.dumps(response), status=400, mimetype="application/json")

    elif statusCode == 403:
        response = {
            "error": True,
            "message": "User is not signed in yet."
        }
        return Response(json.dumps(response), status=403, mimetype="application/json")

    elif statusCode == 500:
        response = {
            "error": True,
            "message": "Oops! It seems that our server went wrong."
        }
        return Response(json.dumps(response), status=500, mimetype="application/json")

def validateDate(date):
    currentDate = datetime.today().strftime("%Y-%m-%d")
    currentYear = int(currentDate.split("-")[0])
    currentMonth = int(currentDate.split("-")[1])
    currentDay = int(currentDate.split("-")[2])
    selectedYear = int(date.split("-")[0])
    selectedMonth = int(date.split("-")[1])
    selectedDay = int(date.split("-")[2])

    if selectedYear >= currentYear:
        if selectedMonth >= currentMonth:
            if selectedDay >= currentDay:
                return True

            else:
                return False

        else:
            return False    

    else:
        return False

# ===================================================================================== #

api = Blueprint("api_bp", __name__)

@api.route("/api/attractions", methods=["GET"])
def showAttractions():
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
def showTargetAttractions(attractionId):
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
            if session["signed"]:
                response = {
                    "data": {
                        "id": session["signed"][0],
                        "name": session["signed"][1],
                        "email": session["signed"][2]
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
                        if db.insertUser(name, email, pwd):
                            response = {
                                "ok": True
                            }
                            return json.dumps(response)

                        else:
                            return errorHandler(500)

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
            result = db.getUserInfo(email)

            if result:
                dbId = result[0]
                dbName = result[1]
                dbEmail = result[2]
                dbPwd = result[3]

                if (pwd == dbPwd):
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

    elif request.method == "DELETE":
        session.clear()

        response = {
            "ok": True
        }
        return json.dumps(response)


@api.route("/api/booking", methods=["GET", "POST", "DELETE"])
def bookTrips():
    if request.method == "GET":
        try:
            memberId = session["signed"][0]
            schedules = db.getScheduleInfo(memberId)

            if schedules:
                scheduleList = []

                for schedule in schedules:
                    scheduleInfo = {
                        "scheduleId": schedule[0],
                        "attraction": {
                            "id": schedule[4],
                            "name": schedule[5],
                            "address": schedule[6],
                            "image": schedule[7]
                        },
                        "date": schedule[8],
                        "time": schedule[9],
                        "price": schedule[10]
                    }

                    scheduleList.append(scheduleInfo)

                response = {
                    "data": scheduleList
                }
                return json.dumps(response, ensure_ascii=False)

            else:
                response = {
                    "data": None
                }
                return json.dumps(response)

        except:
            return errorHandler(403)


    elif request.method == "POST":
        try:
            data = request.get_json()
            memberId = session["signed"][0]
            name = session["signed"][1]
            email = session["signed"][2]
            attractionId = data["attractionId"]
            date = data["date"]
            time = data["time"]
            price = data["price"]

            if attractionId and date and time and price:
                if validateDate(date):
                    if db.insertSchedule(memberId, name, email, attractionId, date, time, price):
                        response = {
                            "ok": True
                        }
                        return json.dumps(response)
                    
                    else:
                        return errorHandler(500)
                
                else:
                    return errorHandler(400, invalidFormat)

            else:
                return errorHandler(400, emptyInput)

        except:
            return errorHandler(403)

    elif request.method == "DELETE":
        try:
            memberId = session["signed"][0]
            data = request.get_json()
            scheduleId = data["scheduleId"]

            if db.deleteSchedule(scheduleId, memberId):
                response = {
                    "ok": True
                }
                return json.dumps(response)

            else:
                return errorHandler(500)

        except:
            return errorHandler(403)
