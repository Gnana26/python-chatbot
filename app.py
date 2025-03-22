from flask import Flask, render_template
from flask_socketio import SocketIO
import mysql.connector
import logging
import socket

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database Connection
def connect_db():
    try:
        db_conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chatbot_db"
        )
        logging.info("Database connection established successfully.")
        return db_conn, db_conn.cursor()
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to MySQL: {err}")
        return None, None

db, cursor = connect_db()

# Predefined chatbot responses
responses = {  
    "welcome": {
        "reply": "Welcome to KMCL Website! Please choose an option:",
        "options": ["Web Design Information", "Digital Marketing Information", "Need Any Help"]
    },
    "Web Design Information": {
        "reply": "Web Design includes different areas such as frontend and backend development.",
        "options": ["Static", "Dynamic", "Shopify"]
    },
    "Static": {
        "reply": "Choose a frontend option:",
        "options": ["HTML/CSS", "React", "Angular"]
    },
    "HTML/CSS": {
        "reply": "Choose your focus area:",
        "options": ["Customization", "SEO Optimization", "Responsive Design"]
    },
    "React": {
        "reply": "Choose your focus area:",
        "options": ["Ones Customization", "SEO Ones Optimization", "Responsive Design Website"]
    },
    "Angular": {
        "reply": "Choose your focus area:",
        "options": ["Customizations", "SEO", "Responsive"]
    },
    "Customization": {
        "reply": "Customization helps in modifying design as per requirements.",
        "options": ["Contact to Admin", "Continue to Chatbot", "End Chat"]
    },
    "SEO Optimization": {
        "reply": "SEO Optimization helps in ranking better on search engines.",
        "options": ["Contact to Admin", "Continue to Chatbot", "End Chat"]
    },
    "Responsive Design": {
        "reply": "Responsive Design ensures compatibility across devices.",
        "options": ["Contact to Admin", "Continue to Chatbot", "End Chat"]
    },
    "Digital Marketing Information": {
        "reply": "Choose a category of digital marketing.",
        "options": ["Website Marketing", "Product Marketing", "Sales Marketing"]
    },
    "Website Marketing": {
        "reply": "Please choose how you want to proceed.",
        "options": ["Email marketing", "Content marketing", "Social media marketing"]
    },
    "Product Marketing": {
        "reply": "Please choose how you want to proceed.",
        "options": ["Market research", "Product launch", "Market strategy"]
    },
    "Sales Marketing": {
        "reply": "Please choose how you want to proceed.",
        "options": ["Value-based selling", "Consultative selling", "Digital channels"]
    },
    "Need Any Help": {
        "reply": "Please choose how you want to proceed.",
        "options": ["Contact to Admin", "Continue to Chatbot", "End Chat"]
    },
    "Contact to Admin": {
        "reply": "Redirecting to admin chat...",
        "options": [],
        "redirect": "/chat_message.php"
    }
}


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('user_message')
def handle_user_message(data):
    user_message = data.get('message', '').strip()
    
    if not user_message:
        logging.warning("Received an empty message from the user.")
        return

    response = responses.get(user_message, {"reply": "I'm sorry, I don't understand.", "options": []})

    logging.info(f"User Message: {user_message}")
    logging.info(f"Bot Response: {response['reply']}")

    if db:
        save_message(user_message, response['reply'])

    socketio.emit('bot_response', response)

def save_message(user_message, bot_reply):
    if db and cursor:
        try:
            cursor.execute("INSERT INTO chatbot_messages (user_message, bot_reply) VALUES (%s, %s)", (user_message, bot_reply))
            db.commit()
            logging.info(f"Saved message to database: {user_message} -> {bot_reply}")
        except mysql.connector.Error as err:
            logging.error(f"Error saving message to database: {err}")

if __name__ == '__main__':
    port = 5003
    logging.info(f"Running Flask-SocketIO on port {port}")
    socketio.run(app, debug=True, port=port, use_reloader=False)