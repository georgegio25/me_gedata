from flask import Flask, render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.provider import Provider 
from flask_app.models.billing_party import Billing_party 
from flask_app.models.case import Case 
from flask_app.models.user import User 
from flask_app.models.case_comment import Case_comment 
from flask_app.models.client import Client 
from flask_app.models.case_comment import Case_comment 

# ---------------------- DISPLAY ROUTES ---------------------

@app.route("/main")
def main():
    all_providers = Provider.show_all()
    all_billers = Billing_party.show_billers_join_providers_id() 
    all_cases = Case.show_cases_join_providers_id()

    logged_in_user = User.get_by_id({"id": session["user_id"]}) 
    return render_template("main.html", all_cases=all_cases, all_billers=all_billers, all_providers=all_providers, user=logged_in_user)
