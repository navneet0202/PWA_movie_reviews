from flask import Flask, jsonify, request, render_template
import db
import sqlite3
import bcrypt

app = Flask(__name__)
db.init_db()


# Default route redirects to login page
@app.route("/")
def default_route():
    return render_template("all_reviews.html")


# Render the login page
@app.route("/login")
def login_page():
    return render_template("login.html")


# Render the signup page
@app.route("/signup")
def signup_page():
    return render_template("signup.html")


# Handle signup logic
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    password = data.get("password")
    email = data.get("email")

    if not name or not password:
        return jsonify({"error": "Name and password are required"}), 400

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    try:
        db.execute_query(
            "INSERT INTO users2 (email, name, password) VALUES (?, ?, ?)",
            (email, name, hashed_password),
        )
        return jsonify({"message": "Signup successful"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409


# Handle login logic
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    name = data.get("name")
    password = data.get("password")

    if not name or not password:
        return jsonify({"error": "Name and password are required"}), 400

    user = db.fetch_all("SELECT * FROM users2 WHERE name = ?", (name,))
    if not user:
        return jsonify({"error": "Invalid username or password"}), 401

    stored_password = user[0]["password"]
    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


@app.route("/add_review")
def add_review_page():
    return render_template("add_review.html")


@app.route("/submit_review", methods=["POST"])
def submit_review():
    data = request.json
    title = data.get("title")
    review_date = data.get("review_date")
    user_name = data.get("user_name")
    rating = data.get("rating")
    review_text = data.get("review_text")

    if not title or not review_date or not user_name or not rating or not review_text:
        return jsonify({"error": "All fields are required"}), 400

    try:
        db.execute_query(
            """
            INSERT INTO reviews (title, review_date, user_name, rating, review_text)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, review_date, user_name, rating, review_text),
        )
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/all_reviews")
def see_all_reviews():
    return render_template("all_reviews.html")


@app.route("/reviews", methods=["GET"])
def get_all_reviews():
    reviews = db.fetch_all("SELECT * FROM reviews")
    return jsonify([dict(row) for row in reviews])  # Converts rows to dictionaries


# Fetch a specific review by ID
@app.route("/review/<int:review_id>", methods=["GET"])
def get_review(review_id):
    try:
        review = db.fetch_all("SELECT * FROM reviews WHERE id = ?", (review_id,))
        if review:
            return jsonify(dict(review[0]))  # Convert the single row to a dictionary
        else:
            return jsonify({"error": "Review not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update a review
@app.route("/edit_review/<int:review_id>", methods=["PUT"])
def edit_review(review_id):
    data = request.json
    new_title = data.get("title")
    new_review_date = data.get("review_date")
    new_rating = data.get("rating")
    new_review_text = data.get("review_text")
    user_name = data.get("user_name")  # To verify user identity

    if not new_title or not new_review_date or not new_rating or not new_review_text:
        return jsonify({"error": "All fields are required"}), 400

    # Verify the review belongs to the logged-in user
    review = db.fetch_all("SELECT * FROM reviews WHERE id = ?", (review_id,))
    if not review or review[0]["user_name"] != user_name:
        return jsonify({"error": "Unauthorized action"}), 403

    try:
        db.execute_query(
            """
            UPDATE reviews
            SET title = ?, review_date = ?, rating = ?, review_text = ?
            WHERE id = ?
            """,
            (new_title, new_review_date, new_rating, new_review_text, review_id),
        )
        return jsonify({"message": "Review updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete a review
@app.route("/delete_review/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    data = request.json
    user_name = data.get("user_name")  # To verify user identity

    # Verify the review belongs to the logged-in user
    review = db.fetch_all("SELECT * FROM reviews WHERE id = ?", (review_id,))
    if not review or review[0]["user_name"] != user_name:
        return jsonify({"error": "Unauthorized action"}), 403

    try:
        db.execute_query("DELETE FROM reviews WHERE id = ?", (review_id,))
        return jsonify({"message": "Review deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
