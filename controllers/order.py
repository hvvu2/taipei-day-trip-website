from flask import Blueprint, request, session
from datetime import datetime
from models.database import db
from .module import errorHandler, genOrderNumber, partnerKey, merchantId, invalidFormat, namePattern, emailPattern, phonePattern
import json, re, requests

# ===================================================================================== #

order = Blueprint("order_api_bp", __name__)

@order.route("/api/orders", methods=["GET", "POST"])
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
                    orderTime = str(order[1])[2:16]
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
            orderTime = str(datetime.today())[0:19]
            orderNumber = genOrderNumber() + str(memberId)
            orderPrice = orderInfo["order"]["price"]
            schedules = orderInfo["order"]["trip"]
            contactName = orderInfo["order"]["contact"]["name"]
            contactEmail = orderInfo["order"]["contact"]["email"]
            contactPhone = orderInfo["order"]["contact"]["phone"]

            if prime and orderPrice and schedules and re.match(namePattern, contactName) and re.match(emailPattern, contactEmail) and re.match(phonePattern, contactPhone):
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


@order.route("/api/order/<orderNumber>", methods=["GET"])
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
            scheduleDate = trip[4][2:]
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