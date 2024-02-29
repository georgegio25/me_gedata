from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL 
# make sure, to follow upper/lower case, it may cause errors. importing this to connect to our DB
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     
from flask_app import DATABASE
from flask_app.models import user 
from flask_app.models import billing_party
from flask_app.models import case

class Provider():
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.practice = data["practice"]
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


    @classmethod
    def show_all(cls):
        query = "SELECT * FROM providers;"
        result = connectToMySQL(DATABASE).query_db(query)
        return result


    @classmethod
    def show_all_with_billers(cls):
        query = "SELECT * FROM providers LEFT JOIN providers_and_billing_parties ON providers.id = providers_and_billing_parties.provider_id LEFT JOIN billing_parties ON billing_parties.id = providers_and_billing_parties.billing_party_id LEFT JOIN cases_and_providers ON providers.id = cases_and_providers.provider_id LEFT JOIN cases ON cases.id = cases_and_providers.case_id;"
        result = connectToMySQL(DATABASE).query_db(query)
        list_of_providers = []
        if result:
            for row in result: 
                temp_provider = cls(row)
                biller_data = { 
                    "id": row["billing_parties.id"], 
                    "name": row["billing_parties.name"],
                    "contact_person": row["contact_person"],
                    "phone1": row["billing_parties.phone1"],
                    "phone2": row["billing_parties.phone2"],
                    "phone3": row["billing_parties.phone3"],
                    "fax": row["billing_parties.fax"],
                    "email": row["billing_parties.email"],
                    "address": row["billing_parties.address"],
                    "city": row["billing_parties.city"],
                    "state": row["billing_parties.state"],
                    "zip": row["billing_parties.zip"],
                    "comments": row["billing_parties.comments"],
                    "created_at": row["billing_parties.created_at"],
                    "updated_at": row["billing_parties.updated_at"],
                    "provider_id": row["billing_parties.provider_id"]
                }
                temp_provider.biller = billing_party.Billing_party(biller_data) 
                list_of_providers.append(temp_provider)
        
        return list_of_providers

    @classmethod
    def show_all_with_billers_and_cases(cls):
        query = "SELECT * FROM providers LEFT JOIN providers_and_billing_parties ON providers.id = providers_and_billing_parties.provider_id LEFT JOIN billing_parties ON billing_parties.id = providers_and_billing_parties.billing_party_id LEFT JOIN cases_and_providers ON providers.id = cases_and_providers.provider_id LEFT JOIN cases ON cases.id = cases_and_providers.case_id;"
        result = connectToMySQL(DATABASE).query_db(query)
        list_of_providers = []
        if result:
            for row in result: 
                temp_provider = cls(row)
                biller_data = { 
                    "id": row["billing_parties.id"], 
                    "name": row["billing_parties.name"],
                    "contact_person": row["contact_person"],
                    "phone1": row["billing_parties.phone1"],
                    "phone2": row["billing_parties.phone2"],
                    "phone3": row["billing_parties.phone3"],
                    "fax": row["billing_parties.fax"],
                    "email": row["billing_parties.email"],
                    "address": row["billing_parties.address"],
                    "city": row["billing_parties.city"],
                    "state": row["billing_parties.state"],
                    "zip": row["billing_parties.zip"],
                    "comments": row["billing_parties.comments"],
                    "created_at": row["billing_parties.created_at"],
                    "updated_at": row["billing_parties.updated_at"],
                    "provider_id": row["provider_id"]
                }
                case_data = { 
                    "id": row["cases.id"], 
                    "title": row["title"],
                    "description": row["description"],
                    "created_at": row["cases.created_at"],
                    "updated_at": row["cases.updated_at"],
                    "user_id": row["user_id"],
                    "provider_id": row["provider_id"]
                }
                temp_provider.biller = billing_party.Billing_party(biller_data) 
                temp_provider.case = case.Case(case_data) 
                list_of_providers.append(temp_provider)
            return list_of_providers

        
    @classmethod
    def add_one(cls, data):
        query = "INSERT INTO providers (name, practice, phone1, phone2, phone3, fax, email, address, city, state, zip, comments) VALUES (%(name)s, %(practice)s, %(phone1)s, %(phone2)s, %(phone3)s, %(fax)s, %(email)s, %(address)s, %(city)s, %(state)s, %(zip)s, %(comments)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def show_one(cls, id):
        query = "SELECT * FROM providers WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, id)
        if results:
            return cls(results[0])

    @classmethod
    def show_providers_related_to_case(cls, case_id):
        query = "SELECT * FROM cases_and_providers JOIN providers ON cases_and_providers.provider_id = providers.id WHERE cases_and_providers.case_id = %(case_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, case_id)
        return result

    @classmethod
    def add_provider(cls, data):
        query = "INSERT INTO providers (`name`, `practice`, `phone1`, `phone2`, `phone3`, `fax`, `email`, `address`, `city`, `state`, `zip`, `comments`) VALUES (%(name)s, %(practice)s, %(phone1)s, %(phone2)s, %(phone3)s, %(fax)s, %(email)s, %(address)s, %(city)s, %(state)s, %(zip)s, %(comments)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def return_provider_id(cls): 
        query = "SELECT id FROM providers WHERE id=(SELECT max(id) FROM providers);"
        result = connectToMySQL(DATABASE).query_db(query)
        return (result[0])

    @classmethod
    def link_with_biller(cls, data):
        query = "INSERT INTO `me_gedata`.`providers_and_billing_parties` (`provider_id`, `billing_party_id`) VALUES (%(provider_id)s, %(billing_party_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def update(cls, data):
        query = "UPDATE providers SET name=%(name)s, practice=%(practice)s, phone1=%(phone1)s, phone2=%(phone2)s, phone3=%(phone3)s, fax=%(fax)s, email=%(email)s, address=%(address)s, city=%(city)s, state=%(state)s, zip=%(zip)s, comments=%(comments)s WHERE id=%(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod 
    def delete_one(cls, data):
        query = "DELETE from providers WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod 
    def provider_input_valdation(data): 
        is_valid = True

        if len(data["name"])==0:
            is_valid = False


        if len(data["zip"])==0: 
            is_valid = False   

        return is_valid