import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
import hashlib
from sqlalchemy_serializer import SerializerMixin


class Division(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "division"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
