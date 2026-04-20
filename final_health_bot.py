import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def search_medicine_in_db(name):
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="health_bot"
        )
        cursor = conn.cursor(dictionary=True)
        # Search for the medicine name
        cursor.execute("SELECT * FROM medicines WHERE name LIKE %s", (f"%{name}%",))
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return None

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    user_question = data.get('question', '').strip()
    
    # Search our 25 medicines in MySQL
    med_info = search_medicine_in_db(user_question)

    if med_info:
        # If found, show the data clearly
        reply = (f"<b>Medicine Found:</b> {med_info['name']}<br>"
                 f"<b>Generic Name:</b> {med_info['generic_name']}<br>"
                 f"<b>Uses:</b> {med_info['uses']}<br>"
                 f"<b>Dosage:</b> {med_info['dosage']}")
        return jsonify({"answer": reply})
    else:
        # If not found in the 25 medicines
        return jsonify({"answer": "I'm sorry, I don't have that medicine in my database yet. Please try Napa or Sergel."})

if __name__ == '__main__':
    print("Safety Bot is starting...")
    app.run(port=5000, debug=True)