from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL # make sure, to follow upper/lower case, it may cause errors. importing this to connect to our DB
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     
from flask_app import DATABASE
from flask_app.models import user # 3. imporing file user and not class User to avoid to avoid circullar
from flask_app.models import provider # 3. imporing file user and not class User to avoid to avoid circullar
from flask_app.models import billing_party
from flask_app.models import case
from flask_app.models import client


# to connect with show_all

class Case_comment():
    def __init__(self, data):
        self.id = data["id"]
        self.comment = data["comment"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.case_id = data["case_id"]
        self.user_id = data["user_id"]
    
    @classmethod
    def show_related_comments_and_creators(cls, case_id):
        query = "SELECT * FROM case_comments JOIN users ON case_comments.user_id = users.id WHERE case_id = %(case_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, case_id)
        list_of_comments = []
        if result:
            for row in result:
                temp_comment = cls(row)
                user_data = {
                    "id": row["users.id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["users.created_at"],
                    "updated_at": row["users.updated_at"]
                }
                temp_comment.creator = user.User(user_data)
                list_of_comments.append(temp_comment)
        return list_of_comments

    @classmethod 
    def create(cls, data):
        query = "INSERT INTO case_comments (comment, case_id, user_id) VALUES (%(comment)s, %(case_id)s, %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    @classmethod
    def show_related_comments(cls, case_id):
   # def show_related_comments(cls):
        #query = "SELECT * FROM cases JOIN case_comments ON cases.id = case_comments.case_id WHERE cases.id = %(id)s;"
        query = "SELECT * FROM case_comments WHERE case_id = %(case_id)s;"
        result = connectToMySQL(DATABASE).query_db(query, case_id)
        
        print(result)
        return result


    @classmethod
    def show_all(cls):
        query = "SELECT * FROM case_comments;"
        result = connectToMySQL(DATABASE).query_db(query)
         
        return result

    @classmethod # todo validation! 
    def delete(cls, data):
        query = "DELETE from case_comments WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

