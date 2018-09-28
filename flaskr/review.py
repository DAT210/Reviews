
import db

def set(id, review):
    database = db.get_db()
    cursor = database.cursor()
    try:
        sql = ""
    return

def get(id):
    database = db.get_db()
    cursor = database.cursor()
    try:
        sql = "SELECT review FROM reviews WHERE id=%s"
        cursor.execute(sql, (id,))
        review = cursor.fetchone()
        return review
    except pk as err:
        flash(err, category='error')
    finally:
        cursor.close()
    return