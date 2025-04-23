from flask import *

from .db import get_db
from .auth import login_required
#for image display
bp = Blueprint('img', __name__, url_prefix='/img')

#Users Images
@bp.route("/user/<int:id>")
@login_required
def user(id):
    db = get_db()
    try:
        image = db.execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()
        if image['img'] is not None:
            return Response(image['img'], mimetype=image['mimetype'])
    except TypeError:
        return "NOT available"
    return "no image"

#Car images
@bp.route('/cars/<int:car_id>')
def cars(car_id):
    db = get_db()
    try:
        image = db.execute(
            'SELECT * FROM vehicle WHERE id = ?', (car_id,)
        ).fetchone()
        if image['image'] is not None:
            return Response(image['image'], mimetype=image['mimetype'])
    except TypeError:
        return "NOT available"
    return "No image"
