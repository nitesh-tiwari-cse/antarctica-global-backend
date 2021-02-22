from flask import Flask, render_template, request, redirect, url_for, session 
from flask_graphql import GraphQLView
import re
from model import db_session , Base,engine, Department , User
from catalog import schema

app = Flask(__name__)
app.debug = True
Base.metadata.create_all(bind=engine)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def adduser(fn,ln,email,pswd,dname):
     # Fill the tables with some data
    print(fn,ln,email,pswd,dname) 
    dpt = Department(name=dname)
    db_session.add(dpt)
    emp=fn+pswd[:3]
    print(emp)
    users = User(firstname=fn,lastname=ln,email=email,empid=emp,password=pswd,department=dpt)
    db_session.add(users)
    db_session.commit()

@app.route('/login', methods =['GET', 'POST']) 
def login(): 
    msg = '' 
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form: 
        username = request.form['email'] 
        password = request.form['password']  
        if username != '' and password != '':
            query = db_session.query(User).all()
            email = ''
            pswd = ''
            recobj={}
            for record in query:
                email = record.email
                pswd = record.password
                recobj = {
                    'First name': record.firstname,
                    'Last Name': record.lastname,
                    'Email': record.email,
					'Emp Id': record.empid,
                    'Organization Name': record.department.name
                }
      
            if username == email and password == pswd:
                msg = 'Logged in successfully !'
                
                return render_template('home.html', msg = msg,ans=recobj) 
            else:
                msg = 'Incorrect username / password !'    
        else: 
            msg = 'Please fill out the form !'
    return render_template('login.html', msg = msg) 
  
@app.route('/')   
@app.route('/register', methods =['GET', 'POST']) 
def register(): 
    msg = '' 
    if request.method == 'POST' and 'dname' in request.form and 'fname' in request.form and  'lname' in request.form and 'password' in request.form and 'email' in request.form : 
        fn = request.form['fname']
        ln= request.form['lname']
        password = request.form['password']
        email = request.form['email']
        dname = request.form['dname']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        #cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, )) 
        #account = cursor.fetchone() 
        #if account: 
        #msg = 'Account already exists !'
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
            msg = 'Invalid email address !'
        elif not fn or not password or not email: 
            msg = 'Please fill out the form !'
        else: 
            adduser(fn,ln,email,password,dname)
            #mysql.connection.commit() 
            msg = 'You have successfully registered !'
    elif request.method == 'POST': 
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg) 





if __name__ == '__main__':
    app.run()
