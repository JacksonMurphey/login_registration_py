from LOG_REG_app import app
from flask import redirect, render_template, request, session, flash
from LOG_REG_app.models.user import User
from flask_bcrypt import Bcrypt 


bcrypt = Bcrypt(app)

# NOTE: this needs to be updated, routes

# initial page for user registration and login. 
@app.route('/')
def dashboard():
    return render_template('login_registration.html')



@app.route('/user/register', methods=['POST'])
def register_user():

    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }
    user_id = User.save(data)
    session['user_id'] = user_id    #this returns a number
    return redirect('/user/dashboard')


@app.route('/user/login', methods=['POST'])
def login_user():
    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        'email' :  request.form['email']
    }
    user = User.get_one_by_email(data)
    session['user_id'] = user.id    #this returns an object, id is red likely b/c it has no value till we run the above line. 
    return redirect('/user/dashboard')



##################### ONLY LOGGED IN USER'S ROUTES BELOW ###############

@app.route('/user/dashboard')
def dash_user():
    if not 'user_id' in session: # can now put this on any controller after they have logged in. BETTER PLACE TO PUT IS IN VALIDATION CHECKS
        flash('Must be logged in')
        return redirect('/')
    # if User.login_check('user_id'):
    #     return redirect('/')

    data = {'id': session['user_id']}
    user = User.get_one_user(data)
    
    return render_template('user_dash.html', user=user)


@app.route('/user/logout')
def logout_user():
    session.pop('user_id')
    return redirect('/')