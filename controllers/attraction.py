from flask import Blueprint, request
from models.database import db
from .module import errorHandler, invalidId
import json

# ===================================================================================== #

attraction = Blueprint("attraction_api_bp", __name__)

@attraction.route("/api/attractions", methods=["GET"])
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
                "images": item[9]
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


@attraction.route("/api/attraction/<attractionId>", methods=["GET"])
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