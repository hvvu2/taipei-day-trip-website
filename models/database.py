import os, mysql.connector, mysql.connector.pooling
from dotenv import load_dotenv

load_dotenv

poolName = "mysqlPool"
poolSize = 6
dbconfig ={
    "host":os.getenv("HOST"),
    "port":os.getenv("PORT"),
    "user":os.getenv("USER"),
    "password":os.getenv("PASSWORD"),
    "database":os.getenv("DATABASE")
}

class DBManager:
    def __init__(self):
        self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = poolName, pool_size = poolSize, **dbconfig, pool_reset_session=True)
        self.cnx = self.cnxpool.get_connection()
        self.cursor = self.cnx.cursor()

    def insertBasicInfo(self, id, name, category, description, address, transport, mrt, latitude, longitude, cover):
        cmd = """
            INSERT INTO `attractions` (`id`, `name`, `category`, `description`, `address`, `transport`, `mrt`, `latitude`, `longitude`, `cover`) 
            VALUES (%(id)s, %(name)s, %(category)s, %(description)s, %(address)s, %(transport)s, %(mrt)s, %(latitude)s, %(longitude)s, %(cover)s);
        """
        param = {
            "id": id,
            "name": name,
            "category": category,
            "description": description,
            "address": address,
            "transport": transport,
            "mrt": mrt,
            "latitude": latitude,
            "longitude": longitude,
            "cover": cover
         }
        self.cursor.execute(cmd, param)

        try:
            self.cnx.commit()

        except:
            self.cnx.rollback()

    def insertImgUrl(self, id, images):
        cmd = "INSERT INTO `images` (`attraction_id`, `url`) VALUES (%(attraction_id)s, %(url)s)"
        param = {
            "attraction_id" : id,
            "url" : images
        }
        self.cursor.execute(cmd, param)

        try:
            self.cnx.commit()

        except:
            self.cnx.rollback()

    def getTotalCount(self):
        cmd = "SELECT COUNT(`id`) FROM `attractions`;"
        self.cursor.execute(cmd)
        result = self.cursor.fetchone()
        return result

    def getRawData(self, currentPage, shownItems):
        cmd = "SELECT * FROM `attractions` LIMIT %(index)s, %(shownItems)s;"
        param = {
            "index": currentPage * shownItems,
            "shownItems": shownItems
        }
        self.cursor.execute(cmd, param)
        result = self.cursor.fetchall()
        return result

    def getKeywordCount(self, keyword):
        cmd = "SELECT COUNT(`name`) FROM `attractions`WHERE `name` LIKE %(keyword)s;"
        param = {"keyword": f"%{keyword}%"}
        self.cursor.execute(cmd, param)
        result = self.cursor.fetchone()
        return result

    def getRawDataByKeyword(self, keyword, currentPage, shownItems):
        cmd = "SELECT * FROM `attractions` WHERE `name` LIKE %(keyword)s LIMIT %(index)s, %(shownItems)s;"
        param = {
            "keyword": f"%{keyword}%",
            "index": currentPage * shownItems,
            "shownItems": shownItems
        }
        self.cursor.execute(cmd, param)
        result = self.cursor.fetchall()
        return result

    def getRawDataById(self, id):
        cmd = "SELECT * FROM `attractions` WHERE `id` = %(id)s;"
        param = {"id": id}
        self.cursor.execute(cmd, param)
        result = self.cursor.fetchone()

        if result:
            return result

        else:
            return False

    def getImages(self, id):
        cmd = "SELECT `url` FROM `images` WHERE `attraction_id` = %(id)s;"
        param = {"id": id}
        self.cursor.execute(cmd, param)
        result = self.cursor.fetchall()
        return result

    def checkEmail(self, email):
        cmd = "SELECT `email` FROM `members` WHERE `email` = %(email)s;"
        param = {"email": email}
        self.cursor.execute(cmd, param)
        result = self.cursor.fetchone()

        if result:
            return False

        else:
            return True

    def insertUser(self, name, email, password):
        cmd = "INSERT INTO `members` (`name`, `email`, `password`) VALUES (%(name)s, %(email)s, %(password)s);"
        param = {
            "name": name,
            "email": email,
            "password": password
        }
        self.cursor.execute(cmd, param)

        try:
            self.cnx.commit()

        except:
            self.cnx.rollback()

    def getUserInfo(self, email):
        cmd = "SELECT `id`, `name`, `email`, `password` FROM `members` WHERE `email` = %(email)s;"
        param = {"email": email}
        self.cursor.execute(cmd, param)
        result = self.cursor.fetchone()

        if result:
            return result

        else:
            return False

    def insertSchedule(self, memberId, name, email, date, time, price, attractionId, attractionName, attractionAddress, attractionCover):
        cmd = """
            INSERT INTO `schedules` (`member_id`, `name`, `email`, `date`, `time`, `price`, `attraction_id`, `attraction_name`, `attraction_address`, `attraction_cover`)
            VALUES (%(memberId)s, %(name)s, %(email)s, %(date)s, %(time)s, %(price)s, %(attractionId)s, %(attractionName)s, %(attractionAddress)s, %(attractionCover)s);
        """
        param = {
            "memberId": memberId,
            "name": name,
            "email": email,
            "date": date,
            "time": time,
            "price": price,
            "attractionId": attractionId,
            "attractionName": attractionName,
            "attractionAddress": attractionAddress,
            "attractionCover": attractionCover
         }
        self.cursor.execute(cmd, param)

        try:
            self.cnx.commit()

        except:
            self.cnx.rollback()

    def getScheduleInfo(self, memberId):
        cmd = "SELECT * FROM `schedules` WHERE `member_id` = %(memberId)s;"
        param = {"memberId": memberId}
        self.cursor.execute(cmd, param)
        result = self.cursor.fetchall()
        if result:
            return result

        else:
            return False

    def deleteSchedule(self, scheduleId, memberId):
        cmd = "DELETE FROM `schedules` WHERE `id` = %(scheduleId)s AND `member_id` = %(memberId)s;"
        param = {
            "scheduleId": scheduleId,
            "memberId": memberId
        }
        self.cursor.execute(cmd, param)

        try:
            self.cnx.commit()

        except:
            self.cnx.rollback()

    def insertOrder(self, orderTime, orderNumber, price, contactName, contactEmail, contactPhone):
        cmd = """
            INSERT INTO `orders` (`order_time`, `order_number`, `price`, `contact_name`, `contact_email`, `contact_phone`)
            VALUES (%(orderTime)s, %(orderNumber)s, %(price)s, %(contactName)s, %(contactEmail)s, %(contactPhone)s);
        """
        param = {
            "orderTime": orderTime,
            "orderNumber": orderNumber,
            "price": price,
            "contactName": contactName,
            "contactEmail": contactEmail,
            "contactPhone": contactPhone
        }
        self.cursor.execute(cmd, param)

        try:
            self.cnx.commit()

        except:
            self.cnx.rollback()

    def insertOrderDetail(self, orderNumber, scheduleId):
        cmd = """
            INSERT INTO `order_details` (`order_number`, `schedule_id`)
            VALUES (%(orderNumber)s, %(scheduleId)s);
        """
        param = {
            "orderNumber": orderNumber,
            "scheduleId": scheduleId
        }
        self.cursor.execute(cmd, param)

        try:
            self.cnx.commit()

        except:
            self.cnx.rollback()


    def updateOrderStatus(self, orderNumber):
        cmd = "UPDATE `orders` SET `status` = '0' WHERE `order_number` = %(orderNumber)s;"
        param = {"orderNumber": orderNumber,}
        self.cursor.execute(cmd, param)

        try:
            self.cnx.commit()

        except:
            self.cnx.rollback()

    def clearAllSchedules(self, memberId):
        cmd = "DELETE FROM `schedules` WHERE `member_id` = %(memberId)s;"
        param = {"memberId": memberId}
        self.cursor.execute(cmd, param)

        try:
            self.cnx.commit()

        except:
            self.cnx.rollback()


    def __exit__(self):
        self.cursor.close()
        self.cnx.close()

db = DBManager()
