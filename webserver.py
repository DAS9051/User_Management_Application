from flask import Flask, request, jsonify, render_template, flash, session, redirect, send_file
from sqlhandle import *
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if session.get('log') == True:
        header = getheader('AUDIT_TRAIL')
        header[0] = 'ID'
        header[1] = 'Username'
        header[2] = 'Name'
        header[3] = 'Changed On'
        header[4] = 'Type of Change'
        header[5] = 'System Name'

        return render_template('home.html', headers=header, data=getdata('AUDIT_TRAIL'), users=dropDown('USER_TABLE', 'User_Name'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if correct_password(username, password):
            session['log'] = True
            session['username'] = username
            auditlog(username, 'Logged In')
            header = getheader('AUDIT_TRAIL')
            header[0] = 'ID'
            header[1] = 'Username'
            header[2] = 'Name'
            header[3] = 'Changed On'
            header[4] = 'Type of Change'
            header[5] = 'System Name'
            return render_template('home.html', headers=header, data=getdata('AUDIT_TRAIL'), users=dropDown('USER_TABLE', 'User_Name'))
        else:
            flash('Incorrect Username or Password', 'danger')
            auditlog(username, 'Failed Log In')
            return render_template('login.html', error="Incorrect Username or Password")

    return render_template('login.html')

@app.route('/home')
def home():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    header = getheader('AUDIT_TRAIL')
    header[0] = 'ID'
    header[1] = 'Username'
    header[2] = 'Name'
    header[3] = 'Changed On'
    header[4] = 'Type of Change'
    header[5] = 'System Name'
    return render_template('home.html', headers=header, data=getdata('AUDIT_TRAIL'), users=dropDown('USER_TABLE', 'User_Name'))


@app.route('/logout')
def logout():
    session['log'] = False
    auditlog(session['username'], 'Logged Out')
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
        if Create_User(user_name, first_name, last_name, department, company, company_email, session['username']):
            flash(('Successfully Added User', 'success'))
        else:
            flash(('Failed to Add User', 'danger'))


    head = getheader('USER_TABLE')
    head[0] = 'User Name'
    head[1] = 'First Name'
    head[2] = 'Last Name'
    head[3] = 'Department'
    head[4] = 'Company'
    head[5] = 'Company Email'
    head[6] = 'Created On'
    head[7] = 'Changed On' 
    head[8] = 'Removed'
    
    return render_template('Add_User.html', headers=head, data=getdata('USER_TABLE'))

@app.route('/remove-user', methods=['GET', 'POST'])
def delete_userpage():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        print(user_name)

        if ('submit_button' in request.form):
            if (Delete_User(user_name, session['username'])):
                flash(('Successfully Deleted User', 'success'))
            else:
                flash(('Failed to Delete User', 'danger'))
        
        else:
            if (Restore_User(user_name, session['username'])):
                flash(('Successfully Restored User', 'success'))
            else:
                flash(('Failed to Restore User', 'danger'))


    head = getheader('USER_TABLE')
    head[0] = 'User Name'
    head[1] = 'First Name'
    head[2] = 'Last Name'
    head[3] = 'Department'
    head[4] = 'Company'
    head[5] = 'Company Email'
    head[6] = 'Created On'
    head[7] = 'Changed On' 
    head[8] = 'Removed'
    return render_template('Remove_User.html', headers=head, data=getdata('USER_TABLE'), usernames=dropDown('USER_TABLE', 'User_Name'))

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
        
        if Create_System(system_name, description, company, software, session['username']):
            flash(('Successfully Added System', 'success'))
        else:
            flash(('Failed to Add System', 'danger'))

    head = getheader('SYSTEM_TABLE')
    head[0] = 'System Name'
    head[1] = 'Description'
    head[2] = 'Company'
    head[3] = 'Software'
    head[4] = 'Created On'
    head[5] = 'Changed On'
    head[6] = 'Removed'
    return render_template('Add_System.html', headers=head, data=getdata('SYSTEM_TABLE'))

@app.route('/remove-system', methods=['GET', 'POST'])
def delete_systempage():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    if request.method == 'POST':
        system_name = request.form.get('System_Name')
        if ('submit_button' in request.form):
            print("Delete")
            if (Delete_System(system_name, session['username'])):
                flash(('Successfully Deleted System', 'success'))
            else:
                flash(('Failed to Delete System', 'danger'))
            # Delete_System(system_name, session['username'])
        else:
            print("Restore")
            if (Restore_System(system_name, session['username'])):
                flash(('Successfully Restored System', 'success'))
            else:
                flash(('Failed to Restore System', 'danger'))
            Restore_System(system_name, session['username'])

    head = getheader('SYSTEM_TABLE')
    head[0] = 'System Name'
    head[1] = 'Description'
    head[2] = 'Company'
    head[3] = 'Software'
    head[4] = 'Created On'
    head[5] = 'Changed On'
    head[6] = 'Removed'
    return render_template('Remove_System.html', headers=head, data=getdata('SYSTEM_TABLE'), systems=dropDown('SYSTEM_TABLE', 'System_Name'))

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
        role = request.form.get('role')
        if (Add_system_access(system_name, user_name, system_user_name, session['username'],role)):
            flash(('Successfully Added System Access', 'success'))
        else:
            flash(('Failed to Add System Access', 'danger'))
    
    head = getheader('SYSTEM_ACCESS_TABLE')
    head[0] = 'Access ID'
    head[1] = 'User Name'
    head[2] = 'System Name'
    head[3] = 'System User Name'
    head[4] = 'Role'
    head[5] = 'Created On'
    head[6] = 'Changed On'
    head[7] = 'Removed'
    return render_template('Add_System_Access.html', headers=head, data=getdata('SYSTEM_ACCESS_TABLE'), systems=sdropDown('SYSTEM_TABLE', 'SYSTEM_NAME'),users=sdropDown('USER_TABLE', 'USER_NAME'))   

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
        system_username = request.form.get('System_User_Name')
        if ('submit_button' in request.form):
        
            if (Delete_system_access(system_name, user_name, session['username'], system_username)):
                flash(('Successfully Deleted System Access', 'success'))
            else:
                flash(('Failed to Delete System Access', 'danger'))
            # Delete_system_access(system_name, user_name, session['username'], system_username)
        else:
            if (Restore_system_access(system_name, user_name, session['username'], system_username)):
                flash(('Successfully Restored System Access', 'success'))
            else:
                flash(('Failed to Restore System Access', 'danger'))
            # Restore_system_access(system_name, user_name, session['username'], system_username)
    head = getheader('SYSTEM_ACCESS_TABLE')
    head[0] = 'Access ID'
    head[1] = 'User Name'
    head[2] = 'System Name'
    head[3] = 'System User Name'
    head[4] = 'Role'
    head[5] = 'Created On'
    head[6] = 'Changed On'
    head[7] = 'Removed'

    return render_template('Remove_System_Access.html', headers=head, data=getdata('SYSTEM_ACCESS_TABLE'), users=dropDown('USER_TABLE', 'USER_NAME'), systems=dropDown('SYSTEM_TABLE', 'SYSTEM_NAME'),system_users=dropDown('SYSTEM_ACCESS_TABLE', 'System_User_Name'), system_username=dropDown('SYSTEM_ACCESS_TABLE', 'System_User_Name'))


@app.route('/create-account', methods=['GET', 'POST'])
def create_accountpage():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        comfirm_password = request.form.get('comfirm_password')
        if (password == comfirm_password):
            if (Create_Account(username, password, session['username'])):
                flash(('Successfully Created Account', 'success'))
            else:
                flash(('Failed to Create Account', 'danger'))
        else:
            flash(('Passwords Do Not Match', 'danger'))
    return render_template('Create_Account.html')

@app.route('/change-password', methods=['GET', 'POST'])
def change_passwordpage():
    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        comfirm_password = request.form.get('comfirm_password')
        if (new_password == comfirm_password):
            if (Change_Password(old_password, new_password, session['username'])):
                flash(('Successfully Changed Password', 'success'))
            else:
                flash(('Password Change Failed', 'danger'))
        else:
            flash(('Passwords Do Not Match', 'danger'))

    return render_template('Change_Password.html')
    

@app.route('/generate-pdf', methods=['POST'])
def generate_reportpage():

    try:
        if session['log'] == False:
            return redirect('/')
    except:
        return redirect('/')
    username = request.form.get('user_name')

    pdf_path = 'report.pdf'
    if generatereport(username, session['username']):
        return send_file(pdf_path, download_name='report.pdf', as_attachment=True)

    # Serve the PDF to the client

    header = getheader('AUDIT_TRAIL')
    header[0] = 'ID'
    header[1] = 'Username'
    header[2] = 'Name'
    header[3] = 'Changed On'
    header[4] = 'Type of Change'
    header[5] = 'System Name'
    return render_template('home.html', headers=header, data=getdata('AUDIT_TRAIL'), users=dropDown('USER_TABLE', 'User_Name'))



@app.route('/upload', methods=['POST'])
def upload():
    selected_table = request.form['table']
    csv_file = request.files['csv_file']
    if csv_file:
        csv_data = csv_file.read().decode('utf-8').splitlines()
        csv_reader = csv.reader(csv_data)
        next(csv_reader)  # Skip header

        if not importcsv(selected_table, session['username'], csv_reader):
            flash(('Failed to Import CSV', 'danger'))
        else:
            flash(('Succesfully Imported CSV', 'success'))
        header = getheader('AUDIT_TRAIL')
        header[0] = 'ID'
        header[1] = 'Username'
        header[2] = 'Name'
        header[3] = 'Changed On'
        header[4] = 'Type of Change'
        header[5] = 'System Name'
        return render_template('home.html', headers=header, data=getdata('AUDIT_TRAIL'), users=dropDown('USER_TABLE', 'User_Name'))

if __name__ == '__main__':
    app.run(debug=True)