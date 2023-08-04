from flask import Flask, request, jsonify
from sqlhandle import *

app = Flask(__name__)

@app.route('/create-user/<user_name>/<first_name>/<last_name>/<department>/<company>/<company_email>')
def create_user(user_name, first_name, last_name, department, company, company_email):
    print("Creating user...")
    print(user_name)
    print(first_name)
    print(last_name)
    print(department)
    print(company)
    print(company_email)
    Create_User(user_name, first_name, last_name, department, company, company_email)
    return jsonify({'success': True})


@app.route('/delete-user/<user_name>')
def delete_user(user_name):
    print("Deleting user...")
    print(user_name)
    Delete_User(user_name)
    return jsonify({'success': True})

@app.route('/create-system/<system_name>/<description>/<company>/<software>')
def create_system(system_name, description, company, software):
    print("Creating system...")
    print(system_name)
    print(description)
    print(company)
    print(software)
    Create_System(system_name, description, company, software)
    return jsonify({'success': True})

@app.route('/delete-system/<system_name>')
def delete_system(system_name):
    print("Deleting system...")
    print(system_name)
    Delete_System(system_name)
    return jsonify({'success': True})

@app.route('/add-system-access/<system_name>/<user_name>/<system_username>')
def add_system_access(system_name, user_name, system_username):
    print("Adding system access...")
    print(system_name)
    print(user_name)
    print(system_username)
    Add_system_access(system_name, user_name, system_username)
    return jsonify({'success': True})

@app.route('/remove-system-access/<system_name>/<user_name>')
def remove_system_access(system_name, user_name):
    print("Removing system access...")
    print(system_name)
    print(user_name)
    Delete_system_access(system_name, user_name)
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
