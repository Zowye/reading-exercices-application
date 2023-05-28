import logging
from flask import Flask, render_template
import re
#import openai
import json
from markupsafe import Markup
from jinja2 import Environment
from datetime import datetime
import numpy as np
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3



app = Flask(__name__)
# Do not include any explanations, only provide a  RFC8259 compliant JSON response  following this format without deviation.

# Configuração do logging
# logging.basicConfig(filename='app.log', level=logging.INFO)

@app.template_filter('nl2br')
def nl2br(value):
    if value is None:
        return value
    return Markup(value.replace('\n', '<br>'))


env = Environment()
env.filters['nl2br'] = nl2br


app.secret_key = 'sua_chave_secreta'


# Rota inicial
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/get_random_text')
def get_random_text():
    file_path = "data.json"
    # Abre o  no .json
    with open(file_path, "r") as json_file:
        data = json.load(json_file)

    # Gets a random Text
    LEN = len(data['lista_treinos'])
    RANDOM_ID = np.random.randint(LEN)
    data = data['lista_treinos'][RANDOM_ID]
    return data



# Rota inicial
@app.route('/')
def home():
    return render_template('index.html')

# Rota de cadastro de usuário
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('readingapp.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('readingapp.db')
        cursor = conn.cursor()
        print(username, password)
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()

        print(user)
        conn.close()
        if user:
            session['username'] = user[1]
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')








def isAuth():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect('readingapp.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return True, user
    else:
        return False, 0



# Rota de perfil do usuário
@app.route('/profile')
def profile():
    isauth, userInfo = isAuth()
    
    if isauth:
        return render_template('hello_user.html', user=userInfo)
    
    return redirect(url_for('login'))




# Rota de logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))















# __________________________________________________________________
# _________________________________________________ EXERCICES ROUTES



@app.route('/blurred')
def blurred():
         
    file_path = "data.json"
    # Abre o  no .json
    with open(file_path, "r") as json_file:
        data = json.load(json_file)


    # Gets a random Text
    LEN = len(data['lista_treinos'])
    RANDOM_ID = np.random.randint(LEN)
    data = data['lista_treinos'][RANDOM_ID]

    return render_template("lineBlur.html", info_dict=data)



@app.route('/centralized')
def display_page():
    file_path = "data.json"
    # Abre o  no .json
    with open(file_path, "r") as json_file:
        data = json.load(json_file)


    # Gets a random Text
    LEN = len(data['lista_treinos'])
    RANDOM_ID = np.random.randint(LEN)
    data = data['lista_treinos'][RANDOM_ID]

    return render_template("centralized.html", info_dict=data)



@app.route('/reading')
def index():


    max_tentativas = 5  # Número máximo de tentativas
    tentativas = 0
    sucesso = False

            
    file_path = "data.json"
    # Abre o  no .json
    with open(file_path, "r") as json_file:
        data = json.load(json_file)


    # Gets a random Text
    LEN = len(data['lista_treinos'])
    RANDOM_ID = np.random.randint(LEN)
    data = data['lista_treinos'][RANDOM_ID]


    return render_template("result2.html", info_dict=data)


if __name__ == '__main__':
    app.run()
