import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)  
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")

history = []

def get_ai_response(code_snippet):
    """
    Sends the code to the AI model and gets a review.
    """
    global history
    
    prompt = f"""
        You are an expert software engineer. Review the following code and provide feedback in markdown format on:
        - **Code Quality:**
        - **Best Practices:**
        - **Potential Bugs:**
        - **Performance Improvements:**
        - **Security Concerns:**

        ---
        Code to review:
        ```
        {code_snippet}
        ```
    """
    
    history.append({"role": "user", "content": prompt})
    
    header = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo", # Or any other model you are using
        "messages": history
    }
    
    try:
        response = requests.post(base_url, headers=header, json=data)
        response.raise_for_status()  # Will raise an HTTPError for bad responses (4xx or 5xx)
        reply = response.json()
        ai_content = reply['choices'][0]['message']['content']
        history.append({"role": "assistant", "content": ai_content})
        return ai_content
    except requests.exceptions.RequestException as e:
        print(f"Error making API call: {e}")
        return f"Sorry, there was an error communicating with the AI service: {e}"



@app.route('/review', methods=['POST'])
def review_code():
    """
    API endpoint that receives code from the front end.
    """
    if not request.json or 'code' not in request.json:
        return jsonify({"error": "Invalid request. 'code' not found."}), 400
        
    user_code = request.json['code']
    
    if not user_code.strip():
        return jsonify({"review": "Please provide some code to review."})

    ai_review = get_ai_response(user_code)
    
    return jsonify({"review": ai_review})


@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)