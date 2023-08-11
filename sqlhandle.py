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

    return True

def Create_System(system_name, description, company, software, Owner_User):
    if (system_name == "" and description == "" and company == "" and software == ""):
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

def Add_system_access(system_name, user_name, system_username, Owner_User):
    if (system_name == "" and user_name == "" and system_username == ""):
        return False
    

    cursor.execute(f"SELECT count(System_Name) FROM SYSTEM_ACCESS_TABLE WHERE System_Name = '{system_name}' AND User_Name = '{user_name}' AND SYSTEM_USER_NAME = '{system_username}';")
    for i in cursor:
        if i[0] == 0:
            break
        else:
            return False
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"INSERT INTO SYSTEM_ACCESS_TABLE(System_Name, User_Name, Created_On, Changed_On, System_user_name, Removed) VALUES('{system_name}', '{user_name}', '{Changed_On}', '{Changed_On}', '{system_username}', 'F')"
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
        for x in range(9):
            text = f"{getheader('USER_TABLE')[x]}: {i[x]}"
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
        spacer = Spacer(1, 0.25 * inch)
        flowables.append(spacer)
        for x in range(7):
            text = f"{getheader('SYSTEM_ACCESS_TABLE')[x]}: {i[x]}"
            style = red_style if color == colors.red else blue_style
            para = Paragraph(text, style=style)
            flowables.append(para)

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
        ("Access Changed by: ", "", ""),
        ("Access Approved by: ", "", "")
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
    text = "Signature _____________________"
    para = Paragraph(text, style=styles["Title"])
    flowables.append(para)
    spacer = Spacer(1, 0.25 * inch)
    flowables.append(spacer)

    doc.build(flowables)




"""



DELETE FROM AUDIT_TRAIL
DELETE FROM SYSTEM_ACCESS_TABLE
DELETE FROM SYSTEM_TABLE


DBCC CHECKIDENT ('AUDIT_TRAIL', RESEED, 0);
DBCC CHECKIDENT ('SYSTEM_ACCESS_TABLE', RESEED, 0);



"""