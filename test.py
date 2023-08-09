import pyodbc


conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP\SQLEXPRESS;'
                      'Database=User Management Application;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


cursor.execute("INSERT INTO Audit_Trail (column1, column2, ...) VALUES (%s, %s, ...)", (value1, value2, ...))
conn.commit()