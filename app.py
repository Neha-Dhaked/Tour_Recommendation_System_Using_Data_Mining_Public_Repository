
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, request
import pandas as pd
import mysql.connector
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import secrets
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from transformers import pipeline
import requests
from popular import popular_bp
from utils.save_popular_locations import save_locations_to_db
from utils.monument_identifier import identify_monument, load_monument_data, get_similar_places
from identify import identify_bp






# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Register the blueprint
app.register_blueprint(popular_bp)

app.register_blueprint(identify_bp)



# Database Connection
def db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="newtrs2"
    )

db = db_connection()
cursor = db.cursor(buffered=True)

# Load and Preprocess Tour Data
tour_data = pd.read_csv("rawTourData.csv").fillna("")
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(tour_data["description"])

# Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_verification_email(email, token):
    verify_link = f"http://localhost:5000/verify_email?token={token}"
    subject = "Verify Your Email"
    message = f"Hello,\n\nPlease click the link below to verify your email:\n{verify_link}\n\nIf you did not request this, please ignore this email."

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, email, msg.as_string())
        server.quit()
        print(f" Verification email sent to {email}")
    except Exception as e:
        print(f" Email Error: {e}")


# ========== ROUTES ==========
@app.route("/")
def home():
    return render_template("home.html", logged_in=('user_id' in session))

# ======================== REGISTER ROUTE ========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        profile = request.form["profile"]

        # Email validation
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            flash("Invalid email format", "danger")
            return redirect(url_for("register"))

        # Password validation
        password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(password_regex, password):
            flash("Password must have at least 8 characters, including uppercase, lowercase, numbers, and special characters.", "danger")
            return redirect(url_for("register"))

        # Confirm password check
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("register"))

        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            flash("Email already registered", "danger")
            return redirect(url_for("register"))

        # Generate a verification token
        verification_token = secrets.token_hex(16)

        try:
            # Insert user into database with verification token
            cursor.execute(
                "INSERT INTO users (username, email, password, profile, is_verified, verification_token) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, email, password, profile, 0, verification_token)
            )
            db.commit()

            # Send verification email
            send_verification_email(email, verification_token)

            flash("Registration successful! Check your email to verify your account.", "info")
            return redirect(url_for("login"))

        except mysql.connector.Error as err:
            print(f" MySQL Error: {err}")
            db.rollback()
    
    return render_template("register.html")


