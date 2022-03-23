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
                               body['contact_number'], body['email'], body['password'], STATUS, body['bank_account_number'],)

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
        customer = session.query(CustomerDAO).filter(CustomerDAO.id == c_id).first()

        if customer:

            text_out = {
                "name": customer.name,
                "address": customer.address,
                "contact_number": customer.contact_number,
                "email": customer.email,
                "bank_account_number": customer.bank_account_number,
                "status": customer.status
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no customer with id {c_id}'}), 404


    @staticmethod
    def get_all_customer():
        session = Session()
        customers = session.query(CustomerDAO).all()
        text_out = {}
        if customers:
            for customer in customers:
                text_out['Customer_id: '+str(customer.id)] = {
                                    "name": customer.name,
                                    "address": customer.address,
                                    "contact_number": customer.contact_number,
                                    "email": customer.email,
                                    "bank_account_number": customer.bank_account_number,
                                    "status": customer.status
                                        }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no customer in database'}), 404



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
                return jsonify({'message': f'Successfully logged in.Your ID is {customer.id}.You can update '
                                           f'or delete your profile based on this ID'}), 200
            else:
                session.close()
                return jsonify({'message': f'Incorrect password'}), 404

        else:
            session.close()
            return jsonify({'message': f'No account exits. Please try again'}), 404


    @staticmethod
    def customer_logout(c_id):
        session = Session()
        customer = session.query(CustomerDAO).filter(CustomerDAO.id == c_id).first()
        if customer:
            if customer.status != 'logged in':
                session.close()
                return jsonify({'message': f'Please Login First'}), 404
            else:
                customer.status = 'logout'
                session.commit()
                session.close()
                return jsonify({'message': f'Successfully Logged Out'}), 200
        else:
            session.close()
            return jsonify({'message': f'There is no customer with id {c_id}'}), 404


    @staticmethod
    def update_customer(id,name=None,address=None,contact_number=None,email=None,password=None,bank_account_number=None):
        session = Session()
        customer = session.query(CustomerDAO).filter(CustomerDAO.id == id).first()
        if customer:
            if customer.status != "logged in":
                session.close()
                return jsonify({'message': f'Please Log In'}), 404
            else:
                if name is not None:
                    customer.name = name
                if address is not None:
                    customer.address = address
                if contact_number is not None:
                    customer.contact_number = contact_number
                if email is not None:
                    email_in_use = session.query(CustomerDAO).filter(CustomerDAO.email == email).first()

                    if email_in_use:
                        session.close()
                        return jsonify({'message': f'Email already in use, please use different email address'}), 404
                    else:
                        customer.email = email
                if password is not None:
                    customer.password = password
                if bank_account_number is not None:
                    customer.bank_account_number = bank_account_number
                session.commit()
                session.close()
                return jsonify({'message': f'Your Profile Updated Successfully Updated'}), 200
        else:
            session.close()
            return jsonify({'message': f'There is no customer with id {id}'}), 404
