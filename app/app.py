from flask import *
import psycopg2
import psycopg2.extras
import re
from werkzeug.security import generate_password_hash, check_password_hash



app=Flask(__name__)

DB_HOST="172.28.224.1"
DB_NAME="app"
DB_USER="postgres"
DB_PASS="1234"

conn=psycopg2.connect(host=DB_HOST,dbname=DB_NAME,password=DB_PASS,user=DB_USER)

@app.route('/register', methods=['GET','POST'])
def register():
    cursor = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        fullname=request.form['fullname']
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        
        cursor.execute('SELECT * FROM USERS WHERE USERNAME = %s',(username))
        account = cursor.fetchone()
        print(account)

        if account:
            flash('La cuenta ya existe!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Email invalido!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('El nombre de usuario solo debe tener numeros y letras!')
        elif not username or not password or not email:
            flash('Por favor llena el formulario!')
        else:
            cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)", (fullname, username, _hashed_password, email))
            conn.commit()
            flash('Se ha registrado correctamente!')

    elif request.method == 'POST':
        flash('Por favor llena el formulario!')

    return render_template('register.html')

if __name__=='__main__':
    app.run(debug=True)