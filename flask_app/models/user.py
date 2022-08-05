from flask import flash
import re # here we importing regular expression to validate email
from flask_app.config.mysqlconnection import connectToMySQL # make sure, to follow upper/lower case, it may cause errors. importing this to connect to our DB
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     
from flask_app import DATABASE
# we are creating an object called bcrypt, 
# which is made by invoking the function Bcrypt with our app as an argument


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"] # if you bycript in database it should be VARCHAR(60) !!!
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @classmethod
    def create(cls, data): #don't forget to specify class
        hashed = bcrypt.generate_password_hash(data["password"]) 
        # in order to use this we must import bcrypt and give it an instance(lines 3 and 4), we can give any name instead of "hashed". 
        # now we will assign var hashed to any data we want to bcrypt (see password bellow)
        hashed_values = { 
        # we can give any name instead of "hashed_values", we gonna pass it with our query belllow
        "first_name": data["first_name"],
        "last_name": data["last_name"], 
        # normally, the value that we assigning after : is coming from our input dictionary
        "email": data["email"], 
        "password": hashed 
        # becasuse we want to hash password we just assign to it var hashed from above

    }
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);" # we don't include created_At and updated_At because they have default values
        return connectToMySQL(DATABASE).query_db(query, hashed_values) 
        # we're also passing data with this query. but because we hashed it here, we're passing our hashed_values
        # connectToMySQL- this won't work if you forget to import connecttomysql from mysqlconnection on very top

    @classmethod
    def get_by_email(cls, data): # here we're selecting from the users whose email is equal to what was typed in    
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:     # if there's something coming back from the result, we want to display it
            return cls(result[0]) # because SELECT method always comes back as a list of dictionaries, we want to see only first value from the list

    @classmethod
    def get_by_id(cls, data): # we're creating this method in order to pass user's info and show user's name on dashboard    
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:     # if there's something coming back from the result, we want to display it
            return cls(result[0]) # because SELECT method always comes back as a list of dictionaries, we want to see only first value from the list


    @staticmethod
    def login_validator(data):        # to validate login we first wanna make sure that there's a user registered with this email and password
        user = User.get_by_email(data)
        
        if not user: # 1.cheking email:
            return False
                
        if not bcrypt.check_password_hash(user.password, data["password"]):   # 2.checking bcrypted password:
            return False 

        # 3. if all was true
        return True

    @staticmethod          # we can set different customized validations
    def registry_validation(data):  # adding this ti create user route in our controllers
        is_valid = True   

        if len(data["first_name"]) < 2:
            flash("First name must have at least 2 characters!")
            is_valid = False

        if len(data["last_name"]) < 2:
            flash("Last name must have at least 2 characters!")
            is_valid = False

        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters!") # don't forget to import flash
            is_valid = False

        # is the email already exist in our database? 
        user = User.get_by_email(data)
        if user:
            flash("Email is already registered!") 
            is_valid = False   

        #regular expression to validate email (looking for special det of characters that emails have)
        # don't forget to import it first
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(data["email"]): 
            flash("Invalid email address!")
            is_valid = False

        if data["password"] != data["confirm_password"]:
            flash("Password doesn't match!")
            is_valid = False

        return is_valid    
    