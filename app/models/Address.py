from app import db





class Address:

    @staticmethod
    def addNewAddress(district,house,floor,flat,porch,street):
        cursor = db.execute('insert into Заказ values("district","house","floor","flat","porch","street") \
        values("{}","{}","{}","{}","{}","{}");'.format(district,house,floor,flat,porch,street))
        lastrowid = cursor.lastrowid
        cursor.close()
        db.commit()
        return lastrowid