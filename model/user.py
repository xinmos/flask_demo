from model.base import AutoincrementId, BaseTable
from sqlalchemy import Column, String, SMALLINT


class User(BaseTable, AutoincrementId):
    __tablename__ = "user"

    name = Column(String(10))
    email = Column(String(50), nullable=False, unique=True)
    role = Column(String(10), nullable=False, default="user")
    delete_status = Column(SMALLINT, nullable=False, default=0)
