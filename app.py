from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import random

app = Flask(__name__)

# Comprehensive meal database with veg/non-veg and gender considerations
MEALS = {
    "high_energy": {
        "veg": [
            {"name": "Paneer Tikka with Brown Rice", "calories": 650, "protein": 38, "carbs": 68, "fat": 18, "fiber": 9, "type": "💪 Muscle Building", 
             "details": "🧀 Paneer: 200g cubes | 🍚 Brown Rice: 1.5 cups | 🥗 Salad: Onions, tomatoes, mint chutney",
             "recipe": "1. Marinate paneer in yogurt, spices for 30 min. 2. Grill until golden. 3. Cook brown rice. 4. Serve with fresh salad."},
            {"name": "Chickpea Curry with Quinoa", "calories": 640, "protein": 32, "carbs": 75, "fat": 16, "fiber": 14, "type": "🔥 Power Meal", "details": "🌾 Chickpeas: 2 cups cooked | 🍚 Quinoa: 1.5 cups | 🥘 Curry: Tomato, onion, spices"},
            {"name": "Tofu Scramble with Sweet Potato", "calories": 630, "protein": 35, "carbs": 70, "fat": 17, "fiber": 12, "type": "⚡ Pre-Workout"},
            {"name": "Lentil Dal with Roti & Rice", "calories": 660, "protein": 30, "carbs": 78, "fat": 15, "fiber": 16, "type": "💪 Muscle Building"},
            {"name": "Veggie Protein Bowl with Quinoa", "calories": 645, "protein": 36, "carbs": 72, "fat": 16, "fiber": 13, "type": "🔥 Power Meal"}
        ],
        "non_veg": [
            {"name": "Grilled Chicken with Quinoa", "calories": 650, "protein": 45, "carbs": 60, "fat": 15, "fiber": 8, "type": "💪 Muscle Building", 
             "details": "🍗 Chicken: 200g breast (2 pieces) | 🌾 Quinoa: 1.5 cups cooked | 🥦 Veggies: Broccoli, bell peppers, carrots",
             "recipe": "1. Season chicken with herbs & spices. 2. Grill 6-7 min each side. 3. Cook quinoa in broth. 4. Steam veggies. 5. Plate together."},
            {"name": "Salmon with Sweet Potato", "calories": 700, "protein": 40, "carbs": 65, "fat": 20, "fiber": 10, "type": "🔥 Power Meal", 
             "details": "🐟 Salmon: 180g fillet (1 large piece) | 🍠 Sweet Potato: 2 medium, roasted | 🥬 Greens: Steamed asparagus or green beans",
             "recipe": "1. Season salmon with lemon & dill. 2. Bake at 400°F for 12-15 min. 3. Roast sweet potatoes. 4. Steam greens. 5. Serve hot."},
            {"name": "Beef Stir-fry with Brown Rice", "calories": 680, "protein": 42, "carbs": 62, "fat": 18, "fiber": 7, "type": "💪 Muscle Building", "details": "🥩 Beef: 150g lean strips | 🍚 Brown Rice: 1.5 cups cooked | 🥕 Stir-fry: Bell peppers, onions, snap peas, soy sauce"},
            {"name": "Grilled Steak with Roasted Vegetables", "calories": 710, "protein": 46, "carbs": 58, "fat": 22, "fiber": 8, "type": "💪 Muscle Building", "details": "🥩 Steak: 200g sirloin (1 thick cut) | 🥔 Potatoes: 2 medium, roasted | 🥦 Veggies: Zucchini, bell peppers, mushrooms"},
            {"name": "Chicken Burrito Bowl with Beans", "calories": 685, "protein": 43, "carbs": 66, "fat": 18, "fiber": 11, "type": "💪 Muscle Building"},
            {"name": "Tuna Pasta with Whole Wheat", "calories": 670, "protein": 38, "carbs": 68, "fat": 16, "fiber": 9, "type": "⚡ Pre-Workout"}
        ]
    },
    "moderate_energy": {
        "veg": [
            {"name": "Veggie Burger with Sweet Potato Fries", "calories": 430, "protein": 22, "carbs": 52, "fat": 13, "fiber": 10, "type": "🌱 Plant Power"},
            {"name": "Tofu Stir-fry with Noodles", "calories": 410, "protein": 26, "carbs": 48, "fat": 11, "fiber": 9, "type": "🌱 Plant Power"},
            {"name": "Quinoa Buddha Bowl", "calories": 435, "protein": 24, "carbs": 51, "fat": 11, "fiber": 11, "type": "🌱 Plant Power"},
            {"name": "Mediterranean Chickpea Bowl", "calories": 428, "protein": 23, "carbs": 49, "fat": 12, "fiber": 10, "type": "🌱 Plant Power"},
            {"name": "Lentil Soup with Whole Grain Bread", "calories": 420, "protein": 25, "carbs": 50, "fat": 10, "fiber": 12, "type": "🌱 Plant Power"},
            {"name": "Paneer Wrap with Veggies", "calories": 445, "protein": 28, "carbs": 46, "fat": 14, "fiber": 8, "type": "🥗 Lean & Clean"}
        ],
        "non_veg": [
            {"name": "Turkey Wrap with Vegetables", "calories": 450, "protein": 30, "carbs": 45, "fat": 12, "fiber": 6, "type": "🥗 Lean & Clean"},
            {"name": "Grilled Fish with Steamed Vegetables", "calories": 400, "protein": 35, "carbs": 35, "fat": 10, "fiber": 8, "type": "🥗 Lean & Clean"},
            {"name": "Chicken Caesar Salad", "calories": 440, "protein": 32, "carbs": 38, "fat": 14, "fiber": 7, "type": "🥗 Lean & Clean"},
            {"name": "Grilled Chicken Sandwich", "calories": 445, "protein": 33, "carbs": 46, "fat": 12, "fiber": 6, "type": "🥗 Lean & Clean"},
            {"name": "Shrimp Tacos with Avocado", "calories": 425, "protein": 28, "carbs": 42, "fat": 13, "fiber": 8, "type": "🥗 Lean & Clean"},
            {"name": "Baked Cod with Asparagus", "calories": 415, "protein": 36, "carbs": 36, "fat": 10, "fiber": 7, "type": "🥗 Lean & Clean"}
        ]
    },
    "low_energy": {
        "veg": [
            {"name": "Greek Yogurt with Berries", "calories": 250, "protein": 20, "carbs": 30, "fat": 5, "fiber": 5, "type": "🍃 Light & Fit"},
            {"name": "Vegetable Salad with Chickpeas", "calories": 300, "protein": 15, "carbs": 35, "fat": 8, "fiber": 10, "type": "🥬 Fat Burner"},
            {"name": "Avocado Toast on Whole Grain", "calories": 290, "protein": 12, "carbs": 32, "fat": 10, "fiber": 9, "type": "🥬 Fat Burner"},
            {"name": "Fruit Salad with Almonds", "calories": 270, "protein": 8, "carbs": 38, "fat": 9, "fiber": 7, "type": "🍃 Light & Fit"},
            {"name": "Hummus with Veggie Sticks", "calories": 255, "protein": 10, "carbs": 30, "fat": 8, "fiber": 8, "type": "🥬 Fat Burner"},
            {"name": "Smoothie Bowl with Granola", "calories": 295, "protein": 14, "carbs": 36, "fat": 7, "fiber": 6, "type": "🍃 Light & Fit"},
            {"name": "Paneer Salad Bowl", "calories": 285, "protein": 22, "carbs": 26, "fat": 10, "fiber": 6, "type": "🥬 Fat Burner"}
        ],
        "non_veg": [
            {"name": "Egg White Omelette with Spinach", "calories": 280, "protein": 25, "carbs": 20, "fat": 8, "fiber": 4, "type": "🍃 Light & Fit"},
            {"name": "Tuna Salad Lettuce Wraps", "calories": 285, "protein": 24, "carbs": 22, "fat": 9, "fiber": 5, "type": "🍃 Light & Fit"},
            {"name": "Grilled Chicken Salad", "calories": 292, "protein": 26, "carbs": 24, "fat": 9, "fiber": 7, "type": "🥬 Fat Burner"},
            {"name": "Protein Shake (Low Carb)", "calories": 245, "protein": 28, "carbs": 18, "fat": 6, "fiber": 3, "type": "🍃 Light & Fit"},
            {"name": "Cottage Cheese with Cucumber", "calories": 260, "protein": 22, "carbs": 28, "fat": 6, "fiber": 4, "type": "🍃 Light & Fit"}
        ]
    },
    "recovery": {
        "veg": [
            {"name": "Banana Smoothie with Protein", "calories": 350, "protein": 25, "carbs": 45, "fat": 6, "fiber": 5, "type": "🔄 Post-Workout"},
            {"name": "Oatmeal with Nuts and Honey", "calories": 380, "protein": 15, "carbs": 55, "fat": 12, "fiber": 8, "type": "🧘 Recovery"},
            {"name": "Acai Bowl with Chia Seeds", "calories": 360, "protein": 16, "carbs": 52, "fat": 10, "fiber": 10, "type": "🧘 Recovery"},
            {"name": "Green Smoothie with Spinach", "calories": 335, "protein": 22, "carbs": 44, "fat": 6, "fiber": 7, "type": "🔄 Post-Workout"},
            {"name": "Baked Sweet Potato with Beans", "calories": 370, "protein": 18, "carbs": 54, "fat": 9, "fiber": 11, "type": "🧘 Recovery"},
            {"name": "Blueberry Walnut Porridge", "calories": 365, "protein": 17, "carbs": 50, "fat": 11, "fiber": 9, "type": "🧘 Recovery"}
        ],
        "non_veg": [
            {"name": "Berry Protein Shake", "calories": 340, "protein": 26, "carbs": 42, "fat": 7, "fiber": 6, "type": "🔄 Post-Workout"},
            {"name": "Salmon with Quinoa Salad", "calories": 375, "protein": 30, "carbs": 38, "fat": 11, "fiber": 7, "type": "🔄 Post-Workout", 
             "details": "🐟 Salmon: 150g fillet (palm-sized) | 🌾 Quinoa: 1 cup cooked | 🥗 Salad: Mixed greens, cherry tomatoes, cucumber, red onion, lemon dressing",
             "recipe": "1. Grill salmon 4-5 min per side. 2. Cook quinoa. 3. Chop salad veggies. 4. Mix with lemon dressing. 5. Top with salmon."},
            {"name": "Chicken Soup with Vegetables", "calories": 320, "protein": 28, "carbs": 30, "fat": 8, "fiber": 6, "type": "🧘 Recovery"},
            {"name": "Turkey and Vegetable Stew", "calories": 330, "protein": 27, "carbs": 35, "fat": 8, "fiber": 8, "type": "🧘 Recovery"},
            {"name": "Grilled Chicken with Rice", "calories": 368, "protein": 31, "carbs": 39, "fat": 9, "fiber": 6, "type": "🔄 Post-Workout"},
            {"name": "Tuna Poke Bowl", "calories": 358, "protein": 29, "carbs": 37, "fat": 10, "fiber": 7, "type": "🔄 Post-Workout"}
        ]
    }
}

