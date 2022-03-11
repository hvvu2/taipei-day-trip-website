import os, mysql.connector, mysql.connector.pooling
from dotenv import load_dotenv

load_dotenv

poolName = "mysqlPool"
poolSize = 3
dbconfig ={
    "host":os.getenv("HOST"),
    "port":os.getenv("PORT"),
    "user":os.getenv("USER"),
    "password":os.getenv("PASSWORD"),
    "database":os.getenv("DATABASE")
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = poolName, pool_size = poolSize, **dbconfig)

class DBManager:
    def __init__(self):
        self.cnx = cnxpool.get_connection()
        self.cursor = self.cnx.cursor()

    def insertBasicInfo(self, id, name, category, description, address, transport, mrt, latitude, longitude):
        cmd = """
            INSERT INTO `attractions` (`id`, `name`, `category`, `description`, `address`, `transport`, `mrt`, `latitude`, `longitude`) 
            VALUES (%(id)s, %(name)s, %(category)s, %(description)s, %(address)s, %(transport)s, %(mrt)s, %(latitude)s, %(longitude)s);
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
            "longitude": longitude
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

    def __exit__(self):
        self.cursor.close()
        self.cnx.close()

db = DBManager()
