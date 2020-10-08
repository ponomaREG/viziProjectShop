from app import db
from app.models.SqlExecuter import SqlExecuter





class Address:

    @staticmethod
    def addNewAddress(district,house,floor,flat,porch,street):
        lastrowid = SqlExecuter.executeModif('insert into Адрес(`district`,`house`,`floor`,`flat`,`porch`,`street`) values("{}","{}","{}","{}","{}","{}");'.format(district,house,floor,flat,porch,street))
        return lastrowid