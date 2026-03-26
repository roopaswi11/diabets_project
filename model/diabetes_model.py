def analyze_diabetes(fasting, pp, hba1c):

    status = "Unknown"

    if hba1c is not None:

        hba1c = float(hba1c)

        if hba1c < 5.7:
            status = "Normal"

        elif 5.7 <= hba1c < 6.5:
            status = "Prediabetes"

        else:
            status = "Diabetes"

    else:

        if fasting is not None:

            fasting = float(fasting)

            if fasting < 100:
                status = "Normal"

            elif 100 <= fasting <= 125:
                status = "Prediabetes"

            else:
                status = "Diabetes"

    return status


def doctor_alert(status):

    if status == "Diabetes":
        return "⚠ High diabetes risk detected. Please consult a doctor immediately."

    elif status == "Prediabetes":
        return "⚠ Risk of developing diabetes. Lifestyle changes recommended."

    elif status == "Normal":
        return "Healthy range."

    return "Unknown status."


def diet_recommendation(status):

    if status == "Diabetes":
        return """
• Avoid sugary drinks and sweets
• Prefer whole grains like oats and brown rice
• Increase vegetables and fiber-rich foods
• Include lean protein like eggs, lentils, and tofu
• Walk or exercise at least 30 minutes daily
"""

    elif status == "Prediabetes":
        return """
• Reduce refined carbohydrates
• Eat more vegetables and fruits
• Choose whole grains instead of white rice
• Maintain healthy body weight
• Exercise regularly
"""

    elif status == "Normal":
        return """
• Maintain balanced diet
• Include fruits, vegetables and whole grains
• Avoid excessive sugar consumption
• Stay physically active
"""

    return "No recommendation available."

def meal_plan(status):

    if status == "Diabetes":
        return {
            "breakfast": "Oatmeal with chia seeds and boiled egg",
            "lunch": "Brown rice with grilled chicken and mixed vegetables",
            "dinner": "Vegetable soup with whole grain roti",
            "snacks": "Almonds or roasted chickpeas"
        }

    elif status == "Prediabetes":
        return {
            "breakfast": "Vegetable omelette with whole grain toast",
            "lunch": "Quinoa salad with vegetables and paneer",
            "dinner": "Grilled fish with steamed vegetables",
            "snacks": "Apple or handful of nuts"
        }

    elif status == "Normal":
        return {
            "breakfast": "Fruit bowl with yogurt and oats",
            "lunch": "Rice with dal and vegetable curry",
            "dinner": "Chapati with paneer and vegetables",
            "snacks": "Fresh fruits"
        }

    return {}