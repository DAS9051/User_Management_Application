import pyodbc 
import requests
import time
from hashlib import sha256


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP\SQLEXPRESS;'
                      'Database=User Management Application;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()



def ping():
    print("Pong")

        

def Create_User(User_Name, First_Name, Last_Name, Department, Company, Company_Email_Address, Owner_User):
    Created_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = "INSERT INTO USER_TABLE(User_Name, First_Name, Last_Name, Department, Company, Company_Email_Address, Created_On, Changed_On, Removed) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);"
    cursor.execute(query, (User_Name, First_Name, Last_Name, Department, Company, Company_Email_Address, Created_On, Created_On, 'F'))
    conn.commit()

    audit_query = "INSERT INTO Audit_Trail(User_Name, Name, Changed_On, Type_Of_Change) VALUES(?, ?, ?, ?);"
    cursor.execute(audit_query, (User_Name, Owner_User, Created_On, "Created User"))
    conn.commit()

def Delete_User(User_Name, Owner_User):
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"UPDATE USER_TABLE SET Removed = 'T', Changed_On = '{Changed_On}' WHERE User_Name = '{User_Name}'"
    cursor.execute(query)
    conn.commit()
    
    audit_query = "INSERT INTO Audit_Trail( User_Name, Name, Changed_On, Type_Of_Change) VALUES(?, ?, ?, ?);"
    cursor.execute(audit_query, (User_Name, Owner_User, Changed_On, "Deleted User"))
    conn.commit()

def Create_System(system_name, description, company, software, Owner_User):
    Created_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = "INSERT INTO SYSTEM_TABLE(System_Name, Description, Company, Software, Created_On, Changed_On, Removed) VALUES(?, ?, ?, ?, ?, ?, ?);"
    cursor.execute(query, (system_name, description, company, software, Created_On, Created_On, 'F'))
    conn.commit()


    audit_query = "INSERT INTO Audit_Trail( System_name, Name, Changed_On, Type_Of_Change) VALUES( ?, ?, ?, ?);"
    cursor.execute(audit_query, (system_name, Owner_User, Created_On, "Created System"))
    conn.commit()

def Delete_System(system_name, Owner_User):
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"UPDATE SYSTEM_TABLE SET Removed = 'T', Changed_On = '{Changed_On}' WHERE System_Name = '{system_name}'"
    cursor.execute(query)
    conn.commit()

    
    audit_query = "INSERT INTO Audit_Trail(System_name, Name, Changed_On, Type_Of_Change) VALUES( ?, ?, ?, ?);"
    cursor.execute(audit_query, ( system_name, Owner_User, Changed_On, "Deleted System"))
    conn.commit()

def Add_system_access(system_name, user_name, system_username, Owner_User):

    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"INSERT INTO SYSTEM_ACCESS_TABLE(System_Name, User_Name, Created_On, Changed_On, System_user_name, Removed) VALUES('{system_name}', '{user_name}', '{Changed_On}', '{Changed_On}', '{system_username}', 'F')"
    cursor.execute(query)
    conn.commit()

    audit_query = "INSERT INTO Audit_Trail(System_name, Name, Changed_On, Type_Of_Change, user_name) VALUES( ?, ?, ?, ?,?);"
    cursor.execute(audit_query, ( system_name, Owner_User, Changed_On, "Added System Access", user_name))
    conn.commit()

def Delete_system_access(system_name, user_name, Owner_User):
    Changed_On = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    query = f"UPDATE SYSTEM_ACCESS_TABLE SET Removed = 'T', Changed_On = '{Changed_On}' WHERE System_Name = '{system_name}' AND User_Name = '{user_name}'"
    cursor.execute(query)
    conn.commit()


    audit_query = "INSERT INTO Audit_Trail(System_name, Name, Changed_On, Type_Of_Change, user_name) VALUES( ?, ?, ?, ?,?);"
    cursor.execute(audit_query, ( system_name, Owner_User, Changed_On, "Deleted System Access", user_name))
    conn.commit()
    
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


# Create_System("Test", "Test", "Test", "Test")