import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
API_KEY = os.getenv('OPENAI_API_KEY')  # Store your API key in environment variable

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

def generate_meal_suggestion(preferences):
    """Generate meal suggestions using OpenAI API based on user preferences."""
    if not API_KEY:
        return {"success": False, "error": "OpenAI API key is not configured"}

    try:
        # Construct the prompt based on user preferences
        prompt = f"Generate a detailed meal plan based on these preferences:\n"
        prompt += f"Dietary Preferences: {', '.join(preferences.get('dietary', []))}\n"
        prompt += f"Fitness Goal: {preferences.get('fitness_goal', '')}\n"
        prompt += f"Daily Budget: ₹{preferences.get('budget', '')}\n"
        prompt += f"Cooking Facilities: {', '.join(preferences.get('facilities', []))}\n"
        prompt += f"Restrictions: {preferences.get('restrictions', '')}\n"
        prompt += "\nProvide a structured meal plan with breakfast, lunch, dinner, and snacks. Include approximate costs and cooking instructions."

        # Make API call using the new OpenAI client
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a nutritionist and meal planning expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        # Extract and structure the response
        meal_plan = response.choices[0].message.content
        return {"success": True, "meal_plan": meal_plan}

    except Exception as e:
        return {"success": False, "error": str(e)}