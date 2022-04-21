import os, mysql.connector, mysql.connector.pooling
from dotenv import load_dotenv

load_dotenv

poolName = "mysqlPool"
poolSize = 10
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

    def __enter__(self):
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
        with self:
            cmd = "SELECT COUNT(`id`) FROM `attractions`;"
            self.cursor.execute(cmd)
            result = self.cursor.fetchone()
            return result

    def getRawData(self, currentPage, shownItems):
        with self:
            cmd = "SELECT * FROM `attractions` LIMIT %(index)s, %(shownItems)s;"
            param = {
                "index": currentPage * shownItems,
                "shownItems": shownItems
            }
            self.cursor.execute(cmd, param)
            result = self.cursor.fetchall()
            return result

    def getKeywordCount(self, keyword):
        with self:
            cmd = "SELECT COUNT(`name`) FROM `attractions`WHERE `name` LIKE %(keyword)s;"
            param = {"keyword": f"%{keyword}%"}
            self.cursor.execute(cmd, param)
            result = self.cursor.fetchone()
            return result

    def getRawDataByKeyword(self, keyword, currentPage, shownItems):
        with self:
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
        with self:
            cmd = "SELECT * FROM `attractions` WHERE `id` = %(id)s;"
            param = {"id": id}
            self.cursor.execute(cmd, param)
            result = self.cursor.fetchone()

            if result:
                return result

            else:
                return False

    def getImages(self, attractionId):
        with self:
            cmd = "SELECT `url` FROM `images` WHERE `attraction_id` = %(attractionId)s;"
            param = {"attractionId": attractionId}
            self.cursor.execute(cmd, param)
            result = self.cursor.fetchall()
            return result

    def checkEmail(self, email):
        with self:
            cmd = "SELECT `email` FROM `members` WHERE `email` = %(email)s;"
            param = {"email": email}
            self.cursor.execute(cmd, param)
            result = self.cursor.fetchone()

            if result:
                return False

            else:
                return True

    def insertUser(self, name, email, password):
        with self:
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
        with self:
            cmd = "SELECT `id`, `name`, `email`, `password` FROM `members` WHERE `email` = %(email)s;"
            param = {"email": email}
            self.cursor.execute(cmd, param)
            result = self.cursor.fetchone()

            if result:
                return result

            else:
                return False

    def checkUserName(self, id, newName):
        with self:
            cmd = "SELECT * FROM `members` WHERE `id` = %(id)s AND `name` = %(newName)s;"
            param = {
                "id": id,
                "newName": newName
            }
            self.cursor.execute(cmd, param)
            result = self.cursor.fetchone()

            if result:
                return False

            else:
                return True

    def changeUserName(self, id, newName):
        with self:
            cmd = "UPDATE `members` SET `name` = %(newName)s WHERE `id` = %(id)s;"
            param = {
                "id": id,
                "newName": newName
            }
            self.cursor.execute(cmd, param)

            try:
                self.cnx.commit()

            except:
                self.cnx.rollback()

    def insertSchedule(self, memberId, date, time, price, attractionId, attractionName, attractionAddress, attractionCover):
        with self:
            cmd = """
                INSERT INTO `schedules` (`member_id`, `date`, `time`, `price`, `attraction_id`, `attraction_name`, `attraction_address`, `attraction_cover`)
                VALUES (%(memberId)s, %(date)s, %(time)s, %(price)s, %(attractionId)s, %(attractionName)s, %(attractionAddress)s, %(attractionCover)s);
            """
            param = {
                "memberId": memberId,
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
        with self:
            cmd = "SELECT * FROM `schedules` WHERE `member_id` = %(memberId)s;"
            param = {"memberId": memberId}
            self.cursor.execute(cmd, param)
            result = self.cursor.fetchall()

            if result:
                return result

            else:
                return False

    def deleteSchedule(self, scheduleId, memberId):
        with self:
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

    def insertOrder(self, memberId, time, number, price, contactName, contactEmail, contactPhone):
        with self:
            cmd = """
                INSERT INTO `orders` (`member_id`, `time`, `number`, `price`, `contact_name`, `contact_email`, `contact_phone`)
                VALUES (%(memberId)s, %(time)s, %(number)s, %(price)s, %(contactName)s, %(contactEmail)s, %(contactPhone)s);
            """
            param = {
                "memberId": memberId,
                "time": time,
                "number": number,
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

    def insertOrderDetail(self, orderNumber, scheduleDate, scheduleTime, attractionId, attractionName, attractionAddress, attractionCover):
        with self:
            cmd = """
                INSERT INTO `order_details` (`order_number`, `schedule_date`, `schedule_time`, `attraction_id`, `attraction_name`, `attraction_address`, `attraction_cover`)
                VALUES (%(orderNumber)s, %(scheduleDate)s, %(scheduleTime)s, %(attractionId)s, %(attractionName)s, %(attractionAddress)s, %(attractionCover)s);
            """
            param = {
                "orderNumber": orderNumber,
                "scheduleDate": scheduleDate,
                "scheduleTime": scheduleTime,
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

    def updateOrderStatus(self, orderNumber):
        with self:
            cmd = "UPDATE `orders` SET `status` = '0' WHERE `number` = %(orderNumber)s;"
            param = {"orderNumber": orderNumber}
            self.cursor.execute(cmd, param)

            try:
                self.cnx.commit()

            except:
                self.cnx.rollback()
    
    def updatePaymentStatus(self, orderNumber):
        with self:
            cmd = "UPDATE `orders` SET `payment_status` = '0' WHERE `number` = %(orderNumber)s;"
            param = {"orderNumber": orderNumber}
            self.cursor.execute(cmd, param)

            try:
                self.cnx.commit()

            except:
                self.cnx.rollback()

    def clearAllSchedules(self, memberId):
        with self:
            cmd = "DELETE FROM `schedules` WHERE `member_id` = %(memberId)s;"
            param = {"memberId": memberId}
            self.cursor.execute(cmd, param)

            try:
                self.cnx.commit()

            except:
                self.cnx.rollback()

    def getOrders(self, memberId):
        with self:
            cmd = """
                SELECT `number`, `time`, `price`, `contact_name`, `contact_email`, `contact_phone`
                FROM `orders` WHERE `member_id` = %(memberId)s AND `status` = 0 AND `payment_status` = 0;
            """
            param = {"memberId": memberId}
            self.cursor.execute(cmd, param)
            result = self.cursor.fetchall()

            if result:
                return result

            else:
                return False

    def getOrderDetails(self, orderNumber):
        with self:
            cmd = """
                SELECT `attraction_id`, `attraction_name`, `attraction_address`, `attraction_cover`, `schedule_date`, `schedule_time`
                FROM `order_details` WHERE `order_number` = %(orderNumber)s;
            """
            param = {"orderNumber": orderNumber}
            self.cursor.execute(cmd, param)
            result = self.cursor.fetchall()
            return result

    def __exit__(self, exc_type, exc_value, tb):
        self.cursor.close()
        self.cnx.close()

db = DBManager()
