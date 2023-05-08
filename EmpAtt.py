from flask import Flask, render_template, request, redirect
import sqlite3
from pymysql import connections
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'

@app.route('/')
def EmpAtt():
    c.execute("SELECT * FROM employee")
    rows = c.fetchall()
    return render_template('EmpAtt.html', rows=rows)

@app.route('/add_attendance', methods=['POST'])
def add_attendance():
    name = request.form['name']
    date = request.form['date']
    status = request.form['status']
    c.execute("INSERT INTO attendance (name, date, status) VALUES (?, ?, ?)", (name, date, status))
    conn.commit()
    return redirect('/')

@app.route('/edit_attendance/<int:id>', methods=['GET', 'POST'])
def edit_attendance(id):
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        status = request.form['status']
        c.execute("UPDATE attendance SET name=?, date=?, status=? WHERE id=?", (name, date, status, id))
        conn.commit()
        return redirect('/')
    else:
        c.execute("SELECT * FROM attendance WHERE id=?", (id,))
        row = c.fetchone()
        return render_template('edit_attendance.html', row=row)

@app.route('/delete_attendance/<int:id>')
def delete_attendance(id):
    c.execute("DELETE FROM attendance WHERE id=?", (id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
