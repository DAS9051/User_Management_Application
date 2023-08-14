# WebApp Deployment and Dependencies Documentation

This documentation provides a step-by-step guide on how to deploy the given web application on a server, along with the necessary dependencies and configurations.

## Table of Contents
1. [Introduction](#introduction)
2. [Dependencies](#dependencies)
3. [SQL Server Table Creation](#sql-server-setup)
4. [Deployment Steps](#deployment-steps)

## 1. Introduction<a name="introduction"></a>
This web application is built using Flask and relies on various libraries and dependencies to function properly. The application includes multiple files, including Flask code, SQL handling scripts, and HTML templates.

## 2. Python Dependencies<a name="dependencies"></a>
Before deploying the web application, make sure you have the following dependencies installed:

- Python (3.6+)
- Flask
- pyodbc
- requests
- aspose.pdf
- reportlab
- flask_session

You can install these dependencies using the following command:
```bash
pip install Flask pyodbc requests aspose.pdf reportlab flask_session
```

## 3. SQL Server Setup<a name="sql-server-setup"></a>
Before running the web application, ensure that you have a Microsoft SQL Server instance configured and running. Update the connection string in the code to match your SQL Server configuration. Modify the connection string in  `sqlhandle.py`.

## Tables Creation
Create the required tables in your SQL Server database. Execute the following SQL queries to create the necessary tables:

1. **Audit Trail Table**:

   ```sql
   CREATE TABLE Audit_Trail (
       id INT IDENTITY(1,1) PRIMARY KEY,
       user_name VARCHAR(255),
       NAME VARCHAR(255),
       Changed_On DATETIME,
       Type_of_Change VARCHAR(255),
       System_name VARCHAR(255)
   );

   -- Reset identity seed for Audit_Trail table
   DBCC CHECKIDENT ('Audit_Trail', RESEED, 0);
    ```
2. **Logins Table**:

    ```sql
    CREATE TABLE Logins (
        username VARCHAR(50),
        password VARCHAR(70)
    );
    ```

3. **System Table:**

    ```sql
    CREATE TABLE System (
    SYSTEM_NAME VARCHAR(50),
    DESCRIPTION VARCHAR(200),
    Company VARCHAR(50),
    SOFTWARE VARCHAR(50),
    Created_on VARCHAR(50),
    Changed_On VARCHAR(50),
    removed CHAR(1),
    PRIMARY KEY (SYSTEM_NAME)
    );
    ```

4. **System Access Table:**

    ```sql
    CREATE TABLE System_Access (
        Access_Id INT IDENTITY(1,1) PRIMARY KEY,
        Username VARCHAR(255),
        system_name VARCHAR(255),
        system_User_name VARCHAR(255),
        role VARCHAR(255),
        created_on DATETIME,
        changed_on DATETIME,
        removed CHAR(1)
    );
    ```
    

5. **User Table:**

    ```sql
    CREATE TABLE User_Table (
    User_name VARCHAR(50),
    First_Name VARCHAR(20),
    Last_name VARCHAR(20),
    Department VARCHAR(20),
    Company VARCHAR(50),
    Company_Email_address VARCHAR(50),
    Created_On VARCHAR(50),
    Changed_On VARCHAR(50),
    removed CHAR(1),
    );
    ```
## 4. Deployment Steps<a name="deployment-steps"></a>
Follow these steps to deploy the web application:

1. **Clone the Repository**: Clone the repository or transfer the necessary files to your server.

2. **Navigate to Root Directory**: Open a terminal on the server and navigate to the root directory of the web application.

3. **Install Dependencies**: Install the required dependencies as mentioned in the "Dependencies" section.
