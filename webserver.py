from flask import Flask, request, jsonify, render_template
from sqlhandle import *

app = Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html', headers=getheader('AUDIT_TRAIL'), data=getdata('AUDIT_TRAIL'))

@app.route('/add-user', methods=['GET', 'POST'])
def add_userpage():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        department = request.form.get('department')
        company = request.form.get('company')
        company_email = request.form.get('company_email')
        
        Create_User(user_name, first_name, last_name, department, company, company_email)
        
    return render_template('Add_User.html', headers=getheader('USER_TABLE'), data=getdata('USER_TABLE'))

@app.route('/remove-user', methods=['GET', 'POST'])
def delete_userpage():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        
        Delete_User(user_name)
    return render_template('Remove_User.html', headers=getheader('USER_TABLE'), data=getdata('USER_TABLE'))

@app.route('/add-system', methods=['GET', 'POST'])
def add_systempage():
    if request.method == 'POST':
        system_name = request.form.get('system_name')
        description = request.form.get('Description')
        company = request.form.get('Company')
        software = request.form.get('Software')
        
        Create_System(system_name, description, company, software)
    return render_template('Add_System.html', headers=getheader('SYSTEM_TABLE'), data=getdata('SYSTEM_TABLE'))

@app.route('/remove-system', methods=['GET', 'POST'])
def delete_systempage():
    if request.method == 'POST':
        system_name = request.form.get('System_Name')
        print(system_name)
        Delete_System(system_name)
    return render_template('Remove_System.html', headers=getheader('SYSTEM_TABLE'), data=getdata('SYSTEM_TABLE'))

@app.route('/add-system-access', methods=['GET', 'POST'])
def add_system_accesspage():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        system_name = request.form.get('system_name')
        system_user_name = request.form.get('system_User_Name')
        Add_system_access(system_name, user_name, system_user_name)
    return render_template('Add_System_Access.html', headers=getheader('SYSTEM_ACCESS_TABLE'), data=getdata('SYSTEM_ACCESS_TABLE'))

@app.route('/remove-system-access', methods=['GET', 'POST'])
def remove_system_accesspage():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        system_name = request.form.get('System_Name')

        Delete_system_access(system_name, user_name)
    return render_template('Remove_System_Access.html', headers=getheader('SYSTEM_ACCESS_TABLE'), data=getdata('SYSTEM_ACCESS_TABLE'))



if __name__ == '__main__':
    app.run(debug=True)
