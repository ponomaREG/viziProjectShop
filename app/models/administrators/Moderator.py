from app import db
from utils import tagsHelper


class Moderator:
    name = None

    def __init__(self,name):
        self.name = name

    

    @staticmethod
    def addProduct(title,desc,cost_purchase,cost_sale,quantity,tags=[]):
        cursor = db.execute('insert into Товар values("{}","{}",{},{},{},"{}");'
        .format(title,desc,cost_purchase,cost_sale,quantity,tagsHelper.makeArrayOfTagsToStr(tags)))
        db.commit()
        lastrowid= cursor.lastrowid
        return lastrowid