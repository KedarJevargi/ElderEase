from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
from flask_cors import CORS
import os

app = Flask(__name__, 
            static_folder='../frontend',
            static_url_path='')
CORS(app)

# Mock data for testing
MOCK_RESPONSES = {
    'information': 'Here is some general information...',
    'religious': 'Let me share a religious story with you...',
    'medical': 'Your medical information is important...',
    'entertainment': 'Here are some entertainment suggestions...',
    'order': 'I can help you order things...',
    'communication': 'Let me help you communicate...',
    'safety': 'Your safety is our priority...',
    'companion': 'I\'m here to chat with you...'
}

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/dashboard')
def serve_dashboard():
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route('/signup')
def serve_signup():
    return send_from_directory(app.static_folder, 'signup.html')

@app.route('/mode')
def serve_mode():
    return send_from_directory(app.static_folder, 'mode_template.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    try:
        # Mock successful signup
        return jsonify({
            "message": "User created successfully",
            "user_id": "mock-user-123"
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/modes/<mode>', methods=['POST'])
def handle_mode(mode):
    data = request.json
    user_id = data.get('user_id')
    query = data.get('query')
    
    if not user_id or not query:
        return jsonify({"error": "Missing user_id or query"}), 400

    try:
        # Return mock response based on mode
        response = MOCK_RESPONSES.get(mode, "I'm not sure how to help with that.")
        
        return jsonify({
            "response": f"{response} You asked: {query}",
            "mode": mode
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sos', methods=['POST'])
def handle_sos():
    try:
        return jsonify({
            "message": "Emergency services have been notified (mock response)",
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 