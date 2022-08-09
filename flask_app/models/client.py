from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     
from flask_app import DATABASE
from flask_app.models import user
from flask_app.models import provider 
from flask_app.models import case


# to connect with show_all

class Client():
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.middle_name = data["middle_name"]
        self.last_name = data["last_name"]
        self.dob = data["dob"]
        self.gender = data["gender"]
        self.phone1 = data["phone1"]
        self.phone2 = data["phone2"]
        self.phone3 = data["phone3"]
        self.fax = data["fax"]
        self.email = data["email"]
        self.address = data["address"]
        self.city = data["city"]
        self.state = data["state"]
        self.zip = data["zip"]
        self.client_since = data["client_since"]
        self.comments = data["comments"]

   