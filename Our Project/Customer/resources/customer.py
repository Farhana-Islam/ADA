from datetime import datetime
from constant import STATUS
from flask import jsonify

from daos.customer_dao import CustomerDAO
from db import Session


class CustomerProfile:
    @staticmethod
    def create(body):
        session = Session()
        customer = CustomerDAO(body['name'], body['address'],
                               body['contact_number'], body['email'], body['password'], STATUS)

        valid_email = session.query(CustomerDAO).filter(CustomerDAO.email == customer.email).first()

        if valid_email:
            session.close()
            return jsonify({'message': f'Email already in use, please use different email address'}), 404
        else:
            session.add(customer)
            session.commit()
            session.refresh(customer)
            session.close()
            return jsonify({'customer_account_id': customer.id}), 200

    @staticmethod
    def get(c_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        customer = session.query(CustomerDAO).filter(CustomerDAO.id == c_id).first()

        if customer:

            text_out = {
                "name": customer.name,
                "address": customer.address,
                "contact_number": customer.contact_number,
                "email": customer.email,
                #"password": customer.password,
                "status": customer.status
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no customer with id {c_id}'}), 404

    @staticmethod
    def delete(c_id):
        session = Session()
        effected_rows = session.query(CustomerDAO).filter(CustomerDAO.id == c_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'No Customer exits with ID {c_id}'}), 404
        else:
            return jsonify({'message': 'The Customer has been removed'}), 200



    @staticmethod
    def customer_login(email, password):
        session = Session()
        customer = session.query(CustomerDAO).filter(CustomerDAO.email == email).first()
        if customer:

            if customer.password == password:
                customer.status = 'logged in'
                session.commit()
                return jsonify({'message': f'Successfully logged in.Your ID is {customer.id}.You can update or delete '
                                           f'your profile based on this ID'}), 200
            else:
                session.close()
                return jsonify({'message': f'Incorrect password'}), 404

        else:
            session.close()
            return jsonify({'message': f'Invalid Email'}), 404

    @staticmethod
    def update_customer(id, email=None, password=None, address= None, contact_number= None, name= None):
        session = Session()
        customer = session.query(CustomerDAO).filter(CustomerDAO.id == id).first()
        if customer.status != "logged in":
            session.close()
            return jsonify({'message': f'Please Log In'}), 404
        else:
            if email is not None:
                customer.email = email
            elif password is not None:
                customer.password = password
            elif name is not None:
                customer.name = name
            elif address is not None:
                customer.address = address
            elif contact_number is not None:
                customer.contact_number = contact_number
            session.commit()
            session.close()
            return jsonify({'message': f'Your Profile Updated Successfully Updated'}), 200