def analyze_physiological_data(heart_rate, blood_oxygen, activity_level):
    """AI-based analysis of physiological data"""
    
    # Check blood oxygen first (highest priority)
    if blood_oxygen < 95:
        energy_state = "recovery"
        recommendation = "Your oxygen levels are a bit low. 🧘 Let's focus on recovery meals rich in antioxidants to help your body bounce back!"
        health_alert = "Hey, we noticed your oxygen levels are lower than usual. If this persists, it might be worth checking in with your doctor. Your health comes first! 💙"
        return {
            "energy_state": energy_state,
            "recommendation": recommendation,
            "health_alert": health_alert
        }
    
    # Check activity level (second priority)
    if activity_level == "high":
        energy_state = "high_energy"
        recommendation = "You're in intense training mode! 🔥 Your body needs energy-dense meals to fuel your workout and recovery."
    elif activity_level == "low":
        energy_state = "low_energy"
        recommendation = "You're in rest mode - perfect! 😌 Your body needs light, nutritious meals that won't weigh you down."
    else:  # moderate
        # Use heart rate for moderate activity
        if heart_rate > 100:
            energy_state = "high_energy"
            recommendation = "Your heart's pumping! 💓 You're burning serious energy right now. Let's fuel you up with power-packed meals!"
        elif heart_rate > 80:
            energy_state = "moderate_energy"
            recommendation = "You're in a good active zone! 🚀 Your body needs balanced nutrition to maintain this steady energy level."
        else:
            energy_state = "moderate_energy"
            recommendation = "You're at a comfortable pace! 🚀 Balanced meals will keep you energized throughout the day."
    
    return {
        "energy_state": energy_state,
        "recommendation": recommendation,
        "health_alert": None
    }

