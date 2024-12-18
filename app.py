from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_rolls(sort=None):
    conn = sqlite3.connect('rolls.db')
    cursor = conn.cursor()

    query = "SELECT name, ingredients, weight, image_url, price FROM rolls"
    params = []

    if sort:
        if sort == "weight_asc":
            query += " ORDER BY CAST(weight AS INTEGER) ASC"
        elif sort == "weight_desc":
            query += " ORDER BY CAST(weight AS INTEGER) DESC"
        elif sort == "ingredient_los":
            query += " WHERE ingredients LIKE ?"
            params.append("%лосось%")
        elif sort == "ingredient_tun":
            query += " WHERE ingredients LIKE ?"
            params.append("%тунец%")
        elif sort == "ingredient_krev":
            query += " WHERE ingredients LIKE ?"
            params.append("%креветки%")

    cursor.execute(query, params)
    rolls = [{'name': row[0], 'ingredients': row[1], 'weight': row[2], 'image_url': row[3], 'price': row[4]} for row in cursor.fetchall()]
    conn.close()

    return rolls

@app.route("/", methods=["GET", "POST"])
def index():
    sort = request.args.get("sort")
    rolls = get_rolls(sort)
    no_rolls_message = None
    if sort and not rolls:
        no_rolls_message = "Нет роллов с выбранным продуктом."

    return render_template("index.html", rolls=rolls, sort=sort, no_rolls_message=no_rolls_message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

