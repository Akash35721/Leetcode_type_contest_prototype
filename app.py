# The new imports are 'render_template'
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f9a8a8f7c9e0d9a7f8d6c9c8d7b6a5b4'   # will put this in env variable later <<======================
socketio = SocketIO(app, cors_allowed_origins="*")


match_state = {
    'winner': None
}
CORRECT_ANSWER_STRING = "wellwell"



@app.route('/')
def index():
    """This function will serve the index.html file from the templates folder."""
    return render_template('index.html')



@app.route('/submit', methods=['POST'])
def submit_code():
    if match_state['winner']:
        return jsonify({'status': 'failed', 'reason': 'Match is already over.'}), 400

    data = request.get_json()
    player_name = data.get('player_name')
    submitted_code = data.get('code')

    if not player_name or not submitted_code:
        return jsonify({'status': 'failed', 'reason': 'Missing player_name or code.'}), 400

    print(f"Received submission from {player_name}")

    if CORRECT_ANSWER_STRING in submitted_code:
        match_state['winner'] = player_name
        print(f"Correct submission! {player_name} is the winner!")
        socketio.emit('gameOver', {'winner': player_name})
        return jsonify({'status': 'success', 'result': 'Correct Answer!'})
    else:
        return jsonify({'status': 'success', 'result': 'Wrong Answer.'})

@socketio.on('connect')
def handle_connect():
    print('A new client has connected!')
    if match_state['winner']:
        emit('gameOver', {'winner': match_state['winner']})

if __name__ == '__main__':
    print("Server starting on http://127.0.0.1:5000")
    socketio.run(app, host='0.0.0.0', port=5000)