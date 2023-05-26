from flask import Flask, render_template
import re
import openai
import json
from markupsafe import Markup
from jinja2 import Environment
from datetime import datetime
import numpy as np


app = Flask(__name__)
# Do not include any explanations, only provide a  RFC8259 compliant JSON response  following this format without deviation.


@app.template_filter('nl2br')
def nl2br(value):
    if value is None:
        return value
    return Markup(value.replace('\n', '<br>'))


env = Environment()
env.filters['nl2br'] = nl2br



@app.route('/')
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