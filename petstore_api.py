from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.debug = True  # Enable debug logging

DATABASE = 'pets.db'

# helper function to connect to the database
def get_db():
    # db = getattr(app, '_database', None)
    # if db is None:
    #     db = app._database = sqlite3.connect(DATABASE)
    #     db.execute("CREATE TABLE IF NOT EXISTS pets (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, species TEXT, price INTEGER)")
    # return db
    # Create a new database connection for each request
    conn = sqlite3.connect('pets.db')
    return conn

def get_pet_data(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM pets WHERE id=?", (id,))
    pet = cur.fetchone()
    db.close()
    if pet:
        return {'id': pet[0], 'name': pet[1], 'species': pet[2], 'price': pet[3]}
    else:
        return None

# API endpoint to get all pets
@app.route('/pets', methods=['GET'])
def get_pets():
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM pets")
    pets = cur.fetchall()
    db.close()
    return jsonify({'pets': pets})

# API endpoint to get a single pet by ID
@app.route('/pets/<int:id>', methods=['GET'])
def get_pet(id):
    # Log the request
    app.logger.debug('Request data: %s', request.data)
    pet = get_pet_data(id)
    if pet:
        return jsonify({'pet': pet})
    else:
        return jsonify({'error': 'Pet not found'})

# API endpoint to add a new pet
@app.route('/pets', methods=['POST'])
def add_pet():
    # Log the request
    app.logger.debug('Request data: %s', request.data)
    name = request.json['name']
    species = request.json['species']
    price = request.json['price']
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO pets (name, species, price) VALUES (?, ?, ?)", (name, species, price))
    db.commit()
    db.close()
    return jsonify({'message': 'Pet added successfully'})


# API endpoint to update an existing pet by ID
@app.route('/pets/<int:id>', methods=['PUT'])
def update_pet(id):
    # Log the request
    app.logger.debug('Request data: %s', request.data)
    pet = get_pet_data(id)
    if not pet:
        return jsonify({'error': 'Pet not found'}), 404

    print("pet: ", pet)
    # Get the updated pet data from the request body
    data = request.get_json()
    name = data.get('name', pet['name'])        # Use existing name if not provided
    species = data.get('species', pet['species'])  # Use existing species if not provided
    price = data.get('price', pet['price'])     # Use existing price if not provided
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE pets SET name=?, species=?, price=? WHERE id=?", (name, species, price, id))
    db.commit()
    db.close()
    return jsonify({'message': 'Pet updated successfully'})

# API endpoint to delete a pet by ID
@app.route('/pets/<int:id>', methods=['DELETE'])
def delete_pet(id):
    # Log the request
    app.logger.debug('Request data: %s', request.data)
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM pets WHERE id=?", (id,))
    db.commit()
    db.close()
    return jsonify({'message': 'Pet deleted successfully'})

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except SystemExit as e:
        if e.code != 0:
            print(f"Error: {e}")
