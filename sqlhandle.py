import pyodbc 
import requests
import time
from hashlib import sha256
import aspose.pdf as ap
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP\SQLEXPRESS;'
                      'Database=User Management Application;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()



def ping():
    print("Pong")

        

def Create_User(User_Name, First_Name, Last_Name, Department, Company, Company_Email_Address, Owner_User):
    
    if (User_Name == "" and First_Name == "" and Last_Name == "" and Department == "" and Company == "" and Company_Email_Address == ""):
        return False
    
    if User_Name == "":
        return False
    
    cursor.execute(f"SELECT count(USER_NAME) FROM USER_TABLE WHERE USER_NAME = '{User_Name}';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False
        
    Created_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = "INSERT INTO USER_TABLE(User_Name, First_Name, Last_Name, Department, Company, Company_Email_Address, Created_On, Changed_On, Removed) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"
    cursor.execute(query, (User_Name, First_Name, Last_Name, Department, Company, Company_Email_Address, Created_On, Created_On, 'F'))
    conn.commit()

    audit_query = "INSERT INTO Audit_Trail(User_Name, Name, Changed_On, Type_Of_Change) VALUES(?, ?, ?, ?);"
    cursor.execute(audit_query, (User_Name, Owner_User, Created_On, "Created User"))
    conn.commit()

    return True




def Restore_User(user_name, Owner_User):
    if (user_name == ""):
        return False
    
    cursor.execute(f"SELECT count(USER_NAME) FROM USER_TABLE WHERE USER_NAME = '{user_name}';")
    for i in cursor:
        if i[0] > 0:
            break
        else:
            return False
        
    cursor.execute(f"SELECT count(USER_NAME) FROM USER_TABLE WHERE USER_NAME = '{user_name}' AND Removed = 'F';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False

    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"UPDATE USER_TABLE SET Removed = 'F', Changed_On = '{Changed_On}' WHERE User_Name = '{user_name}'"
    cursor.execute(query)
    conn.commit()
    
    audit_query = "INSERT INTO Audit_Trail( User_Name, Name, Changed_On, Type_Of_Change) VALUES(?, ?, ?, ?);"
    cursor.execute(audit_query, (user_name, Owner_User, Changed_On, "Restored User"))
    conn.commit()

    return True

def Delete_User(User_Name, Owner_User):
    if (User_Name == ""):
        return False
    
    cursor.execute(f"SELECT count(USER_NAME) FROM USER_TABLE WHERE USER_NAME = '{User_Name}';")
    for i in cursor:
        if i[0] > 0:
            break
        else:
            return False
        
    cursor.execute(f"SELECT count(USER_NAME) FROM USER_TABLE WHERE USER_NAME = '{User_Name}' AND Removed = 'T';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False

    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"UPDATE USER_TABLE SET Removed = 'T', Changed_On = '{Changed_On}' WHERE User_Name = '{User_Name}'"
    cursor.execute(query)
    conn.commit()
    
    audit_query = "INSERT INTO Audit_Trail( User_Name, Name, Changed_On, Type_Of_Change) VALUES(?, ?, ?, ?);"
    cursor.execute(audit_query, (User_Name, Owner_User, Changed_On, "Deleted User"))
    conn.commit()

    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE USER_NAME = '{User_Name}' AND REMOVED = 'F';")
    for i in cursor:
        if i[0] == 0:
            return True
        else:
            # print("bob")
            break 
    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE USER_NAME = '{User_Name}';")
    for i in cursor:
        if i[0] > 0:
            break
        else:
            return True
    print("test")
    systemname = cursor.execute(f"Select SYSTEM_NAME FROM SYSTEM_ACCESS_TABLE WHERE USER_NAME = '{User_Name}'")
    systemname = systemname.fetchall()
    systems = []
    for i in systemname:
        systems.append(i[0])

    print(systems)


    for i in systems:
        query = f"UPDATE SYSTEM_ACCESS_TABLE SET Removed = 'T', Changed_On = '{Changed_On}' WHERE USER_NAME = '{User_Name}';"
        cursor.execute(query)
        audit_query = "INSERT INTO Audit_Trail(System_name, Name, Changed_On, Type_Of_Change, USER_NAME) VALUES(?, ?, ?,?,?);"
        cursor.execute(audit_query, ( i, Owner_User, Changed_On, "Deleted System Access", User_Name))
        conn.commit()


    return True

def Create_System(system_name, description, company, software, Owner_User):
    if (system_name == "" and description == "" and company == "" and software == ""):
        return False
    
    if (system_name == ""):
        return False
    
    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_TABLE WHERE System_Name = '{system_name}';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False
    Created_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = "INSERT INTO SYSTEM_TABLE(System_Name, Description, Company, Software, Created_On, Changed_On, Removed) VALUES(?, ?, ?, ?, ?, ?, ?);"
    cursor.execute(query, (system_name, description, company, software, Created_On, Created_On, 'F'))
    conn.commit()


    audit_query = "INSERT INTO Audit_Trail( System_name, Name, Changed_On, Type_Of_Change) VALUES( ?, ?, ?, ?);"
    cursor.execute(audit_query, (system_name, Owner_User, Created_On, "Created System"))
    conn.commit()

    return True

def Delete_System(system_name, Owner_User):
    if (system_name == ""):
        return False
    
    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_TABLE WHERE System_Name = '{system_name}';")
    for i in cursor:
        if i[0] > 0:
            break
        else:
            return False
        

    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_TABLE WHERE System_Name = '{system_name}' AND Removed = 'T';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"UPDATE SYSTEM_TABLE SET Removed = 'T', Changed_On = '{Changed_On}' WHERE System_Name = '{system_name}'"
    cursor.execute(query)
    conn.commit()

    
    audit_query = "INSERT INTO Audit_Trail(System_name, Name, Changed_On, Type_Of_Change) VALUES( ?, ?, ?, ?);"
    cursor.execute(audit_query, ( system_name, Owner_User, Changed_On, "Deleted System"))
    conn.commit()

    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE System_Name = '{system_name}' AND REMOVED = 'F';")
    for i in cursor:
        if i[0] == 0:
            return True
        else:
            # print("bob")
            break 
    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE System_Name = '{system_name}';")
    for i in cursor:
        if i[0] > 0:
            break
        else:
            return True
    print("test")
    username = cursor.execute(f"Select USER_NAME FROM SYSTEM_ACCESS_TABLE WHERE System_Name = '{system_name}'")
    username = username.fetchall()
    users = []
    for i in username:
        users.append(i[0])


    for i in users:
        query = f"UPDATE SYSTEM_ACCESS_TABLE SET Removed = 'T', Changed_On = '{Changed_On}' WHERE System_Name = '{system_name}';"
        cursor.execute(query)
        audit_query = "INSERT INTO Audit_Trail(System_name, Name, Changed_On, Type_Of_Change, USER_NAME) VALUES(?, ?, ?,?,?);"
        cursor.execute(audit_query, ( system_name, Owner_User, Changed_On, "Deleted System Access", i))
        conn.commit()


    return True


def Restore_System(system_name, Owner_User):
    if (system_name == ""):
        return False
    
    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_TABLE WHERE System_Name = '{system_name}';")
    for i in cursor:
        if i[0] > 0:
            break
        else:
            return False
        

    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_TABLE WHERE System_Name = '{system_name}' AND Removed = 'F';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"UPDATE SYSTEM_TABLE SET Removed = 'F', Changed_On = '{Changed_On}' WHERE System_Name = '{system_name}'"
    cursor.execute(query)
    conn.commit()

    
    audit_query = "INSERT INTO Audit_Trail(System_name, Name, Changed_On, Type_Of_Change) VALUES( ?, ?, ?, ?);"
    cursor.execute(audit_query, ( system_name, Owner_User, Changed_On, "Restored System"))
    conn.commit()
    return True

def Add_system_access(system_name, user_name, system_username, Owner_User, role):
    if (system_name == "" and user_name == "" and system_username == "" and role == ""):
        return False
    

    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE System_Name = '{system_name}' AND User_Name = '{user_name}' AND SYSTEM_USER_NAME = '{system_username}';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"INSERT INTO SYSTEM_ACCESS_TABLE(System_Name, User_Name, Created_On, Changed_On, System_user_name, Removed, ROLE) VALUES('{system_name}', '{user_name}', '{Changed_On}', '{Changed_On}', '{system_username}', 'F', '{role}')"
    cursor.execute(query)
    conn.commit()

    audit_query = "INSERT INTO Audit_Trail(System_name, Name, Changed_On, Type_Of_Change, user_name) VALUES( ?, ?, ?, ?,?);"
    cursor.execute(audit_query, ( system_name, Owner_User, Changed_On, "Added System Access", user_name))
    conn.commit()
    return True

def Delete_system_access(system_name, user_name, Owner_User, system_user_name):
    if (system_name == "" and user_name == ""):
        return False
    

    
    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE System_Name = '{system_name}' AND User_Name = '{user_name}' AND SYSTEM_USER_NAME = '{system_user_name}' AND REMOVED = 'T';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False
    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE System_Name = '{system_name}' AND User_Name = '{user_name}' AND SYSTEM_USER_NAME = '{system_user_name}';")
    for i in cursor:
        if i[0] > 0:
            break
        else:
            return False
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"UPDATE SYSTEM_ACCESS_TABLE SET Removed = 'T', Changed_On = '{Changed_On}' WHERE System_Name = '{system_name}' AND User_Name = '{user_name}' AND SYSTEM_USER_NAME = '{system_user_name}'"
    cursor.execute(query)
    conn.commit()


    audit_query = "INSERT INTO Audit_Trail(System_name, Name, Changed_On, Type_Of_Change, user_name) VALUES( ?, ?, ?, ?,?);"
    cursor.execute(audit_query, ( system_name, Owner_User, Changed_On, "Deleted System Access", user_name))
    conn.commit()
    return True
   


def Restore_system_access(system_name, user_name, owner, system_user_name):
    if (system_name == "" and user_name == ""):
        return False
    
    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE System_Name = '{system_name}' AND User_Name = '{user_name}' AND SYSTEM_USER_NAME = '{system_user_name}' AND REMOVED = 'F';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False
    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE System_Name = '{system_name}' AND User_Name = '{user_name}' AND SYSTEM_USER_NAME = '{system_user_name}';")
    for i in cursor:
        if i[0] > 0:
            break
        else:
            return False
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"UPDATE SYSTEM_ACCESS_TABLE SET Removed = 'F', Changed_On = '{Changed_On}' WHERE System_Name = '{system_name}' AND User_Name = '{user_name}' AND SYSTEM_USER_NAME = '{system_user_name}'"
    cursor.execute(query)
    conn.commit()


    audit_query = "INSERT INTO Audit_Trail(System_name, Name, Changed_On, Type_Of_Change, user_name) VALUES( ?, ?, ?, ?,?);"
    cursor.execute(audit_query, ( system_name, owner, Changed_On, "Restored System Access", user_name))
    conn.commit()
    return True
    
    

def getheader(table):
    cursor.execute(f"SELECT * FROM {table}")
    header = [i[0] for i in cursor.description]
    return header


def getdata(table):
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    return data


def correct_password(username, password):
    cursor.execute(f"SELECT PASSWORD FROM LOGINS WHERE USERNAME = '{username}'")
    for i in cursor:
        if i[0] == sha256(password.encode('utf-8')).hexdigest():
            return True
        else:
            return False
    return False

def sdropDown(table, dropDown):
    cursor.execute(f"SELECT {dropDown} FROM {table} WHERE Removed = 'F'")
    data = cursor.fetchall() # [(x, ), (y, ), (z, )]
    newdata = [x[0] for x in data] # [x, y, z]
    return newdata

def dropDown(table, dropDown):
    cursor.execute(f"SELECT {dropDown} FROM {table}")
    data = cursor.fetchall() # [(x, ), (y, ), (z, )]
    newdata = [x[0] for x in data] # [x, y, z]
    return newdata

def auditlog(username, typeofchange):
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = "INSERT INTO Audit_Trail(Name, Changed_On, Type_Of_Change) VALUES(?, ?, ?);"
    cursor.execute(query, (username, Changed_On, typeofchange))
    conn.commit()


def Create_Account(username, password, owner):
    if (username == "" and password == ""):
        return False
    cursor.execute(f"SELECT count(Username) FROM LOGINS WHERE Username = '{username}';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"INSERT INTO LOGINS(Username, Password) VALUES('{username}', '{sha256(password.encode('utf-8')).hexdigest()}')"
    cursor.execute(query)
    conn.commit()

    audit_query = "INSERT INTO Audit_Trail(Name, Changed_On, Type_Of_Change, user_name) VALUES( ?, ?, ?, ?);"
    cursor.execute(audit_query, ( owner, Changed_On, "Created Account", username))
    conn.commit()
    return True

def Change_Password(old_password, new_password, owner):
    if (old_password == "" and new_password == ""):
        return False
    cursor.execute(f"SELECT count(Username) FROM LOGINS WHERE Username = '{owner}' AND Password = '{sha256(old_password.encode('utf-8')).hexdigest()}';")
    for i in cursor:
        if i[0] > 0:
            break
        else:
            return False
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"UPDATE LOGINS SET Password = '{sha256(new_password.encode('utf-8')).hexdigest()}' WHERE Username = '{owner}'"
    cursor.execute(query)
    conn.commit()

    audit_query = "INSERT INTO Audit_Trail(Name, Changed_On, Type_Of_Change) VALUES( ?, ?, ?);"
    cursor.execute(audit_query, ( owner, Changed_On, "Changed Password"))
    conn.commit()
    return True



def generatereport(username, owner):

    cursor.execute(f"SELECT count(USER_NAME) FROM USER_TABLE WHERE USER_NAME = '{username}';")
    for i in cursor:
        if i[0] == 0:
            return False
        else:
            break
    doc = SimpleDocTemplate(
        "report.pdf",
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=18,
    )
    styles = getSampleStyleSheet()

    # Define a custom ParagraphStyle with the desired color
    red_style = ParagraphStyle(
        name='RedText',
        parent=styles['Normal'],
        textColor=colors.red
    )
    blue_style = ParagraphStyle(
        name='BlueText',
        parent=styles['Normal'],
        textColor=colors.blue
    )

    flowables = []

    changed_on = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    text = "Generated by: " + owner + " on " + changed_on
    para = Paragraph(text, style=styles["Title"])
    flowables.append(para)

    text = "for user: " + username
    para = Paragraph(text, style=styles["Title"])
    flowables.append(para)


    removed = cursor.execute(f"SELECT Removed FROM USER_TABLE WHERE USER_NAME = '{username}'")
    removed = removed.fetchall()
    removed = removed[0][0]
    text=f"User State: {'Active' if removed == 'F' else 'Inactive'}"
    para = Paragraph(text, style=styles["Title"])
    flowables.append(para)

    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)
    text = "User Information"
    para = Paragraph(text, style=styles["Title"])
    flowables.append(para)
    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)

    cursor.execute(f"SELECT * FROM USER_TABLE WHERE USER_NAME = '{username}'")
    data = cursor.fetchall()
    for i in data:
        text = f"Username: {i[0]}"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = f"First Name: {i[1]}"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = f"Last Name: {i[2]}"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = f"Department: {i[3]}"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = f"Company: {i[4]}"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = f"Company Email Address: {i[5]}"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = f"Created On: {i[6]}"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

        text = f"Changed On: {i[7]}"
        para = Paragraph(text, style=styles["Normal"])
        flowables.append(para)

    
        flowables.append(Paragraph("", style=styles["Title"]))

    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)

    text = "System Access"
    para = Paragraph(text, style=styles["Title"])
    flowables.append(para)

    cursor.execute(f"SELECT * FROM SYSTEM_ACCESS_TABLE WHERE USER_NAME = '{username}'")
    data = cursor.fetchall()
    for i in data:
        color = colors.red if i[6] == 'T' else colors.blue
        style = red_style if color == colors.red else blue_style
        spacer = Spacer(1, 0.25 * inch)
        flowables.append(spacer)
        text = f"Access ID: {i[0]}"
        para = Paragraph(text, style=style)
        flowables.append(para)
        text = f"Username: {i[1]}"
        para = Paragraph(text, style=style)
        flowables.append(para)
        text = f"System Name: {i[2]}"
        para = Paragraph(text, style=style)
        flowables.append(para)
        text = f"System Username: {i[3]}"
        para = Paragraph(text, style=style)
        flowables.append(para)
        text = f"Role: {i[4]}"
        para = Paragraph(text, style=style)
        flowables.append(para)
        text = f"Created On: {i[5]}"
        para = Paragraph(text, style=style)
        flowables.append(para)
        text = f"Changed On: {i[6]}"
        para = Paragraph(text, style=style)
        flowables.append(para)
        # for x in range(7):
        #     text = f"{getheader('SYSTEM_ACCESS_TABLE')[x]}: {i[x]}"
        #     para = Paragraph(text, style=style)
        #     flowables.append(para)

    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)

    text = "Audit Information"
    para = Paragraph(text, style=styles["Title"])
    flowables.append(para)
    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)

    cursor.execute(f"SELECT * FROM AUDIT_TRAIL WHERE USER_NAME = '{username}'")
    data = cursor.fetchall()

    data.insert(0, getheader('AUDIT_TRAIL'))
    tblstyle = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])
    data = [list(i) for i in data]
    audit_table = Table(data)
    audit_table.setStyle(tblstyle)

    flowables.append(audit_table)

    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)

    text = "Approval"
    para = Paragraph(text, style=styles["Title"])
    flowables.append(para)
    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)

    approval_data = [
        ("", "Name                                          ", "Date                                            "),
        ("Access Changed by: ", "\n", "\n"),
        ("Access Approved by: ", "\n", "\n")
    ]

    tblstyle = TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black)])
    approval_data = [list(i) for i in approval_data]
    approval_table = Table(approval_data)
    approval_table.setStyle(tblstyle)

    flowables.append(approval_table)

    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)
    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)
    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)

    # Print Signature field

    # spacer = Spacer(1, 0.25 * inch)
    # flowables.append(spacer)

    doc.build(flowables)
    return True


