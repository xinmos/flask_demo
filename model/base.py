from datetime import datetime

from sqlalchemy import Column, TIMESTAMP, text, Integer

from uitls.database import db


class BaseTable(db.Model):
    __abstract__ = True

    def to_dict(self):
        dic = {}
        for c in self.__table__.columns:
            if isinstance(getattr(self, c.name), datetime):
                dic[c.name] = getattr(self, c.name).strftime("%Y-%m-%d %H:%M:%S")
            dic[c.name] = getattr(self, c.name)
        return dic


class AutoincrementId(object):
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)


class HasTime(object):
    create_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
