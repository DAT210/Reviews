
import reviews.db as db

def set(id, review):
    if 1 > review or review > 5:
        return
    database = db.get_db()
    cursor = database.cursor()
    try:
        sql = "SELECT score, nr_of_reviews FROM reviews WHERE meal_id=%s"
        cursor.execute(sql, (id,))
        (score, nr_of_reviews) = cursor.fetchone()
        score += review
        nr_of_reviews += 1
        review = round((score/nr_of_reviews), 1)
        sql = "UPDATE reviews SET review=%s, score=%s, nr_of_reviews=%s WHERE meal_id=%s"
        cursor.execute(sql, (review, score, nr_of_reviews, id,))
        database.commit()
    except db.mysql.connector.Error as err:
        print(f"Error_set: {err}")
    finally:
        cursor.close()
    return

def get(id):
    database = db.get_db()
    cursor = database.cursor()
    try:
        sql = "SELECT review FROM reviews WHERE meal_id=%s"
        cursor.execute(sql, (id,))
        (review,) = cursor.fetchone()
        return review
    except db.mysql.connector.Error as err:
        print(f"Error_get: {err}")
    finally:
        cursor.close()
    return

class MealReview():
    __single_instance

    def __init__(self):
        if __single_instance is None:
            __single_instance = self

    def set(id, review):
        return NotImplementedError

    def get(id):
        return NotImplementedError

class ResturantReview():

    def __init__(self):

    def set(id, review):
        return NotImplementedError

    def get(id):
        return NotImplementedError