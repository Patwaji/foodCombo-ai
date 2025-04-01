from flask import Flask, render_template, request, jsonify
import os
from config import generate_meal_suggestion
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/meal-generator')
def meal_generator():
    return render_template('meal_generator.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')
        preferences = data.get('preferences', {})
        
        # Prepare the conversation context
        system_prompt = """You are a helpful AI nutritionist and meal planner. Help users create personalized meal plans 
        based on their preferences, dietary restrictions, and budget. Provide specific meal suggestions, cooking tips, 
        and nutritional information. Keep responses concise and practical."""
        
        # Generate response using OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"My preferences: {preferences}\n\nUser question: {user_message}"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Extract and return the AI's response
        ai_response = response.choices[0].message.content
        return jsonify({'response': ai_response})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)