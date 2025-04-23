import functools

from flask import *
from werkzeug.security import check_password_hash, generate_password_hash
from car_booking.db import get_db

#Authentication
bp = Blueprint('auth', __name__, url_prefix='/auth')

#Registration route
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        dob = request.form['dob']
        security = request.form['sec_que']
        answer = request.form['answer']
        pic = request.files['profile']

        db = get_db()
        error = None

        if not email:
            error = 'email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                if pic is None:
                    db.execute(
                        "INSERT INTO user (email, password, isAdmin,username, 'address', 'date_of_birth',"
                        "'security_question', 'security_answer') VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (email, generate_password_hash(password), "False", username, address, dob, security, answer),
                    )
                else:
                    db.execute(
                        "INSERT INTO user (email, password, isAdmin,username, address, img, mimetype, date_of_birth,"
                        "security_question, security_answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (email, generate_password_hash(password), "False", username, address, pic.read(), pic.mimetype,
                         dob, security, answer),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

#Sign in route
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'+user['password']

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            # if user['isAdmin'] == 'True':
            #     return redirect(url_for('admin.home'))
            return redirect(url_for('user.index'))

        flash(error)

    return render_template('auth/login.html')

#get user data on log in
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

#logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#confirm to change password
@bp.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form['email']
        answer = request.form['answer']
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE email =?", (email,)
        ).fetchone()
        if user:
            if user['security_answer'] == answer:
                g.user = user
                return redirect(url_for("user.new"))
            else:
                error = "Wrong Answer, Please try again"
        else:
            error = "No such user"
        flash(error)
    return render_template("auth/forgot.html")

#confirm user logged in
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view

#Confirm Admin logged in
def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user['isAdmin'] != "True":
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
