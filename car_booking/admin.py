from flask import *
from werkzeug.security import generate_password_hash

from car_booking.db import get_db
from .auth import admin_required

#Admin Blueprint
bp = Blueprint('admin', __name__, url_prefix='/admin')


#home route
@bp.route('/home')
@admin_required
def home():
    db = get_db()
    user = db.execute(
        'SELECT * FROM user'
    ).fetchall()
    cars = db.execute(
        'SELECT * FROM vehicle'
    ).fetchall()
    testify = db.execute(
        'SELECT * FROM testimonial'
    ).fetchall()
    questions = db.execute(
        'SELECT * FROM queries'
    ).fetchall()
    book = db.execute(
        'SELECT * FROM booking'
    ).fetchall()
    book_no = len(book)
    num = len(user)
    num1 = len(cars)
    num2 = len(testify)
    num3 = len(questions)
    return render_template('admin/home.html', user=user, book=book_no, num=num, num1=num1, num2=num2, num3=num3)

#Admin registration route
@bp.route('register', methods=("GET", "POST"))
@admin_required
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
                        (email, generate_password_hash(password), "True", username, address, dob, security, answer),
                    )
                else:
                    db.execute(
                        "INSERT INTO user (email, password, isAdmin,username, address, img, mimetype, date_of_birth,"
                        "security_question, security_answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (email, generate_password_hash(password), "True", username, address, pic.read(), pic.mimetype,
                         dob, security, answer),
                    )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
        else:
            return redirect(url_for("admin.home"))

        flash(error)

    return render_template('auth/register.html')

#Brand creation route
@bp.route('/brand', methods=("GET", "POST"))
@admin_required
def create_brand():
    if request.method == "POST":
        db = get_db()
        name = request.form['name']
        db.execute("INSERT INTO brands (brand_name) VALUES (?)", (name,))
        db.commit()
        return redirect(url_for('admin.home'))
    return render_template('admin/car_brands.html')

#Car registry route
@bp.route('/add_car', methods=("GET", "POST"))
@admin_required
def car():
    db = get_db()
    brand = db.execute("SELECT * FROM brands").fetchall()
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        brands = request.form['brands']
        description = request.form['description']
        img = request.files['image']

        try:
            db.execute(
                "INSERT INTO vehicle (name, 'image', mimetype, rent_price, description, brands) VALUES (?, "
                "?, ?, ?, ?, ? )", (name, img.read(), img.mimetype, price, description, brands)
            )
            db.commit()
            return redirect(url_for("admin.home"))
        except:
            error = "Problem encountered"
        flash(error)
    return render_template('admin/create_car.html', brand=brand)

#Bookings route
@bp.route("/bookings")
@admin_required
def booking():
    db = get_db()
    book = db.execute(
        "SELECT * FROM booking as b JOIN vehicle AS v JOIN user AS u ON v.id = b.vehicle_id and u.id=b.user_id ORDER "
        "BY b.register DESC;"
    ).fetchall()
    return render_template("admin/cars.html", book=book)

#Car dashboard route
@bp.route("/car")
@admin_required
def cars():
    db = get_db()
    cars = db.execute(
        "SELECT * FROM vehicle"
    ).fetchall()
    brand = db.execute(
        "SELECT * FROM brands"
    ).fetchall()
    return render_template('admin/car.html', cars=cars, brand=brand)

#User dashboard route
@bp.route("/users")
@admin_required
def users():
    db = get_db()
    users = db.execute(
        "SELECT * FROM user"
    ).fetchall()
    return render_template("admin/users.html", users=users)

#Questions route
@bp.route("/queries")
@admin_required
def query():
    db = get_db()
    queries = db.execute(
        "SELECT * FROM queries"
    ).fetchall()
    return render_template('admin/queries.html', queries=queries)

#Testimonies route
@bp.route("/testimony")
@admin_required
def test():
    db = get_db()
    testimony = db.execute(
        "SELECT * FROM testimonial"
    ).fetchall()
    return render_template('admin/testify.html', testimonies=testimony)

#Brands dashboard route
@bp.route("/brands")
@admin_required
def brand():
    db = get_db()
    brands = db.execute(
        "SELECT * FROM brands"
    ).fetchall()
    return render_template("admin/brands.html", brands=brands)

#Brands update route
@bp.route("/brand/<int:ids>", methods=["GET", "POST"])
@admin_required
def update_brand(ids):
    db = get_db()
    brand = db.execute(
        "SELECT * FROM brands WHERE id = ?", (ids,)
    ).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        try:
            db.execute(
                "UPDATE brands SET brand_name = ? WHERE id = ?", (name, ids)
            )
            db.commit()
            return redirect(url_for('admin.home'))
        except:
            error = "Try again"
        flash(error)
    return render_template("update/brand_update.html", brand=brand)

#Delete Brands
@bp.route("/delete_brand/<int:id>")
@admin_required
def delete_brand(id):
    db = get_db()
    db.execute(
        "DELETE FROM brands WHERE id = ?", (id,)
    )
    db.commit()
    return redirect(url_for('admin/home'))

#Car Update route
@bp.route("/update car/<int:id>", methods=["GET", "POST"])
@admin_required
def update_car(id):
    db = get_db()
    car = db.execute(
        "SELECT * FROM vehicle WHERE id = ?", (id,)
    ).fetchone()
    brand = db.execute(
        "SELECT * FROM brands"
    ).fetchall()
    if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        brands = request.form['brands']
        description = request.form['description']
        print(name + " " + str(id) + " " + price + " " + brands + " " + description)
        try:
            db.execute(
                "UPDATE vehicle SET name= ?, rent_price= ?, brands = ?, description = ? WHERE id = ?",
                (name, int(price), brands, description, id)
            )
            db.commit()
            return redirect(url_for('admin.home'))
        except:
            error = "Try again"
        flash(error)
    return render_template("update/car_update.html", car=car, brand=brand)

#Delete car
@bp.route("/delete_car/<int:id>")
@admin_required
def delete_car(id):
    db = get_db()
    db.execute(
        "DELETE FROM vehicle WHERE id = ?", (id,)
    )
    db.commit()
    return redirect(url_for('admin.home'))

#Delete Queries
@bp.route("/deleteq/<int:id>")
@admin_required
def delete_q(id):
    db = get_db()
    db.execute(
        "DELETE FROM queries WHERE id = ?", (id,)
    )
    db.commit()
    return redirect(url_for("admin.query"))

#Booking confirmation
@bp.route("/confirm/<int:id>")
@admin_required
def confirm(id):
    db = get_db()
    db.execute(
        "UPDATE booking SET 'status' = 'Confirmed' WHERE id = ?", (id,)
    )
    db.commit()
    return redirect(url_for('admin.booking'))

#Booking Rejection
@bp.route("/reject/<int:id>")
@admin_required
def reject(id):
    db = get_db()
    db.execute(
        "UPDATE booking SET 'status' = 'Rejected' WHERE id = ?", (id,)
    )
    db.commit()
    return redirect(url_for('admin.booking'))
