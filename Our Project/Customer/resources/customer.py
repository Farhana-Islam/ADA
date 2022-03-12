from datetime import datetime

from flask import jsonify

from daos.customer_dao import CustomerDAO
from db import Session


class CustomerProfile:
    @staticmethod
    def create(body):
        session = Session()
        customer = CustomerDAO(body['customer_id'], body['name'], body['address'],
                               body['contact_number'], body['email'], body['password'])
        session.add(customer)
        session.commit()
        session.refresh(customer)
        session.close()
        return jsonify({'delivery_id': customer.id}), 200

    @staticmethod
    def get(c_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        customer = session.query(CustomerDAO).filter(CustomerDAO.id == c_id).first()

        if customer:

            text_out = {
                "customer_id:": customer.customer_id,
                "name": customer.name,
                "address": customer.address,
                "contact_number": customer.contact_number,
                "email": customer.email,
                "password": customer.password
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
            return jsonify({'message': f'There is no customer with id {c_id}'}), 404
        else:
            return jsonify({'message': 'The customer has been removed'}), 200

    @staticmethod
    def update_email(c_id, email):
        session = Session()
        customer = session.query(CustomerDAO).filter(CustomerDAO.id == c_id).first()
        if customer:
            customer.email = email
            session.commit()
            return jsonify({'message': 'Customer email address has been changed'}), 200
        else:
            session.close()
            return jsonify({'message': f'There is no customer with id {c_id}'}), 404

    @staticmethod
    def update_password(c_id, password):
        session = Session()
        customer = session.query(CustomerDAO).filter(CustomerDAO.id == c_id).first()
        if customer:
            customer.password = password
            session.commit()
            return jsonify({'message': 'Customer password address has been changed'}), 200
        else:
            session.close()
            return jsonify({'message': f'There is no customer with id {c_id}'}), 404
