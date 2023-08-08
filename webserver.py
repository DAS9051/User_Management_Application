from flask import Flask, request, jsonify, render_template, flash, session, redirect
from sqlhandle import *
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('log') == True:
        return render_template('home.html', headers=getheader('AUDIT_TRAIL'), data=getdata('AUDIT_TRAIL'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if correct_password(username, password):
            session['log'] = True
            return render_template('home.html', headers=getheader('AUDIT_TRAIL'), data=getdata('AUDIT_TRAIL'))
        else:
            return render_template('login.html', error="Incorrect Username or Password")

    return render_template('login.html')

@app.route('/home')
def home():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    return render_template('home.html', headers=getheader('AUDIT_TRAIL'), data=getdata('AUDIT_TRAIL'))


@app.route('/logout')
def logout():
    session['log'] = False
    return redirect('/')

@app.route('/add-user', methods=['GET', 'POST'])
def add_userpage():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
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
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        
        Delete_User(user_name)
    return render_template('Remove_User.html', headers=getheader('USER_TABLE'), data=getdata('USER_TABLE'))

@app.route('/add-system', methods=['GET', 'POST'])
def add_systempage():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    if request.method == 'POST':
        system_name = request.form.get('system_name')
        description = request.form.get('Description')
        company = request.form.get('Company')
        software = request.form.get('Software')
        
        Create_System(system_name, description, company, software)
    return render_template('Add_System.html', headers=getheader('SYSTEM_TABLE'), data=getdata('SYSTEM_TABLE'))

@app.route('/remove-system', methods=['GET', 'POST'])
def delete_systempage():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    if request.method == 'POST':
        system_name = request.form.get('System_Name')
        print(system_name)
        Delete_System(system_name)
    return render_template('Remove_System.html', headers=getheader('SYSTEM_TABLE'), data=getdata('SYSTEM_TABLE'))

@app.route('/add-system-access', methods=['GET', 'POST'])
def add_system_accesspage():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        system_name = request.form.get('system_name')
        system_user_name = request.form.get('system_User_Name')
        Add_system_access(system_name, user_name, system_user_name)
    return render_template('Add_System_Access.html', headers=getheader('SYSTEM_ACCESS_TABLE'), data=getdata('SYSTEM_ACCESS_TABLE'))

@app.route('/remove-system-access', methods=['GET', 'POST'])
def remove_system_accesspage():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        system_name = request.form.get('System_Name')

        Delete_system_access(system_name, user_name)
    return render_template('Remove_System_Access.html', headers=getheader('SYSTEM_ACCESS_TABLE'), data=getdata('SYSTEM_ACCESS_TABLE'))



if __name__ == '__main__':
    app.run(debug=True)
