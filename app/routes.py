from app import app, db
from flask import render_template, url_for, redirect, flash
from app.forms import UserInfoForm, LoginForm
from app.models import User, Products
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
def index():
    title='Home'
    product = Products.query.all()
    return render_template('index.html', title=title, product=product)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = UserInfoForm()
    if register_form.validate_on_submit():
        print()
        # Grab Data from form
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        # print(username, email, password)
        
        # check if username from the form  already exists in the User table
        existing_user = User.query.filter_by(username=username).all()
        # If there is a user with that username message them asking to try again
        if existing_user:
            # Flash a warning message
            flash(f'The username {username} is already in use. Please try again.', 'danger')
            # Redirect back to the register page
            return redirect(url_for('register'))

        # Create a new user instance
        new_user = User(username, email, password)
        print(new_user)
        # Add that user to the database
        db.session.add(new_user)
        db.session.commit()
        # Flash a success message thanking them for signing up
        flash(f'Thank you {username}, enjoy your shopping experience!', 'success')

        return redirect(url_for('view_products'))

    return render_template('register.html', form=register_form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Grab data from form
        username = form.username.data
        password = form.password.data
        
        # Query our user table for a user with a username
        user = User.query.filter_by(username=username).first()

        # Check if the user is None or if password is incorrect
        if user is None or not user.check_password(password):
            flash('Your username or password is incorrect', 'danger')
            return redirect(url_for('login'))

        login_user(user)

        flash(f'Welcome {user.username}. You have successfully logged in.', 'success')

        return redirect(url_for('view_products'))

    return render_template('login.html', login_form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/products')
def view_products():
    product = Products.query.all()
    title='Products'
    return render_template('products.html', title=title, product=product)


@app.route('/Angel Hair')
def angel_hair():
    return render_template('angelhair.html')

@app.route('/Penne')
def penne():
    return render_template('penne.html')

@app.route('/Rigatoni')
def rigatoni():
    return render_template('rigatoni.html')

@app.route('/Campanelle')
def campanelle():
    return render_template('campanelle.html')

@app.route('/Marinara')
def marinara():
    return render_template('marinara.html')

@app.route('/Vodka Sauce')
def vodka_sauce():
    return render_template('vodka_sauce.html')


@app.route('/my-cart')
@login_required
def my_cart():
    my_products = current_user.product
    return render_template('my_cart.html', product= my_products)

@app.route('/add-to-cart/<prod_id>')
@login_required
def add_to_cart(prod_id):
    product = Products.query.get_or_404(prod_id)
    current_user.products.append(product)
    db.session.commit()
    return redirect(url_for('my_cart'))

# @app.route('/cart', methods=['GET', 'POST'])
# def my_cart():
#     product = MyCart.query.all()
#     # newcart = MyCart(MyCart.name, MyCart.price, user_id=1)
#     # db.session.add(newcart)
#     # db.session.commit()
#     return render_template('my_cart.html',product=product)

