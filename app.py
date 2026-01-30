from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///recipes.db")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def dash():
    
    return render_template("home.html")




@app.route("/home")
@login_required
def index():
    
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    username = user[0]["username"]
    recipes = db.execute("SELECT recipes.*, users.username FROM recipes JOIN users ON recipes.user_id = users.id ORDER BY recipes.id DESC")
    return render_template("index.html", recipes=recipes, username=username)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("Must provide username")
            return render_template("register.html")
        elif not password:
            flash("Must provide password")
            return render_template("register.html")
        elif password != confirmation:
            flash("Passwords must match")
            return render_template("register.html")

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        except:
            flash("Username already exists")
            return render_template("register.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        flash("Registered!")
        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Must provide username and password")
            return render_template("login.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Invalid username and/or password")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]
        flash("Logged in!")
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    recipe = db.execute("SELECT recipes.*, users.username FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = ?", recipe_id)
    if not recipe:
        return redirect("/")
    
    ingredients = db.execute("SELECT * FROM ingredients WHERE recipe_id = ?", recipe_id)
    instructions = db.execute("SELECT * FROM instructions WHERE recipe_id = ? ORDER BY step_number", recipe_id)
    
    return render_template("recipe.html", recipe=recipe[0], ingredients=ingredients, instructions=instructions)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        prep_time = request.form.get("prep_time")
        cook_time = request.form.get("cook_time")
        servings = request.form.get("servings")

        if not title:
            flash("Must provide title")
            return redirect("/add")

        recipe_id = db.execute("INSERT INTO recipes (user_id, title, description, prep_time, cook_time, servings) VALUES (?, ?, ?, ?, ?, ?)",
                              session["user_id"], title, description, prep_time, cook_time, servings)

        ingredients = request.form.getlist("ingredient_name")
        amounts = request.form.getlist("ingredient_amount")
        for name, amount in zip(ingredients, amounts):
            if name and amount:
                db.execute("INSERT INTO ingredients (recipe_id, name, amount) VALUES (?, ?, ?)", recipe_id, name, amount)

        instructions = request.form.getlist("instruction")
        for i, text in enumerate(instructions, 1):
            if text:
                db.execute("INSERT INTO instructions (recipe_id, step_number, text) VALUES (?, ?, ?)", recipe_id, i, text)

        flash("Recipe added!")
        return redirect(f"/recipe/{recipe_id}")

    return render_template("add.html")


@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def edit(recipe_id):
    recipe = db.execute("SELECT * FROM recipes WHERE id = ? AND user_id = ?", recipe_id, session["user_id"])
    if not recipe:
        return redirect("/")
    
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        prep_time = request.form.get("prep_time")
        cook_time = request.form.get("cook_time")
        servings = request.form.get("servings")

        db.execute("UPDATE recipes SET title = ?, description = ?, prep_time = ?, cook_time = ?, servings = ? WHERE id = ?",
                  title, description, prep_time, cook_time, servings, recipe_id)

        db.execute("DELETE FROM ingredients WHERE recipe_id = ?", recipe_id)
        db.execute("DELETE FROM instructions WHERE recipe_id = ?", recipe_id)

        ingredients = request.form.getlist("ingredient_name")
        amounts = request.form.getlist("ingredient_amount")
        for name, amount in zip(ingredients, amounts):
            if name and amount:
                db.execute("INSERT INTO ingredients (recipe_id, name, amount) VALUES (?, ?, ?)", recipe_id, name, amount)

        instructions = request.form.getlist("instruction")
        for i, text in enumerate(instructions, 1):
            if text:
                db.execute("INSERT INTO instructions (recipe_id, step_number, text) VALUES (?, ?, ?)", recipe_id, i, text)

        flash("Recipe updated!")
        return redirect(f"/recipe/{recipe_id}")

    ingredients = db.execute("SELECT * FROM ingredients WHERE recipe_id = ?", recipe_id)
    instructions = db.execute("SELECT * FROM instructions WHERE recipe_id = ? ORDER BY step_number", recipe_id)
    return render_template("edit.html", recipe=recipe[0], ingredients=ingredients, instructions=instructions)


@app.route("/delete/<int:recipe_id>", methods=["GET","POST"])
@login_required
def delete(recipe_id):
    db.execute("DELETE FROM recipes WHERE id = ? AND user_id = ?", recipe_id, session["user_id"])
    flash("Recipe deleted!")
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)