from flask import Flask, request
import sqlite3
import os
from werkzeug.utils import secure_filename

# IMPORTANT for showing images
app = Flask(__name__, static_url_path='')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ---------------- DB ----------------
def get_db():
    conn = sqlite3.connect('medimind.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, password TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS user_info (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, age INTEGER, gender TEXT, address TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS family_info (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, member_name TEXT, relation TEXT, age INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS health_record (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, disease TEXT, medication TEXT, doctor TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS disease_images (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, image_path TEXT)")

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return """
    <h1>Medimind APIs</h1>
    <a href='/register'>Register</a><br>
    <a href='/login'>Login</a><br>
    <a href='/user_info'>User Info</a><br>
    <a href='/family_info'>Family Info</a><br>
    <a href='/health_record'>Health Record</a><br>
    <a href='/upload_image'>Upload Image</a><br>
    <a href='/view_records'>View Records</a><br>
    """

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        conn = get_db()
        conn.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
                     (request.form['name'], request.form['email'], request.form['password']))
        conn.commit()
        conn.close()
        return "Registered! <a href='/'>Home</a>"

    return """
    <h2>Register</h2>
    <form method="post">
    Name:<input name="name"><br>
    Email:<input name="email"><br>
    Password:<input name="password"><br>
    <button>Submit</button>
    </form>
    """

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                            (request.form['email'], request.form['password'])).fetchone()
        conn.close()

        if user:
            return f"Login Success! User ID = {user['id']} <br><a href='/'>Home</a>"
        else:
            return "Invalid Login <a href='/login'>Try Again</a>"

    return """
    <h2>Login</h2>
    <form method="post">
    Email:<input name="email"><br>
    Password:<input name="password"><br>
    <button>Login</button>
    </form>
    """

# ---------------- USER INFO ----------------
@app.route('/user_info', methods=['GET', 'POST'])
def user_info():
    if request.method == 'POST':
        conn = get_db()
        conn.execute("INSERT INTO user_info VALUES (NULL,?,?,?,?)",
                     (request.form['user_id'], request.form['age'],
                      request.form['gender'], request.form['address']))
        conn.commit()
        conn.close()
        return "User Info Saved <a href='/'>Home</a>"

    return """
    <h2>User Info</h2>
    <form method="post">
    User ID:<input name="user_id"><br>
    Age:<input name="age"><br>
    Gender:<input name="gender"><br>
    Address:<input name="address"><br>
    <button>Save</button>
    </form>
    """

# ---------------- FAMILY INFO ----------------
@app.route('/family_info', methods=['GET', 'POST'])
def family_info():
    if request.method == 'POST':
        conn = get_db()
        conn.execute("INSERT INTO family_info VALUES (NULL,?,?,?,?)",
                     (request.form['user_id'], request.form['member_name'],
                      request.form['relation'], request.form['age']))
        conn.commit()
        conn.close()
        return "Family Info Saved <a href='/'>Home</a>"

    return """
    <h2>Family Info</h2>
    <form method="post">
    User ID:<input name="user_id"><br>
    Member Name:<input name="member_name"><br>
    Relation:<input name="relation"><br>
    Age:<input name="age"><br>
    <button>Save</button>
    </form>
    """

# ---------------- HEALTH RECORD ----------------
@app.route('/health_record', methods=['GET', 'POST'])
def health_record():
    if request.method == 'POST':
        conn = get_db()
        conn.execute("INSERT INTO health_record VALUES (NULL,?,?,?,?)",
                     (request.form['user_id'], request.form['disease'],
                      request.form['medication'], request.form['doctor']))
        conn.commit()
        conn.close()
        return "Health Record Saved <a href='/'>Home</a>"

    return """
    <h2>Health Record</h2>
    <form method="post">
    User ID:<input name="user_id"><br>
    Disease:<input name="disease"><br>
    Medication:<input name="medication"><br>
    Doctor:<input name="doctor"><br>
    <button>Save</button>
    </form>
    """

# ---------------- IMAGE UPLOAD ----------------
@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['image']
        user_id = request.form['user_id']

        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            conn = get_db()
            conn.execute("INSERT INTO disease_images VALUES (NULL,?,?)",
                         (user_id, path))
            conn.commit()
            conn.close()

            return "Image Uploaded <a href='/'>Home</a>"

    return """
    <h2>Upload Image</h2>
    <form method="post" enctype="multipart/form-data">
    User ID:<input name="user_id"><br>
    Image:<input type="file" name="image"><br>
    <button>Upload</button>
    </form>
    """

# ---------------- VIEW RECORDS ----------------
@app.route('/view_records')
def view_records():
    conn = get_db()

    users = conn.execute("SELECT * FROM users").fetchall()
    user_info = conn.execute("SELECT * FROM user_info").fetchall()
    family = conn.execute("SELECT * FROM family_info").fetchall()
    health = conn.execute("SELECT * FROM health_record").fetchall()
    images = conn.execute("SELECT * FROM disease_images").fetchall()

    conn.close()

    html = "<h1>All Records</h1>"

    # USERS
    html += "<h2>Users</h2>"
    for u in users:
        html += f"ID: {u['id']} | Name: {u['name']} | Email: {u['email']}<br>"

    # USER INFO
    html += "<h2>User Info</h2>"
    for u in user_info:
        html += f"UserID: {u['user_id']} | Age: {u['age']} | Gender: {u['gender']} | Address: {u['address']}<br>"

    # FAMILY
    html += "<h2>Family Info</h2>"
    for f in family:
        html += f"UserID: {f['user_id']} | Name: {f['member_name']} | Relation: {f['relation']} | Age: {f['age']}<br>"

    # HEALTH
    html += "<h2>Health Records</h2>"
    for h in health:
        html += f"UserID: {h['user_id']} | Disease: {h['disease']} | Medicine: {h['medication']} | Doctor: {h['doctor']}<br>"

    # IMAGES
    html += "<h2>Images</h2>"
    for i in images:
        filename = i['image_path'].split("/")[-1]
        html += f"UserID: {i['user_id']}<br>"
        html += f"<img src='/uploads/{filename}' width='120'><br>"

    html += "<br><a href='/'>Back Home</a>"

    return html

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
