from flask import Flask, request

from db import Base, engine
from resources.customer import CustomerProfile

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/customers', methods=['POST'])
def add_customer():
    req_data = request.get_json()
    return CustomerProfile.create(req_data)


@app.route('/customers/<c_id>', methods=['GET'])
def get_delivery(c_id):
    return CustomerProfile.get(c_id)


@app.route('/customers/<c_id>', methods=['DELETE'])
def delete_delivery(c_id):
    return CustomerProfile.delete(c_id)


@app.route('/customers/<c_id>/email', methods=['PUT'])
def update_customer_email(c_id):
    email = request.args.get('email')
    return CustomerProfile.update_email(c_id, email)
# example    http://localhost:5002/customers/4/email?email=abc@gmail.com


@app.route('/customers/<c_id>/password', methods=['PUT'])
def update_customer_password(c_id):
    password = request.args.get('password')
    return CustomerProfile.update_password(c_id, password)
# example    http://localhost:5002/customers/4/email?password=12348


app.run(host='0.0.0.0', port=5002)
