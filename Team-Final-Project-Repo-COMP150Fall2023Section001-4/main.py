from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_database.db'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key_here'


def query_db(query: str, params: tuple = ()) -> list:
    """Query the SQLite database and return all the results."""
    conn = sqlite3.connect('game.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


def execute_db(query: str, params: tuple = ()):
    """Execute an action on the SQLite database."""
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


@app.route('/')
def hello_world():
    user_data = {
        'user_id': request.headers.get('X-Replit-User-Id'),
        'user_name': request.headers.get('X-Replit-User-Name'),
        'user_roles': request.headers.get('X-Replit-User-Roles'),
        'user_bio': request.headers.get('X-Replit-User-Bio'),
        'user_profile_image': request.headers.get('X-Replit-User-Profile-Image'),
        'user_teams': request.headers.get('X-Replit-User-Teams'),
        'user_url': request.headers.get('X-Replit-User-Url')
    }
    return render_template('createaccount.html', user_data=user_data)


# Code to redirect to new window
@app.route('/buttonpressing')
def button_game():
    return render_template('buttonpressing.html')


@app.route('/tictactoe')
def tic_tac_toe():
    return render_template('tictactoe.html')


@app.route('/pong')
def pong_game():
    return render_template('pong.html')


@app.route('/rps')
def rps_game():
    return render_template('rps.html')


@app.route('/bingo')
def bingo_game():
    return render_template('bingo.html')


@app.route('/pacman')
def pacman_game():
    return render_template('pacman.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/index')
def main():
    return render_template('index.html')


@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/resume')
def resume():
    return render_template('resume.html')


users = {
    "user1": {"password": "password1", "currency": 100, "games": []}
}


# CURRENCY
@app.route('/purchase_game', methods=['POST'])
def purchase_game():
    data = request.get_json()
    game_number = data.get('game_number')
    game_price = data.get('game_price')

    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()

        if user and user.currency >= game_price:
            user.currency -= game_price
            user.games.append(game_number)
            db.session.commit()
            return jsonify({"message": "Game purchased!"}), 200

    return jsonify({"message": "Insufficient funds or not logged in."}), 400


global_currency = 0


@app.route('/update', methods=['POST'])
def update_currency():
    global global_currency
    data = request.get_json()
    if 'currency' in data:
        global_currency = data['currency']
        return jsonify({'message': 'Global currency updated successfully'})
    return jsonify({'message': 'Bad request'}), 400


@app.route('/get', methods=['GET'])
def get_currency():
    return jsonify({'globalCurrency': global_currency})


@app.route('/')
def home():
    return render_template('createaccount.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()
        # Store password as is (insecure, replace with a secure method)
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists. Registration failed."
    else:
        return "Invalid data. Registration failed."


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('game.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0] == password:  # Directly comparing the password (insecure)
            session['username'] = username
            session['currency'] = 100
            return redirect('/main_page')
        else:
            return "Login failed. Invalid username or password."

    return render_template('login.html')


# Check if user is new or returning

@app.route('/start_new_game')
def start_new_game():
    message = request.args.get('message')
    return render_template('index.html', message=message)


@app.route('/resume_or_start_game')
def resume_or_start_game():
    message = request.args.get('message')
    return render_template('index.html', message=message)


@app.route('/resume_game')
def resume_game():
    return "Resuming your game."


@app.route('/main_page')
def main_page():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))  # Redirect to the login page if not logged in


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        # Clear the session to log the user out
        session.pop('username', None)
        return redirect(url_for('login'))
    return render_template('logout.html')


def init_db():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()

    cursor.execute('''
      CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          username TEXT NOT NULL UNIQUE,
          password TEXT NOT NULL,
          currency INTEGER DEFAULT 0 
      )
  ''')

    conn.commit()
    conn.close()


@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template("index.html")


@app.route('/api/get_count', methods=['GET'])
def get_count():
    """Fetch the current count value from the database."""
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM counter WHERE id = 1")
    count = cursor.fetchone()[0]
    conn.close()
    return jsonify({"count": count})


@app.route('/api/increment', methods=['POST'])
def increment_count():
    """Increment the count value in the database."""
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM counter WHERE id = 1")
    current_count = cursor.fetchone()[0]
    new_count = current_count + 1
    cursor.execute("UPDATE counter SET value = ? WHERE id = 1", (new_count,))
    conn.commit()
    conn.close()
    return jsonify({"new_count": new_count})


# ROCK PAPER SCISSORS GAME
def play_rps(user_choice):
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = "It's a tie!"
    elif (
            (user_choice == "rock" and computer_choice == "scissors") or
            (user_choice == "paper" and computer_choice == "rock") or
            (user_choice == "scissors" and computer_choice == "paper")
    ):
        result = "You win!"
    else:
        result = "Computer wins!"

    return {"user_choice": user_choice, "computer_choice": computer_choice, "result": result}


@app.route("/play", methods=["POST"])
def play():
    user_choice = request.json["choice"]
    result = play_rps(user_choice)
    return jsonify(result)


# BINGO GAME

bingo_numbers = set()
selected_numbers = set()


@app.route('/start', methods=['GET'])
def start_game():
    global bingo_numbers, selected_numbers
    bingo_numbers = set(range(1, 76))
    selected_numbers = set()
    return jsonify({"message": "Bingo game started"})


@app.route('/draw', methods=['GET'])
def draw_number():
    if bingo_numbers:
        number = random.choice(list(bingo_numbers))
        bingo_numbers.remove(number)
        selected_numbers.add(number)
        return jsonify({"number": number, "selected_numbers": list(selected_numbers)})
    else:
        return jsonify({"message": "All numbers have been drawn"})


if __name__ == "__main__":
    init_db()
    app.secret_key = 'your_secret_key_here'
    app.run(host='0.0.0.0', port=8080, debug=True)
