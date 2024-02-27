
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     
from flask_app import DATABASE
from flask_app.models import user 
from flask_app.models import provider 
from flask_app.models import billing_party
from flask_app.models import client


class Case():
    def __init__(self, data):
        self.id = data["id"]
        self.title = data["title"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data ["user_id"]


    @classmethod 
    def show_one_with_provider(cls, id):
        query = "SELECT * FROM cases LEFT JOIN cases_and_clients ON cases.id = cases_and_clients.case_id LEFT JOIN clients ON cases_and_clients.client_id = clients.id LEFT JOIN cases_and_providers ON cases.id = cases_and_providers.case_id LEFT JOIN providers ON providers.id = cases_and_providers.provider_id LEFT JOIN case_comments ON cases.id = case_comments.case_id LEFT JOIN users ON users.id = case_comments.user_id WHERE cases.id = %(id)s;"
        
        
        result = connectToMySQL(DATABASE).query_db(query, id)
        list_of_cases = []
        if result:
            for row in result: 
                temp_case = cls(row)
                provider_data = { 
                    "id": row["providers.id"], 
                    "name": row["name"],
                    "practice": row["practice"],
                    "phone1": row["phone1"],
                    "phone2": row["phone2"],
                    "phone3": row["phone3"],
                    "fax": row["fax"],
                    "email": row["email"],
                    "address": row["address"],
                    "city": row["city"],
                    "state": row["state"],
                    "zip": row["zip"],
                    "comments": row["comments"],
                }
                client_data = { 
                    "id": row["clients.id"], 
                    "first_name": row["first_name"],
                    "middle_name": row["middle_name"],
                    "last_name": row["last_name"],
                    "dob": row["dob"],
                    "gender": row["gender"],
                    "phone1": row["phone1"],
                    "phone2": row["phone2"],
                    "phone3": row["phone3"],
                    "fax": row["fax"],
                    "email": row["email"],
                    "address": row["address"],
                    "city": row["city"],
                    "state": row["state"],
                    "zip": row["zip"],
                    "client_since": row["client_since"],
                    "comments": row["comments"],
                }
                temp_case.provider = provider.Provider(provider_data) 
                temp_case.client = client.Client(client_data) 

                list_of_cases.append(temp_case)
        
        return list_of_cases[0]

    @classmethod
    def show_one(cls, id):
        query = "SELECT * FROM cases WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, id)
        if result:
            return cls(result[0])

    @classmethod
    def create(cls, data):
        query = "INSERT INTO cases (title, description, user_id) VALUES (%(title)s, %(description)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def return_case_id(cls): 
        query = "SELECT id FROM cases WHERE id=(SELECT max(id) FROM cases);"
        result = connectToMySQL(DATABASE).query_db(query)
        return (result[0]) 

    @classmethod
    def link_with_client(cls, data):
        query = "INSERT INTO cases_and_clients (case_id, client_id) VALUES (%(case_id)s, %(client_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def link_with_provider(cls, data):
        query = "INSERT INTO cases_and_providers (case_id, provider_id) VALUES (%(case_id)s, %(provider_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def show_cases_join_providers_id(cls): 
        query = "SELECT * FROM cases LEFT JOIN cases_and_providers ON cases_and_providers.case_id = cases.id;"
        result = connectToMySQL(DATABASE).query_db(query)
        return result





    @staticmethod 
    def case_input_validation(data): 
        is_valid = True

        if len(data["title"])==0:
            is_valid = False

        if len(data["description"])==0:
            is_valid = False

        return is_valid


