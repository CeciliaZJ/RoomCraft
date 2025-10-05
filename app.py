from flask import Flask, render_template, request, jsonify
from manager import MarketplaceManager
from user_manager import UserManager

# This project was developed with the assistance of ChatGPT.

app = Flask(__name__)
manager = MarketplaceManager()
user_manager = UserManager()

@app.route('/')
def index():
    listings = manager.get_all_listings()
    return render_template('forum.html', flask_listings=listings)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    result = user_manager.register_api(username, password)
    return jsonify(result)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    result = user_manager.login_api(username, password)
    if result:
        return jsonify({'success': True, 'username': result})
    else:
        return jsonify({'success': False, 'message': 'Invalid login'})

@app.route('/api/create_listing', methods=['POST'])
def create_listing():
    data = request.json
    seller = data.get('seller')
    name = data.get('name')
    description = data.get('description')
    link = data.get('link')  # Support link from JS

    if not all([seller, name, description]):
        return jsonify({'success': False, 'error': 'Missing data'}), 400

    listing = manager.create_listing(seller, name, description, link)
    return jsonify({'success': True, 'listing': listing})

@app.route('/api/listings', methods=['GET'])
def get_listings():
    listings = manager.get_all_listings()
    return jsonify(listings)

if __name__ == '__main__':
    app.run(debug=True)