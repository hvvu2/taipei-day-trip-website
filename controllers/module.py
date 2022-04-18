from flask import Response
from datetime import datetime
import json, random, os

invalidId = "The attraction does not exist or the input is invalid."
emptyInput = "All inputs are required."
invalidFormat = "The format is invalid."
emailRegistered = "The email has already been registered."
sameUserName = "The name must be different from you're using now."
incorrectSignIn = "The email or the password is incorrect."
salt = os.getenv("SALT")
partnerKey = os.getenv("PARTNER_KEY")
merchantId = os.getenv("MERCHANT_ID")
namePattern = r"(^.{2,32}$)"
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
