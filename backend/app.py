from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, send_file
from flask_cors import CORS
import os
import google.generativeai as genai
from dotenv import load_dotenv
from web_automation import order_food, order_cab, order_accessories
import json

# Load environment variables
load_dotenv()

app = Flask(__name__, 
            static_folder='../frontend',
            static_url_path='')
CORS(app)

# Configure Gemini AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro')

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
@app.route('/modes/<mode>')
def serve_mode(mode=None):
    # If mode is None, get it from query parameters
    if mode is None:
        mode = request.args.get('mode', '')
    
    # Normalize the mode parameter by removing extra spaces and decoding URL encoding
    normalized_mode = mode.strip().lower() if mode else ''
    
    if normalized_mode == 'entertainment':
        return send_from_directory(app.static_folder, 'entertainment_mode.html')
    elif normalized_mode == 'religious':
        return send_from_directory(app.static_folder, 'religious_mode.html')
    elif normalized_mode == 'information':
        return send_from_directory(app.static_folder, 'information_mode.html')
    elif normalized_mode == 'order':
        return send_from_directory(app.static_folder, 'order_mode.html')
    elif normalized_mode in ['ai-companion', 'ai companion']:
        return send_from_directory(app.static_folder, 'ai_companion_mode.html')
    elif normalized_mode in ['communications', 'communication']:
        return send_from_directory(app.static_folder, 'communications_mode.html')
    elif normalized_mode in ['safety', 'security', 'safety & security', 'safety%20&%20security']:
        return send_from_directory(app.static_folder, 'safety_mode.html')
    elif normalized_mode in ['medical', 'medical info', 'medical%20info']:
        return send_from_directory(app.static_folder, 'medical_mode.html')
    else:
        return "Mode not found", 404

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

@app.route('/api/modes/information', methods=['POST'])
def information_mode():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400

        query = data['query']
        print(f"Received query: {query}")  # Debug print

        # Configure Gemini AI
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("Error: GEMINI_API_KEY not found in environment variables")
            return jsonify({'error': 'API configuration error'}), 500

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')

        # Generate response
        try:
            response = model.generate_content(
                f"""You are a helpful assistant for senior citizens. Please provide a clear, concise, and easy-to-understand answer to the following question. 
                Use simple language and avoid technical jargon. If you're not sure about something, say so honestly.
                
                Question: {query}"""
            )
            print(f"Generated response: {response.text}")  # Debug print
            return jsonify({
                'response': response.text,
                'mode': 'information'
            })
        except Exception as e:
            print(f"Error generating response: {str(e)}")  # Debug print
            return jsonify({'error': f'Error generating response: {str(e)}'}), 500

    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug print
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/modes/religious', methods=['POST'])
def religious_mode():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400

        query = data['query']
        print(f"Received religious query: {query}")  # Debug print

        # Configure Gemini AI
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("Error: GEMINI_API_KEY not found in environment variables")
            return jsonify({'error': 'API configuration error'}), 500

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro')

        # Generate response
        try:
            response = model.generate_content(
                f"""You are a helpful assistant for senior citizens regarding religious and spiritual matters. 
                Please provide a clear, respectful, and easy-to-understand answer to the following question about faith or spirituality.
                Use simple language and avoid technical jargon. If you're not sure about something, say so honestly.
                Be inclusive and respectful of all religious beliefs.
                
                Question: {query}"""
            )
            print(f"Generated religious response: {response.text}")  # Debug print
            return jsonify({
                'response': response.text,
                'mode': 'religious'
            })
        except Exception as e:
            print(f"Error generating religious response: {str(e)}")  # Debug print
            return jsonify({'error': f'Error generating response: {str(e)}'}), 500

    except Exception as e:
        print(f"Unexpected error in religious mode: {str(e)}")  # Debug print
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

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

@app.route('/api/modes/order', methods=['POST'])
def handle_order():
    try:
        data = request.get_json()
        if not data or 'type' not in data or 'query' not in data:
            return jsonify({'error': 'Missing order type or query'}), 400

        order_type = data['type']
        query = data['query']

        if order_type == 'food':
            result = order_food(query)
        elif order_type == 'cab':
            result = order_cab(query)
        elif order_type == 'accessories':
            result = order_accessories(query)
        else:
            return jsonify({'error': 'Invalid order type'}), 400

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/modes/ai-companion', methods=['POST'])
def handle_ai_companion():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Missing message'}), 400

        # Configure Gemini AI
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-pro')

        # Generate response
        response = model.generate_content(
            f"""You are a friendly AI companion for senior citizens. 
            Be kind, patient, and understanding in your responses.
            Keep your responses clear and concise.
            User's message: {data['message']}"""
        )

        return jsonify({
            'status': 'success',
            'response': response.text
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contacts/emergency', methods=['GET'])
def get_emergency_contacts():
    try:
        # Get user ID from session or request
        user_id = request.args.get('user_id') or 'default_user'
        
        # Get the user's data from localStorage (passed from frontend)
        user_data = request.args.get('user_data')
        if not user_data:
            return jsonify({
                "status": "error",
                "message": "No user data provided"
            }), 400
            
        # Parse the user data
        user_data = json.loads(user_data)
        
        # Extract emergency contacts from user data
        emergency_contacts = []
        
        # Add emergency contact 1 if provided
        if user_data.get('emergencyContact1Name'):
            emergency_contacts.append({
                "name": user_data['emergencyContact1Name'],
                "relation": user_data.get('emergencyContact1Relation', 'Emergency Contact'),
                "phone": user_data['emergencyContact1Phone'],
                "photo": user_data.get('emergencyContact1Photo', 'https://via.placeholder.com/100'),
                "is_emergency": True
            })
            
        # Add emergency contact 2 if provided
        if user_data.get('emergencyContact2Name'):
            emergency_contacts.append({
                "name": user_data['emergencyContact2Name'],
                "relation": user_data.get('emergencyContact2Relation', 'Emergency Contact'),
                "phone": user_data['emergencyContact2Phone'],
                "photo": user_data.get('emergencyContact2Photo', 'https://via.placeholder.com/100'),
                "is_emergency": True
            })
        
        return jsonify({
            "status": "success",
            "contacts": emergency_contacts
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/modes/medical', methods=['POST'])
def medical_mode():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400
            
        # Get response from AI
        response = get_ai_response(query, "medical")
        
        return jsonify({
            'response': response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 