def importcsv(tablename, owner, data):
    if tablename == "USER_TABLE":
        for row in data:
            print(row)



            try:
                user_name = row[0]
            except ValueError:
                return False

            try:
                first_name = row[1]
            except ValueError:
                first_name = ""

            try:
                last_name = row[2]
            except ValueError:
                last_name = ""
            
            try:
                department = row[3]
            except ValueError:
                department = ""

            try:
                company = row[4]
            except ValueError:
                company = ""
            
            try:
                email = row[5]
            except ValueError:
                email = ""


            cursor.execute(f"SELECT count(USER_NAME) FROM USER_TABLE WHERE USER_NAME = '{user_name}';")
            for i in cursor:
                if i[0] == 0:
                    break
                else:
                    return False
            # Convert datetime strings to datetime objects
            created_on = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            changed_on = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # Insert data into the database
            cursor.execute('''
                INSERT INTO USER_TABLE
                (USER_NAME, FIRST_NAME, LAST_NAME, DEPARTMENT, COMPANY, COMPANY_EMAIL_ADDRESS, CREATED_ON, CHANGED_ON, REMOVED)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_name, first_name, last_name, department, company, email, created_on, changed_on, 'F'))
            


            conn.commit()
            # audit trail
            audit_query = "INSERT INTO Audit_Trail( User_Name, Name, Changed_On, Type_Of_Change) VALUES(?, ?, ?, ?);"
            cursor.execute(audit_query, (user_name, owner, changed_on, "Imported User"))
            conn.commit()
        return True
    elif tablename == "SYSTEM_TABLE":
        for row in data:

            # # check the number of rows
            # if len(row) < 4:
            #     return False
            
            try:
                system_name = row[0]
            except ValueError:
                return False
            
            try:
                description = row[1]
            except ValueError:
                description = ""

            try:
                company = row[2]
            except ValueError:
                company = ""
                

            try:
                software = row[3]
            except ValueError:
                software = ""


        

            cursor.execute(f"SELECT count(SYSTEM_NAME) FROM SYSTEM_TABLE WHERE SYSTEM_NAME = '{system_name}';")
            for i in cursor:
                if i[0] == 0:
                    break
                else:
                    return False
            # Convert datetime strings to datetime objects
            created_on = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            changed_on = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # Insert data into the database
            cursor.execute('''
                INSERT INTO System_Table
                (system_name, description, company, software, created_on, changed_on, removed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (system_name, description, company, software, created_on, changed_on, 'F'))
            
            conn.commit()
            # audit trail
            audit_query = "INSERT INTO Audit_Trail( System_Name, Name, Changed_On, Type_Of_Change) VALUES(?, ?, ?, ?);"
            cursor.execute(audit_query, (system_name, owner, changed_on, "Imported System"))
            conn.commit()
        return True
    elif tablename == "SYSTEM_ACCESS_TABLE":
        for row in data:

            # # check the number of rows
            # if len(row) < 5:
            #     return False

            try:
                username = row[1]
            except ValueError:
                return False
            
            try:
                system_name = row[2]
            except ValueError:
                return False
            
            try:
                system_username = row[3]
            except ValueError:
                system_username = ""

            try:
                role = row[4]
            except ValueError:
                role = ""

            cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE System_Name = '{system_name}' AND User_Name = '{username}' AND SYSTEM_USER_NAME = '{system_username}';")
            for i in cursor:
                if i[0] == 0:
                    break
                else:
                    return False
            # Convert datetime strings to datetime objects
            created_on = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            changed_on = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # Insert data into the database
            cursor.execute('''
                INSERT INTO System_ACCESS_Table
                (user_name, system_name,SYSTEM_USER_NAME, created_on, changed_on, removed, role)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username,system_name, system_username, created_on, changed_on, 'F', role))

            
            conn.commit()
            # audit trail
            audit_query = "INSERT INTO Audit_Trail( System_Name, Name, Changed_On, Type_Of_Change, user_name) VALUES(?, ?, ?, ?,?);"
            cursor.execute(audit_query, (system_name, owner, changed_on, "Imported System Access", username))
            conn.commit()
        return True


"""



DELETE FROM AUDIT_TRAIL
DELETE FROM SYSTEM_ACCESS_TABLE
DELETE FROM SYSTEM_TABLE


DBCC CHECKIDENT ('AUDIT_TRAIL', RESEED, 0);
DBCC CHECKIDENT ('SYSTEM_ACCESS_TABLE', RESEED, 0);



"""