from flask import Flask, jsonify, request

app = Flask(__name__)

# Exemple de route
@app.route('/api/pixels', methods=['GET'])
def get_pixels():
    # Exemple de données
    pixels = [
        {'id': 1, 'color': 'red', 'x': 10, 'y': 20},
        {'id': 2, 'color': 'blue', 'x': 15, 'y': 25}
    ]
    return jsonify(pixels)

# Démarrer l'application
if __name__ == '__main__':
    app.run(debug=Tru