def adjust_portions_for_gender(meal, gender):
    """Adjust meal portions based on gender"""
    adjusted_meal = meal.copy()
    if gender == "female":
        # Reduce portions by ~25% for females (scientifically appropriate)
        adjusted_meal["calories"] = int(meal["calories"] * 0.75)
        adjusted_meal["protein"] = int(meal["protein"] * 0.75)
        adjusted_meal["carbs"] = int(meal["carbs"] * 0.75)
        adjusted_meal["fat"] = int(meal.get("fat", 0) * 0.75)
        adjusted_meal["fiber"] = int(meal.get("fiber", 0) * 0.75)
        
        # Keep details and recipe unchanged
        if "details" in meal:
            adjusted_meal["details"] = "👩 Female Portion (25% reduced): " + meal["details"]
        if "recipe" in meal:
            adjusted_meal["recipe"] = meal["recipe"]
    else:
        if "details" in meal:
            adjusted_meal["details"] = "👨 Male Portion: " + meal["details"]
        if "recipe" in meal:
            adjusted_meal["recipe"] = meal["recipe"]
    
    return adjusted_meal

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/suggest-meals', methods=['POST'])
def suggest_meals():
    data = request.json
    
    heart_rate = int(data.get('heart_rate', 70))
    blood_oxygen = int(data.get('blood_oxygen', 98))
    activity_level = data.get('activity_level', 'moderate')
    gender = data.get('gender', 'male')
    diet_preference = data.get('diet_preference', 'both')
    
    analysis = analyze_physiological_data(heart_rate, blood_oxygen, activity_level)
    meal_category = analysis['energy_state']
    
    # Filter meals based on diet preference
    available_meals = []
    if diet_preference == 'veg':
        available_meals = MEALS[meal_category]['veg']
    else:  # non-veg gets both veg and non-veg options
        available_meals = MEALS[meal_category]['veg'] + MEALS[meal_category]['non_veg']
    
    # Select random meals
    num_meals = min(3, len(available_meals))
    suggested_meals = random.sample(available_meals, num_meals)
    
    # Adjust portions for gender
    suggested_meals = [adjust_portions_for_gender(meal, gender) for meal in suggested_meals]
    
    # Add gender info to analysis
    analysis['gender_info'] = f"👨 Male portions" if gender == 'male' else f"👩 Female portions (25% reduced for optimal nutrition)"
    
    return jsonify({
        "status": "success",
        "analysis": analysis,
        "meals": suggested_meals,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
