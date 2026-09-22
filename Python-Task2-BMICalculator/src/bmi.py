def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI using weight in kilograms
    and height in centimeters.
    """

    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")

    if height_cm <= 0:
        raise ValueError("Height must be greater than zero.")

    height_m = height_cm / 100

    bmi = weight_kg / (height_m ** 2)

    return round(bmi, 2)


def get_bmi_category(bmi):
    """
    Return BMI category based on standard BMI ranges.
    """

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


def get_category_color(category):
    """
    Return a display color for the BMI category.
    """

    colors = {
        "Underweight": "orange",
        "Normal": "green",
        "Overweight": "darkorange",
        "Obese": "red"
    }

    return colors.get(category, "black")