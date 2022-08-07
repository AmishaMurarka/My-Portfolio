# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 13:07:02 2022

@author: Amisha
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'adv_python_db'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)
with open(f'model.pkl', 'rb') as f:
    model = pickle.load(f)

def generate_random_number():
    global num
    num = np.random.randint(1,100)
    print("Random Number Generated:",num)   
    
# root route
@app.route('/')
def welcome_page():
    
    cur = mysql.connection.cursor()    	

    cur.execute('select * from project')
    project_data = cur.fetchall()
    
    #cur.execute('select distinct pri_lang, count(id) from project group by pri_lang')
    #skill_info = cur.fetchall()
    
    cur.execute('select objective, pri_lang, count(id) from project group by objective, pri_lang')
    skill_info = cur.fetchall()

    cur.close()
    
    return render_template('webpage.html', project=project_data, skill=skill_info) 

# Adding new project to database route
@app.route('/add_project')
def add_project():
    return render_template('add_project.html')

# Submit new project to database route
@app.route('/submit_project', methods=['POST'])
def submit_project():
    if request.method == 'POST':
        pname =  request.form['name']
        pdesc = request.form['descr']
        plang = request.form['plang']
        slang = request.form['slang']
        objective = request.form['objective']
        status = request.form['status']
        git = request.form['git']
        demo = request.form['demo']
        
        cur = mysql.connection.cursor()    	

        cur.execute('insert into project(name,description,pri_lang,sec_lang,objective,status,github_link,live_demo_link) values ("{}","{}","{}","{}","{}","{}","{}","{}")'.format(pname,pdesc,plang,slang,objective,status,git,demo))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('welcome_page'))

# number game route
@app.route('/number_game')
def number_game():
    global num
    generate_random_number()
    return render_template('number_game.html',num = num, res = "noinput")

# number game - guess route
@app.route('/number_game/guess', methods = ['POST'])
def user_guess():
    guess = int(request.form['guess'])
    if(guess == num):   
        return render_template('number_game.html',num = num, res = 'correct')
    elif(guess>num):
        return render_template('number_game.html',res = 'high', num = num)
    elif(guess<num):
        return render_template('number_game.html',res = 'low', num = num)
    else:
        return render_template('number_game.html',res = 'noinput', num = num)
    
# number game route
@app.route('/wheat_classifier')
def wheat_classifier():
    return render_template('classifier.html', prediction = 0)

# prediction route
@app.route('/wheat_classifier/predict', methods = ['POST'])
def prediction():
    if request.method == 'POST':
        area =  request.form['area']
        peri = request.form['peri']
        compact = request.form['compact']
        length = request.form['length']
        width = request.form['width']
        coeff = request.form['coeff']
        groove = request.form['groove']
        
        input_variables = pd.DataFrame([[area,peri,compact,length,width,coeff,groove]],
                                       columns=['Area','Perimeter','Compactness','KernelLength','KernelWidth','AsymmeteryCoeff','KernelGrooveLength'],
                                       dtype=float)
        
        prediction = model.predict(input_variables)[0]
        
        return render_template('classifier.html', prediction = prediction)


if __name__ == '__main__':
    app.run(debug=True)