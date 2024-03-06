from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.user import User 


@app.route("/")
def index():
    if "user_id" in session:    
        return redirect("/main")
    return render_template("index.html")


@app.route("/users/create", methods = ["POST"]) 
def create_user():     
    if User.registry_validation(request.form):  
        session["user_id"] = User.create(request.form) 
    return redirect("/")