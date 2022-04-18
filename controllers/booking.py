from flask import Blueprint, request, session
from models.database import db
from .module import errorHandler, validateDate, invalidFormat, emptyInput
import json

# ===================================================================================== #

booking = Blueprint("booking_api_bp", __name__)

@booking.route("/api/booking", methods=["GET", "POST", "DELETE"])
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