from app import app
from flask import render_template, url_for, redirect, flash
from app.forms import UserInfoForm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        return redirect(url_for('index'))   
    flash('That username is already taken, please try again.')
    return render_template('register.html', form=register_form)