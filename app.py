from flask import Flask, request
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- MySQL connection ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",       # change if needed
    password="",       # change if your MySQL has password
    database="medimind_db"
)
c = conn.cursor(buffered=True)

# --- Home page ---
@app.route('/')
def index():
    return """
    <h1>Medimind Demo</h1>
    <ul>
        <li><a href='/register'>Register</a></li>
        <li><a href='/login'>Login</a></li>
        <li><a href='/add-family'>Add Family Member</a></li>
        <li><a href='/upload'>Upload Image</a></li>
        <li><a href='/view-family'>View Family Members</a></li>
        <li><a href='/view-images'>View Uploaded Images</a></li>
    </ul>
    """

# --- Register ---
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        sql = "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)"
        c.execute(sql, (name,email,password))
        conn.commit()
        return "<h3>Registered successfully!</h3><a href='/'>Back</a>"
    return """
    <h2>Register</h2>
    <form method='POST'>
        Name: <input name='name' required><br>
        Email: <input name='email' required><br>
        Password: <input name='password' type='password' required><br>
        <input type='submit'>
    </form>
    <a href='/'>Back</a>
    """

# --- Login ---
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        c.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email,password))
        user = c.fetchone()
        if user:
            return "<h3>Welcome {}!</h3><a href='/'>Back</a>".format(user[1])
        else:
            return "<h3>Invalid credentials</h3><a href='/login'>Back</a>"
    return """
    <h2>Login</h2>
    <form method='POST'>
        Email: <input name='email' required><br>
        Password: <input name='password' type='password' required><br>
        <input type='submit'>
    </form>
    <a href='/'>Back</a>
    """

# --- Add Family Member ---
@app.route('/add-family', methods=['GET','POST'])
def add_family():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        age = request.form.get('age')
        relation = request.form.get('relation')
        sql = "INSERT INTO family_members (user_id,name,age,relation) VALUES (%s,%s,%s,%s)"
        c.execute(sql, (user_id,name,age,relation))
        conn.commit()
        return "<h3>Family member added!</h3><a href='/'>Back</a>"
    return """
    <h2>Add Family Member</h2>
    <form method='POST'>
        User ID: <input name='user_id' type='number' required><br>
        Name: <input name='name' required><br>
        Age: <input name='age' type='number' required><br>
        Relation: <input name='relation' required><br>
        <input type='submit'>
    </form>
    <a href='/'>Back</a>
    """

# --- Upload Image ---
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        user_id = request.form.get('user_id')  # optional
        if not file or file.filename=='':
            return "<h3>No file selected</h3><a href='/upload'>Back</a>"
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        sql = "INSERT INTO images (user_id,filename) VALUES (%s,%s)"
        c.execute(sql, (user_id, file.filename))
        conn.commit()
        return "<h3>File uploaded and saved in DB: {}</h3><a href='/'>Back</a>".format(file.filename)
    return """
    <h2>Upload Image</h2>
    <form method='POST' enctype='multipart/form-data'>
        User ID (optional): <input name='user_id' type='number'><br><br>
        Select file: <input name='file' type='file' required><br><br>
        <input type='submit'>
    </form>
    <a href='/'>Back</a>
    """

# --- View Family Members ---
@app.route('/view-family')
def view_family():
    c.execute("SELECT * FROM family_members")
    members = c.fetchall()
    html = "<h2>Family Members</h2><ul>"
    for m in members:
        html += "<li>ID:{} User:{} Name:{} Age:{} Relation:{}</li>".format(m[0], m[1], m[2], m[3], m[4])
    html += "</ul><a href='/'>Back</a>"
    return html

# --- View Uploaded Images ---
@app.route('/view-images')
def view_images():
    c.execute("SELECT * FROM images")
    images = c.fetchall()
    html = "<h2>Uploaded Images</h2><ul>"
    for img in images:
        html += "<li>ID:{} User:{} Filename:{} Uploaded At:{}</li>".format(img[0], img[1], img[2], img[3])
    html += "</ul><a href='/'>Back</a>"
    return html

# --- Run server ---
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)