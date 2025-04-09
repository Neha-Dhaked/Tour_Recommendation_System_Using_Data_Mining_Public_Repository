# from flask import Flask, render_template, request, redirect, url_for, session
# import pandas as pd
# import mysql.connector
# from db_config import db_connection

# app = Flask(__name__)
# app.secret_key = 'secretkey'  # For session management

# # Database connection
# conn = db_connection()
# cursor = conn.cursor()

# # Home route
# @app.route('/')
# def home():
#     logged_in = 'user_id' in session
#     return render_template('home.html', logged_in=logged_in)

# # Registration route
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         profile = request.form['profile']

#         cursor.execute("INSERT INTO users (username, email, password, profile) VALUES (%s, %s, %s, %s)",
#                        (username, email, password, profile))
#         conn.commit()
#         return redirect(url_for('home'))

#     return render_template('register.html')

# # Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         cursor.execute("SELECT id FROM users WHERE email = %s AND password = %s", (email, password))
#         user = cursor.fetchone()
#         if user:
#             session['user_id'] = user[0]
#             return redirect(url_for('home'))
#         else:
#             return "Invalid credentials!"

#     return render_template('login.html')

# # Logout route
# @app.route('/logout')
# def logout():
#     session.pop('user_id', None)
#     return redirect(url_for('home'))

# # Profile route

# # @app.route('/profile')
# # def profile():
# #     if 'user_id' in session:
# #         cursor.execute("SELECT username, email, profile FROM users WHERE id = %s", (session['user_id'],))
# #         user_data = cursor.fetchone()
# #         return render_template('profile.html', user=user_data)
# #     return redirect(url_for('login'))
# @app.route('/profile')
# def profile():
#     if 'user_id' in session:
#         cursor.execute("SELECT username, email, profile FROM users WHERE id = %s", (session['user_id'],))
#         user_data = cursor.fetchone()
#         if user_data:
#             return render_template('profile.html', user=user_data)
#         else:
#             return "User not found!"
#     return redirect(url_for('login'))


# # Search route
# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     recommendations = []
#     if request.method == 'POST':
#         search_query = request.form['query']

#         # Save search in DB
#         if 'user_id' in session:
#             cursor.execute("INSERT INTO user_search (user_id, search_query) VALUES (%s, %s)",
#                            (session['user_id'], search_query))
#             conn.commit()

#         # Fetch recommendations
#         tours = pd.read_csv('rawTourData.csv')
#         recommendations = tours[tours['description'].str.contains(search_query, case=False)].to_dict('records')

#     return render_template('search.html', recommendations=recommendations)

# # Feedback route
# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback():
#     if request.method == 'POST':
#         feedback_text = request.form['feedback']

#         if 'user_id' in session:
#             cursor.execute("INSERT INTO feedback (user_id, feedback_text) VALUES (%s, %s)",
#                            (session['user_id'], feedback_text))
#             conn.commit()
#         return redirect(url_for('home'))

#     return render_template('feedback.html')

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
import pandas as pd
from datetime import datetime
from db_config import db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
# conn = db_connection()
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="newtrs"
# )

# cursor = db.cursor()
db = db_connection()
cursor = db.cursor()


# Home route
@app.route("/")
def home():
    logged_in = 'user_id' in session
    return render_template("home.html", logged_in=logged_in)

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        profile = request.form['profile']
        cursor.execute("INSERT INTO users (username, email, password, profile) VALUES (%s, %s, %s, %s)", 
                       (username, email, password, profile))
        db.commit()
        return redirect("/login")
    return render_template("register.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        if user:
            session['user_id'] = user[0]
            return redirect("/")
    return render_template("login.html")

# Logout route
@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return redirect("/")

# Profile route
@app.route("/profile")
def profile():
    if 'user_id' not in session:
        return redirect("/login")
    user_id = session['user_id']
    cursor.execute("SELECT username, email, profile FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    return render_template("profile.html", user=user)

# # Search route
# @app.route("/search", methods=["GET", "POST"])
# def search():
#     recommendations = []
#     if 'user_id' not in session:
#         return redirect("/login")
#     if request.method == "POST":
#         search_query = request.form['query']
#         user_id = session['user_id']
#         tour_data = pd.read_csv("rawTourData.csv")
#         recommendations = tour_data[tour_data['description'].str.contains(search_query, case=False, na=False)].to_dict(orient="records")
#         search_date = datetime.now()
#         cursor.execute(
            
#             "INSERT INTO search_history (user_id, search_string, search_date) VALUES (%s, %s, %s)",
#             (user_id, search_query, search_date)
#         )
#         db.commit()
#         cursor.execute(
            
#             "INSERT INTO user_search (user_id, search_string, search_date) VALUES (%s, %s)",
#             (user_id, search_query)
#         )
#         db.commit()
#     return render_template("search.html", recommendations=recommendations)

# Search route
# Search route
@app.route("/search", methods=["GET", "POST"])
def search():
    recommendations = []
    if 'user_id' not in session:
        return redirect("/login")
    
    if request.method == "POST":
        search_string = request.form['query']
        user_id = session['user_id']
        tour_data = pd.read_csv("rawTourData.csv")
        recommendations = tour_data[tour_data['description'].str.contains(search_string, case=False, na=False)].to_dict(orient="records")
        search_date = datetime.now()

        try:
            # Insert into search_history table
            cursor.execute(
                "INSERT INTO user_search (user_id, search_query) VALUES (%s, %s)",
                 (user_id, search_string)
                 
            )
            cursor.execute(
            "INSERT INTO search_history (user_id, search_string, search_date) VALUES (%s, %s, %s)",
                (user_id, search_string, search_date)
            )
            print("Inserted into search_history")
            db.commit()

            # Insert into user_search table
            # cursor.execute(
            #     "INSERT INTO user_search (user_id, search_query) VALUES (%s, %s)",
            #     (user_id, search_query)
            # )
            # print("Inserted into user_search")

            # Commit the changes to DB
            # db.commit()
            # print("Commit successful!")

        except mysql.connector.Error as err:
            print("Error:", err)
            db.rollback()  # Rollback changes if an error occurs

    return render_template("search.html", recommendations=recommendations)





# Search History route
@app.route("/search_history")
def search_history():
    if 'user_id' not in session:
        return redirect("/login")
    user_id = session['user_id']
    cursor.execute("SELECT search_string, search_date FROM search_history WHERE user_id=%s", (user_id,))
    history = cursor.fetchall()
    return render_template("search_history.html", history=history, enumerate=enumerate)

# My Recommendations route
@app.route("/my_recommendations")
def my_recommendations():
    if 'user_id' not in session:
        return redirect("/login")
    user_id = session['user_id']
    cursor.execute("SELECT search_string FROM search_history WHERE user_id=%s", (user_id,))
    searches = [row[0] for row in cursor.fetchall()]
    if not searches:
        return render_template("my_recommendations.html", recommendations=[])
    interests = '|'.join(searches)
    tour_data = pd.read_csv("rawTourData.csv")
    recommendations = tour_data[tour_data['description'].str.contains(interests, case=False, na=False)].to_dict(orient="records")
    return render_template("my_recommendations.html", recommendations=recommendations)

# Feedback route
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']

        if 'user_id' in session:
            cursor.execute("INSERT INTO feedback (user_id, feedback_text) VALUES (%s, %s)",
                           (session['user_id'], feedback_text))
            db.commit()

        return redirect(url_for('home'))

    return render_template('feedback.html')

if __name__ == "__main__":
    app.run(debug=True)

