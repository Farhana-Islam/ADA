from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import EmailType, PasswordType, force_auto_coercion
import flask
import passlib
from passlib.context import LazyCryptContext
from db import Base

force_auto_coercion()


class CustomerDAO(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    name = Column(String(100), nullable=False, unique=False)
    address = Column(String(200), nullable=True)
    contact_number = Column(String, nullable=True)
    status = Column(String)
    email = Column(EmailType, unique=True, nullable=False)
    password = Column(PasswordType(schemes=['pbkdf2_sha512','md5_crypt'], deprecated=['md5_crypt']),
                unique=False, nullable=False)


    def __init__(self,  name, address, contact_number, email, password, status):
        self.name = name
        self.address = address
        self.contact_number = contact_number
        self.email = email
        self.password = password
        self.status = status

