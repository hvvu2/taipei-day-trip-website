from database import db
import json

with open("data/taipei-attractions.json", encoding="utf-8") as file:
    attractions = json.load(file)["result"]["results"]

id = 0

for attraction in attractions:
    
    id += 1
    name = attraction["stitle"]
    category = attraction["CAT2"]
    description = attraction["xbody"]
    address = attraction["address"]
    transport = attraction["info"]
    mrt = attraction["MRT"]
    latitude = attraction["latitude"]
    longitude = attraction["longitude"]
    imagesList = attraction["file"].lower().split("https://")
    cover = "https://" + imagesList[1]
    
    db.insertBasicInfo(id, name, category, description, address, transport, mrt, latitude, longitude, cover)

    for images in imagesList:
        if images.endswith(".jpg"):
            images = "https://" + images
            db.insertImgUrl(id, images)
