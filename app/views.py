from flask import render_template, request
from app import app
from model import *

@app.route('/')
def form():
    return render_template("form.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    output = predict(text)
    return render_template('form.html', message=output)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/model')
def model():
    return render_template("model.html")