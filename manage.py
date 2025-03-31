from flask import Flask, redirect, url_for, render_template, request
import sqlite3
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/flask')
def hello_flask():  
    return 'Hello Flask'

@app.route('/python/<name>')
def hello_python(name):
    if name == 'ken':
        return 'Hello Python with {0} as the admin'.format(name)
    else:
        return 'Welcome guest!'

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success',name = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success',name = user))
    
@app.route('/success/<name>')
def success(name):
    return 'Welcome {0}'.format(name)

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['addr']
         city = request.form['city']
         zip = request.form['zip']
         
         with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,zip) VALUES ('{0}','{1}','{2}','{3}')".format(nm,addr,city,zip))
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "Error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sqlite3.connect("database.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall(); 
   return render_template("list.html",rows = rows)


if __name__ == '__main__':
    app.run()