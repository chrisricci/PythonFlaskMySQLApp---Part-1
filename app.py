import os
import sys
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = os.environ.get('MYSQL_DATABASE_USER') if os.environ.get('MYSQL_DATABASE_USER') != None else 'root'
sys.stdout.write(os.environ.get('MYSQL_DATABASE_USER'))
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('MYSQL_DATABASE_PASSWORD') if os.environ.get('MYSQL_DATABASE_PASSWORD') != None else 'mYcezJ@rySIk@LhehJaM(AcajaD'
sys.stdout.write(os.environ.get('MYSQL_DATABASE_PASSWORD'))
app.config['MYSQL_DATABASE'] = os.environ.get('MYSQL_DATABASE') if os.environ.get('MYSQL_DATABASE') != None else 'db1'
sys.stdout.write(os.environ.get('MYSQL_DATABASE'))
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('MYSQL_DATABASE_HOST') if os.environ.get('MYSQL_DATABASE_HOST') != None else 'localhost1'
sys.stdout.write(os.environ.get('MYSQL_DATABASE_HOST'))
sys.stdout.flush()
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showAdmin')
def showAdmin():
    return render_template('admin.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            print(_hashed_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

conn = mysql.connect()
cursor = conn.cursor()
@app.route('/initDb',methods=['POST','GET'])
def initDb():
    try:

        # Create Table
        createTableCommand = "CREATE TABLE tbl_user (`user_id` BIGINT NOT NULL AUTO_INCREMENT,`user_name` VARCHAR(45) NULL,`user_username` VARCHAR(45) NULL, `user_password` VARCHAR(100) NULL,PRIMARY KEY (`user_id`))"
        cursor.execute(createTableCommand)
        data = cursor.fetchall()

        # Create Stored Procedure
        createStoredProcCommand = "CREATE PROCEDURE `sp_createUser`(IN p_name VARCHAR(20), IN p_username VARCHAR(20), IN p_password VARCHAR(100)) BEGIN if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN select 'Username Exists !!'; ELSE insert into tbl_user (user_name, user_username, user_password) values ( p_name, p_username, p_password); END IF; END"

        cursor.execute(createStoredProcCommand)
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'Database Initialized successfully!'})
        else:
            return json.dumps({'error':str(data[0])})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
