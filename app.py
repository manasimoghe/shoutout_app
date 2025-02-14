from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS  # Import CORS
import sqlite3

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)  # This allows all domains to access your API

#Globals
CONN = None # sqllite db handle
# Helper function to connect to the database
def get_db():
    global CONN
    if not CONN:
        CONN = sqlite3.connect(":memory:")
        CONN.row_factory = sqlite3.Row  # To fetch rows as dictionaries
        init_db(CONN)
    return CONN

# Initialize the database (create shoutouts table) when the app starts
def init_db(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shoutouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contents TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        likes INTEGER DEFAULT 0
    )
    ''')
    conn.commit()
    print("create shoutouts table")

# GET API: Fetch all shoutouts
@app.route('/api/v1/shoutouts', methods=['GET'])
def get_shoutouts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM shoutouts')
    shoutouts = cursor.fetchall()
    # Convert query result to a list of dictionaries
    shoutout_list = [{"id": shoutout["id"], "Contents": shoutout["contents"], "CreationTime": shoutout["created_at"], "Likes": shoutout["likes"]} for shoutout in shoutouts]
   # print(f"shoutout list: {shoutout_list}")
    return jsonify(shoutout_list)

# POST API: Add a new shoutout
@app.route('/api/v1/shoutouts', methods=['POST'])
def add_shoutouts():
    new_shoutout = request.get_json()  # Get the shoutout data from the request
    # print(f"data read: {new_shoutout}")
    contents = new_shoutout.get('contents')

    # Error handling
    if not contents:
        return jsonify({"error": "No text provided"}), 400
    
    conn = get_db()
    cursor = conn.cursor()
   # print(f"Insert {contents}")
    cursor.execute('INSERT INTO shoutouts (contents) VALUES (?)', (contents,))
    conn.commit()

    # Get the ID of the newly inserted shoutout
    new_shoutout_id = cursor.lastrowid

    return jsonify({"id": new_shoutout_id}), 201

# DELETE API: Delete a shoutout by ID
@app.route('/api/v1/shoutouts/<int:shoutout_id>', methods=['DELETE'])
def delete_shoutout(shoutout_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM shoutouts WHERE id = ?', (shoutout_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Shoutout not found"}), 404
    
    conn.commit()
    
    return jsonify({"message": f"Shoutout with id {shoutout_id} has been deleted"}), 200

# PATCH API: Increment the number of likes for a shoutout
@app.route('/api/v1/shoutouts/like/<int:shoutout_id>', methods=['PUT'])
def like_shoutout(shoutout_id):
    conn = get_db()
    cursor = conn.cursor()
    #find shoutout with given id
    cursor.execute('SELECT likes FROM shoutouts WHERE id = ?', (shoutout_id,))
    shoutout = cursor.fetchone()

    if shoutout is None:
        conn.close()
        return jsonify({"error": "Shoutout not found"}), 404

    # Increment the likes
    new_likes = shoutout['likes'] + 1
    cursor.execute('UPDATE shoutouts SET likes = ? WHERE id = ?', (new_likes, shoutout_id))
    conn.commit()

    return jsonify({"message": f"Shoutout {shoutout_id} liked", "likes": new_likes}), 200

if __name__ == '__main__':
    #start flask server
    app.run(debug=True, port=3000) # clash with 5000 port
