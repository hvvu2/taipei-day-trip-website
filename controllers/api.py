from flask import Blueprint, request, Response, session
from datetime import datetime
from models.database import db
import json, re, random, os, requests

invalidId = "The attraction does not exist or the input is invalid."
emptyInput = "All inputs are required."
invalidFormat = "The format is invalid."
emailRegistered = "The email has already been registered."
incorrectSignIn = "The email or the password is incorrect."
emailPattern = r"(^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$)"
phonePattern = r"(^09\d{8}$)"

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

def genOrderNumber():
    date = str(datetime.today()).split(" ")[0]
    time = str(datetime.today()).split(" ")[1]
    argsA = date[2:4] + date[5:7] + date[8:10]
    argsB = time[6:8] + time[3:5] + time[0:2]
    argsC = str(random.randint(10, 99))
    orderNumber = argsA + argsB + argsC
    return orderNumber

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
    if request.method == "GET":
        try:
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
                if re.match(emailPattern, email):
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
def manageSchedules():
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
                            "id": schedule[7],
                            "name": schedule[8],
                            "address": schedule[9],
                            "image": schedule[10]
                        },
                        "date": schedule[4],
                        "time": schedule[5],
                        "price": schedule[6]
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
            memberId = session["signed"][0]

            try:
                data = request.get_json()
                name = session["signed"][1]
                email = session["signed"][2]
                date = data["date"]
                time = data["time"]
                price = data["price"]
                attractionId = data["attractionId"]
                attractionInfo = db.getRawDataById(attractionId)
                attractionName = attractionInfo[1]
                attractionAddress = attractionInfo[4]
                attractionCover = attractionInfo[9]

                if attractionId and date and time and price:
                    if validateDate(date):
                        db.insertSchedule(memberId, name, email, date, time, price, attractionId, attractionName, attractionAddress, attractionCover)
                        response = {
                            "ok": True
                        }
                        return json.dumps(response)
                    
                    else:
                        return errorHandler(400, invalidFormat)

                else:
                    return errorHandler(400, emptyInput)

            except:
                return errorHandler(500)

        except:
            return errorHandler(403)

    elif request.method == "DELETE":
        try:
            memberId = session["signed"][0]

            try:
                data = request.get_json()
                scheduleId = data["scheduleId"]

                db.deleteSchedule(scheduleId, memberId)
                response = {
                    "ok": True
                }
                return json.dumps(response)

            except:
                errorHandler(500)

        except:
            return errorHandler(403)


@api.route("/api/orders", methods=["POST"])
def processPayment():
    try:
        memberId = session["signed"][0]

        try: 
            orderInfo = request.get_json()
            prime = orderInfo["prime"]
            partnerKey = os.getenv("PARTNER_KEY")
            orderTime = str(datetime.today())[0:19]
            orderNumber = genOrderNumber()
            price = orderInfo["order"]["price"]
            schedules = orderInfo["order"]["trip"]
            contactName = orderInfo["order"]["contact"]["name"]
            contactEmail = orderInfo["order"]["contact"]["email"]
            contactPhone = orderInfo["order"]["contact"]["phone"]

            if prime and price and schedules and contactName and re.match(emailPattern, contactEmail) and re.match(phonePattern, contactPhone):
                db.insertOrder(orderTime, orderNumber, price, contactName, contactEmail, contactPhone)

                for schedule in schedules:
                    scheduleId = schedule["scheduleId"]

                    db.insertOrderDetail(orderNumber, scheduleId)

                url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
                headers = {
                    "Content-Type": "application/json",
                    "x-api-key": os.getenv("PARTNER_KEY")
                }
                body = {
                    "prime": prime,
                    "partner_key": partnerKey,
                    "merchant_id": "hvvu2_CTBC",
                    "details":"TapPay Test",
                    "amount": price,
                    "cardholder": {
                        "phone_number": contactPhone,
                        "name": contactName,
                        "email": contactEmail,
                        "zip_code": "",
                        "address": "",
                        "national_id": ""
                    }
                }
                paymentResponse = requests.post(url, json=body, headers=headers).json()

                if paymentResponse["status"] == 0:
                    db.updateOrderStatus(orderNumber)
                    db.clearAllSchedules(memberId)

                    response = {
                        "data": {
                            "number": orderNumber,
                            "payment": {
                            "status": 0,
                            "message": "Payment completed."
                            }
                        }
                    }
                    return json.dumps(response)

                else:
                    response = {
                        "data": {
                            "number": orderNumber,
                            "payment": {
                            "status": 1,
                            "message": "Failed to process payment."
                            }
                        }
                    }
                    return json.dumps(response)
            
            else:
                return errorHandler(400, invalidFormat)
        
        except:
            return errorHandler(500)

    except:
        return errorHandler(403)
