from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

import sqlite3 as sql

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():
   return render_template('home.html')

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
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            q = "INSERT INTO students (name,addr,city,pin) VALUES ('{0}','{1}','{2}','{3}')".format(nm,addr,city,pin)
            cur.execute(q)
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)