@app.route("/verify_email")
def verify_email():
    token = request.args.get("token")

    if not token:
        flash("Invalid verification link.", "danger")
        return redirect(url_for("login"))

    cursor.execute("SELECT id FROM users WHERE verification_token=%s", (token,))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET is_verified=1, verification_token=NULL WHERE id=%s", (user[0],))
        db.commit()
        flash("Email verified successfully! You can now log in.", "success")
        return redirect(url_for("login"))

    flash("Invalid or expired token.", "danger")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("SELECT id, is_verified FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            if user[1] == 0:  # Check if user is verified
                flash("Please verify your email before logging in.", "warning")
                return redirect(url_for("login"))

            session["user_id"] = user[0]
            return redirect(url_for("home"))

        flash("Invalid email or password", "danger")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")


# Profile route
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    cursor.execute("SELECT username, email, profile FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if not user:  # If no user data is found, handle it properly
        return render_template("profile.html", user=None)

    return render_template("profile.html", user=user)


# ========== SEARCH FUNCTIONALITY ==========
def search_tours(user_query, top_n=15):
    user_query_vector = vectorizer.transform([user_query])
    cosine_sim = cosine_similarity(user_query_vector, tfidf_matrix)
    sim_scores = sorted(enumerate(cosine_sim[0]), key=lambda x: x[1], reverse=True)
    top_tour_indices = [i[0] for i in sim_scores[:top_n]]
    return tour_data.iloc[top_tour_indices][['tour_name', 'location', 'tour_type', 'description', 'best_time']].to_dict(orient='records')

# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         query = request.form.get('query')
#         user_id = session['user_id']
#         search_date = datetime.now()
#         recommendations = search_tours(query)
#         session['recommendations'] = recommendations
#         #Save search in DB
#         if 'user_id' in session:
#             cursor.execute(
#                 "INSERT INTO search_history (user_id, search_string, tours_viewed, search_date) VALUES (%s, %s, %s, %s)",
#                 (user_id, query, None, search_date)
#             )
#             cursor.execute(
#                 "INSERT INTO user_search (user_id, search_query) VALUES (%s, %s)",
#                 (user_id, query)
#             )

#             # Commit changes to database
#             db.commit()
#         return render_template('search.html', recommendations=recommendations)
#     return render_template('search.html', recommendations=[])



@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        search_date = datetime.now()
        recommendations = search_tours(query)
        session['recommendations'] = recommendations

        # Check if user is logged in before accessing 'user_id'
        user_id = session.get('user_id')  # Use session.get() to avoid KeyError

        if user_id:  # Only save search history if the user is logged in
            cursor.execute(
                "INSERT INTO search_history (user_id, search_string, tours_viewed, search_date) VALUES (%s, %s, %s, %s)",
                (user_id, query, None, search_date)
            )
            cursor.execute(
                "INSERT INTO user_search (user_id, search_query) VALUES (%s, %s)",
                (user_id, query)
            )

            # Commit changes to database
            db.commit()

        return render_template('search.html', recommendations=recommendations)

    return render_template('search.html', recommendations=[])




@app.route("/search_history")
def search_history():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    cursor.execute("SELECT search_string, search_date FROM search_history WHERE user_id=%s", (user_id,))
    history = cursor.fetchall()

    return render_template("search_history.html", history=history, enumerate=enumerate)





@app.route("/my_recommendations")
def my_recommendations():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Fetch search history
    cursor.execute("SELECT search_string FROM search_history WHERE user_id=%s", (user_id,))
    searches = [row[0] for row in cursor.fetchall()]

    if not searches:
        return render_template("my_recommendations.html", recommendations=[])

    # Get most recent search term
    search_query = searches[-1]

    # Get recommendations using the search_tours function
    recommendations = search_tours(search_query)

    return render_template("my_recommendations.html", recommendations=recommendations)

# ========== FEEDBACK ==========
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        feedback_text = request.form["feedback"]
        if "user_id" in session:
            cursor.execute("INSERT INTO feedback (user_id, feedback_text) VALUES (%s, %s)", (session["user_id"], feedback_text))
            db.commit()
        return redirect(url_for("home"))
    return render_template("feedback.html")

#  Chatbot API (Fixed)
@app.route("/chat", methods=["POST"])
def chatbot():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please enter a message!"})

    chatbot_url = "http://127.0.0.1:5001/chat"  #  Ensure chatbot.py is running

    try:
        chatbot_response = requests.post(chatbot_url, json={"message": user_message})

        if chatbot_response.status_code == 200:
            return chatbot_response.json()
        else:
            return jsonify({"reply": "Chatbot is currently unavailable. Try again later."})

    except requests.exceptions.RequestException as e:
        print("Error connecting to chatbot:", e)
        return jsonify({"reply": "Error: Could not connect to the chatbot service."})
    



# def save_locations_to_db(locations):
#     conn = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='yourpassword',
#         database='yourdbname'
#     )
#     cursor = conn.cursor()
#     for loc in locations:
#         query = "INSERT INTO tourism_locations (name, lat, lon) VALUES (%s, %s, %s)"
#         cursor.execute(query, (loc['name'], loc['lat'], loc['lon']))
#     conn.commit()
#     cursor.close()
#     conn.close()



@app.route("/identify", methods=["POST"])
def identify():
    file = request.files["image"]
    if file:
        filepath = os.path.join("static/uploads", file.filename)
        file.save(filepath)

        place_name = identify_monument(filepath)
        monument_data = load_monument_data()
        monument_info = monument_data.get(place_name, {})

        similar_places = get_similar_places(place_name)

        return render_template("identify_result.html",
                               place_name=place_name,
                               monument=monument_info,
                               similar_places=similar_places)
    else:
        return "No image uploaded", 400




#  Start Flask App
if __name__ == "__main__":
    app.run(debug=True, port=5000)
