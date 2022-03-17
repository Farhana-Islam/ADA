from flask import Flask, request
from flask_migrate import Migrate
from db import Base, engine
from resources.customer import CustomerProfile
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)
ab= SQLAlchemy(app)
migrate = Migrate(app, ab)

@app.route('/customers', methods=['POST'])
def add_customer():
    req_data = request.get_json()
    return CustomerProfile.create(req_data)


@app.route('/customers/<c_id>', methods=['GET'])
def get_delivery(c_id):
    return CustomerProfile.get(c_id)


@app.route('/customers/<c_id>', methods=['DELETE'])
def delete_customer(c_id):
    return CustomerProfile.delete(c_id)


@app.route('/customers/login', methods=['PUT'])
def customer_login():
    email = request.args.get('email')
    password = request.args.get('password')
    return CustomerProfile.customer_login(email, password)
# example    http://localhost:5002/customers/login?email=abc@gmail.com&password=123


@app.route('/customers/<id>/update', methods=['PUT'])
def update_customer(id, email=None, password=None, address= None, contact_number= None, name= None):
    req_data = request.get_json()
    if req_data.get('email'):
        email = req_data.get('email')
    elif req_data.get('password'):
        password = req_data.get('password')
    elif req_data.get('address'):
        address = req_data.get('address')
    elif req_data.get('contact_number'):
        contact_number = req_data.get('contact_number')
    elif req_data.get('name'):
        name = req_data.get('name')
    return CustomerProfile.update_customer(id, email, password, address, contact_number, name)
# example    http://localhost:5002/customers/4/





app.run(host='0.0.0.0', port=5002)
