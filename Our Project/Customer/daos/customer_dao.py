from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref


from db import Base


class CustomerDAO(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    customer_id = Column(String)
    name = Column(String)
    address = Column(String)
    contact_number = Column(String)
    email = Column(String)
    password = Column(String)

    def __init__(self, customer_id, name, address, contact_number, email, password):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.contact_number = contact_number
        self.email = email
        self.password = password

