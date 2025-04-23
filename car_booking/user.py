from flask import *

from car_booking.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from .auth import login_required
#Main Blueprint
bp = Blueprint('user', __name__)

#Home route
@bp.route("/")
def index():
    if g.user:
        return render_template("user/home.html")
    return render_template('user/guest.html')

#Car route
@bp.route("/product")
@login_required
def product():
    db = get_db()
    cars = db.execute(
        "SELECT * FROM vehicle"
    ).fetchall()
    brand = db.execute(
        "SELECT * FROM brands"
    ).fetchall()
    return render_template('user/product.html', cars=cars, brand=brand)

#Testimony Route
@bp.route("/testimonial", methods=["GET", "POST"])
def testify():
    if request.method == "POST":
        db = get_db()
        name = request.form['name']
        body = request.form['body']
        db.execute(
            "INSERT INTO testimonial (name, body) VALUES (?, ?)", (name, body)
        )
        db.commit()
        return redirect(url_for('user.index'))
    return render_template("user/testimonials.html")

#Contact us route
@bp.route("/contact", methods=("POST", "GET"))
def contact():
    if request.method == "POST":
        name = request.form['name']
        subject = request.form['subject']
        body = request.form['body']
        db = get_db()
        db.execute(
            "INSERT INTO queries (name, subject, message) VALUES (?, ?, ?)", (name, subject, body)
        )
        db.commit()
        return render_template('user/contact.html')
    return render_template('user/contact.html')

#View Profile
@bp.route("/profile")
@login_required
def profile():
    user = g.user
    return render_template('user/profile.html', user=user)

#Update profile
@bp.route("/update", methods=["GET", "POST"])
@login_required
def update():
    user = g.user
    if request.method == "POST":
        id = g.user['id']
        username = request.form['username']
        email = request.form['email']
        address = request.form['address']
        dob = request.form['dob']
        pic = request.files['profile']
        db = get_db()
        try:
            if pic is not None:
                db.execute(
                    "UPDATE user SET username= ?, email= ?, address= ?, date_of_birth= ?, img= ?, mimetype= ? WHERE "
                    "id = ? ",
                    (username, email, address, dob, pic.read(), pic.mimetype, id)
                )
                db.commit()
            else:
                db.execute(
                    "UPDATE user SET username= ?, email= ?, address= ?, date_of_birth= ? WHERE id = ? ",
                    (username, email, address, dob, id)
                )
                db.commit()
            return redirect(url_for("user.index"))
        except:
            error = "Could not finish transaction"
        if error is not None:
            flash(error)
        return render_template("update/profile_update.html", user=user)
    return render_template("update/profile_update.html", user=user)

#Profile image
@bp.route("/<int:id>")
@login_required
def img(id):
    db = get_db()
    try:
        image = db.execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()
        if image['img'] is not None:
            return Response(image['img'], mimetype=image['mimetype'])
    except TypeError:
        return "NOT available"
    return "No image"

#Delete User
@bp.route("/delete", methods=("POST",))
@login_required
def delete_user():
    db = get_db()
    id = g.user['id']
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for("auth.logout"))

#Change password
@bp.route("/password", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        db = get_db()
        password = request.form['password']
        new = request.form['new']
        confirm = request.form['confirm']

        if check_password_hash(g.user['password'], password):
            if new == confirm:
                db.execute(
                    "Update user SET password = ? WHERE id = ?",
                    (generate_password_hash(new), g.user['id'])
                )
                db.commit()
                return redirect(url_for("user.index"))
            else:
                error = "Password and confirm must be the same"
        else:
            error = "Password is incorrect"
        flash(error)
        return render_template('auth/password.html')
    return render_template("auth/password.html")

#New Password
@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "POST":
        db = get_db()
        new = request.form['new']
        confirm = request.form['confirm']
        if new == confirm:
            db.execute(
                "Update user SET password = ? WHERE id = ?",
                (generate_password_hash(new), g.user['id'])
            )
            db.commit()
            return redirect(url_for("user.index"))
        else:
            error = "Password and confirm must be the same"
        flash(error)
        return render_template('auth/new.html')
    return render_template("auth/new.html")

#Car details route
@bp.route("/book/<int:car>", methods=["GET", "POST"])
@login_required
def booking(car):
    db = get_db()
    cars = db.execute(
        "SELECT * FROM vehicle WHERE id = ?", (car,)
    ).fetchone()
    if request.method == "POST":
        id = g.user['id']
        car_id = car
        date = request.form['date']
        try:
            db.execute(
                "INSERT INTO booking (user_id, vehicle_id, date_use, 'status') VALUES (?, ?, ?, ?)",
                (id, car_id, date, "Waiting")
            )
            db.commit()
            return redirect(url_for('user.index'))
        except:
            error = "Sorry try again"
        flash(error)
    return render_template("user/details.html", cars=cars)

#Booked car route
@bp.route("/list")
@login_required
def list():
    db = get_db()
    book = db.execute(
        "SELECT * FROM vehicle v JOIN booking b ON v.id = b.vehicle_id WHERE b.user_id = ? ORDER BY b.register DESC",
        (g.user['id'],)
    ).fetchall()
    return render_template("user/Booked.html", book=book)

#Testimony
@bp.route("/testimonies/<int:id>", methods=["GET", "POST"])
@login_required
def update_test(id):
    db = get_db()
    test = db.execute(
        "SELECT * FROM testimonial WHERE id = ?",
        (id,)
    ).fetchone()
    return render_template("update/testimonial_update.html", test=test)
