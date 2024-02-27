from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     
from flask_app import DATABASE
from flask_app.models import user 

class Billing_party():
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.contact_person = data["contact_person"]
        self.phone1 = data["phone1"]
        self.phone2 = data["phone2"]
        self.phone3 = data["phone3"]
        self.fax = data["fax"]
        self.email = data["email"]
        self.address = data["address"]
        self.city = data["city"]
        self.state = data["state"]
        self.zip = data["zip"]
        self.comments = data["comments"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        self.provider_id = data["provider_id"] 



    @classmethod
    def show_all(cls):
        query = "SELECT * FROM billing_parties;"
        result = connectToMySQL(DATABASE).query_db(query)
        return result

    @classmethod
    def add_biller(cls, data):
        query = "INSERT INTO billing_parties (name, contact_person, phone1, phone2, phone3, fax, email, address, city, state, zip, comments) VALUES (%(name)s, %(contact_person)s, %(phone1)s, %(phone2)s, %(phone3)s, %(fax)s, %(email)s, %(address)s, %(city)s, %(state)s, %(zip)s, %(comments)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def return_biller_id(cls): 
        query = "SELECT id FROM billing_parties WHERE id=(SELECT max(id) FROM billing_parties);"
        result = connectToMySQL(DATABASE).query_db(query)
        return (result[0])

    @classmethod
    def show_billers_join_providers_id(cls): 
        query = "SELECT * FROM providers_and_billing_parties JOIN billing_parties ON providers_and_billing_parties.billing_party_id = billing_parties.id;"
        result = connectToMySQL(DATABASE).query_db(query)
        return result

    @classmethod 
    def show_related_biller(cls, provider_id):
        query = "SELECT * FROM providers_and_billing_parties JOIN billing_parties ON providers_and_billing_parties.billing_party_id = billing_parties.id WHERE provider_id = %(provider_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, provider_id)
        return result

    @staticmethod 
    def biller_input_validation(data): 
        is_valid = True

        if len(data["name"])==0:
            is_valid = False


        if len(data["zip"])==0: 
            is_valid = False   

        return is_valid




















    @classmethod
    def show_one(cls, id):
        query = "SELECT * FROM billing_parties WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, id)
        if results:
            return cls(results[0])
            

    @classmethod
    def update(cls, data):
        query = "UPDATE billing_parties SET name=%(name)s, contact_person=%(contact_person)s, phone1=%(phone1)s, phone2=%(phone2)s, phone3=%(phone3)s, fax=%(fax)s, email=%(email)s, address=%(address)s, city=%(city)s, state=%(state)s, zip=%(zip)s, comments=%(comments)s WHERE id=%(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod 
    def delete_one(cls, data):
        query = "DELETE from billing_parties WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

