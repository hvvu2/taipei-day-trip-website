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
            
        except:
            return errorHandler(403)

        else:
            schedules = db.getScheduleInfo(memberId)

            if schedules:
                scheduleList = []

                for schedule in schedules:
                    scheduleInfo = {
                        "scheduleId": schedule[0],
                        "attraction": {
                            "id": schedule[5],
                            "name": schedule[6],
                            "address": schedule[7],
                            "image": schedule[8]
                        },
                        "date": schedule[2],
                        "time": schedule[3],
                        "price": schedule[4]
                    }
                    scheduleList.append(scheduleInfo)

                response = {
                    "data": scheduleList
                }

            else:
                response = {
                    "data": None
                }

            return json.dumps(response, ensure_ascii=False)

    elif request.method == "POST":
        try:
            memberId = session["signed"][0]

        except:
            return errorHandler(403)

        else:
            data = request.get_json()
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
                    db.insertSchedule(memberId, date, time, price, attractionId, attractionName, attractionAddress, attractionCover)
                    response = {
                        "ok": True
                    }
                    return json.dumps(response)
                
                else:
                    return errorHandler(400, invalidFormat)

            else:
                return errorHandler(400, emptyInput)

    elif request.method == "DELETE":
        try:
            memberId = session["signed"][0]
        
        except:
            return errorHandler(403)

        else:
            data = request.get_json()
            scheduleId = data["scheduleId"]

            db.deleteSchedule(scheduleId, memberId)
            response = {
                "ok": True
            }
            return json.dumps(response)


@api.route("/api/orders", methods=["GET", "POST"])
def manageOrders():
    if request.method == "GET":
        try:
            memberId = session["signed"][0]

        except:
            return errorHandler(403)

        else:
            orders = db.getOrders(memberId)
                
            if orders:
                orderList = []

                for order in orders:
                    orderNumber = order[0]
                    orderTime = str(order[1])[0:16]
                    orderPrice = order[2]
                    contactName = order[3]
                    contactEmail = order[4]
                    contactPhone = order[5]
                    
                    orderInfo = {
                        "number": orderNumber,
                        "time": orderTime,
                        "price": orderPrice,
                        "contact": {
                            "name": contactName,
                            "email": contactEmail,
                            "phone": contactPhone
                        }
                    }

                    orderList.append(orderInfo)
                
                response = {
                    "data": orderList
                }

            else:
                response = {
                    "data": None
                }

            return json.dumps(response, ensure_ascii=False)

    elif request.method == "POST":
        try:
            memberId = session["signed"][0]

        except:
            return errorHandler(403)

        else:
            orderInfo = request.get_json()
            prime = orderInfo["prime"]
            partnerKey = os.getenv("PARTNER_KEY")
            merchantId = os.getenv("MERCHANT_ID")
            orderTime = str(datetime.today())[0:19]
            orderNumber = genOrderNumber() + str(memberId)
            orderPrice = orderInfo["order"]["price"]
            schedules = orderInfo["order"]["trip"]
            contactName = orderInfo["order"]["contact"]["name"]
            contactEmail = orderInfo["order"]["contact"]["email"]
            contactPhone = orderInfo["order"]["contact"]["phone"]

            if prime and orderPrice and schedules and contactName and re.match(emailPattern, contactEmail) and re.match(phonePattern, contactPhone):
                db.insertOrder(memberId, orderTime, orderNumber, orderPrice, contactName, contactEmail, contactPhone)

                for schedule in schedules:
                    scheduleDate = schedule["date"]
                    scheduleTime = schedule["time"]
                    attractionId = schedule["attraction"]["id"]
                    attractionName = schedule["attraction"]["name"]
                    attractionAddress = schedule["attraction"]["address"]
                    attractionCover = schedule["attraction"]["image"]

                    db.insertOrderDetail(orderNumber, scheduleDate, scheduleTime, attractionId, attractionName, attractionAddress, attractionCover)

                url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
                headers = {
                    "Content-Type": "application/json",
                    "x-api-key": partnerKey
                }
                body = {
                    "prime": prime,
                    "partner_key": partnerKey,
                    "merchant_id": merchantId,
                    "details":"TapPay Test",
                    "amount": orderPrice,
                    "cardholder": {
                        "phone_number": contactPhone,
                        "name": contactName,
                        "email": contactEmail,
                    }
                }
                paymentResponse = requests.post(url, json=body, headers=headers).json()

                if paymentResponse:
                    db.updateOrderStatus(orderNumber)

                    if paymentResponse["status"] == 0:
                        db.updatePaymentStatus(orderNumber)
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
                    return errorHandler(500)
            
            else:
                return errorHandler(400, invalidFormat)


@api.route("/api/order/<orderNumber>", methods=["GET"])
def getOrderDetails(orderNumber):
    try:
        session["signed"]

    except:
        return errorHandler(403)

    else:
        trips = db.getOrderDetails(orderNumber)
        tripList = []
        
        for trip in trips:
            attractionId = trip[0]
            attractionName = trip[1]
            attractionAddress = trip[2]
            scheduleDate = trip[4]
            scheduleTime = trip[5]

            tripInfo = {
                "attraction": {
                    "id": attractionId,
                    "name": attractionName,
                    "address": attractionAddress
                },
                "date": scheduleDate,
                "time": scheduleTime
            }

            tripList.append(tripInfo)
        
        response = {
            "data": tripList
        }
        return json.dumps(response, ensure_ascii=False)
