import csv
import random
 
 
# ── CSV Loaders ─────────────────────────────────────────────────────────────
 
def load_csv(filepath):
    """
    Open a CSV file and turn each row into a dictionary.

    Example:
    If a CSV has columns like "name,color,category",
    each row becomes something like:
    {"name": "Blue Shirt", "color": "blue", "category": "top"}

    We also strip extra spaces from both the column names
    and the values so the data stays clean.
    """
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        return [
            {key.strip(): value.strip() for key, value in row.items()}
            for row in reader
        ]
 
 
# ── Weather Rule Lookup ──────────────────────────────────────────────────────
 
def get_weather_rule(weather_rules, temperature):
    """
    Given a temperature, find the matching row in weather.csv.

    Each weather rule has a minimum and maximum temperature range.
    For example, one row might say:
    60 to 75 degrees = short sleeves + shorts + no coat

    This function loops through every rule and returns the first one
    whose temperature range includes the user's temperature.

    Returns:
        A dictionary containing the matching rule
        OR None if no rule matches
    """
    for rule in weather_rules:
        if int(rule["temp_min"]) <= temperature <= int(rule["temp_max"]):
            return rule
    return None  # no matching rule found
 
 
# ── Mood Color Lookup ────────────────────────────────────────────────────────
 
def get_mood_colors(mood_data, mood):
    """
    Return a list of colors that match the user's mood.

    Example:
    If the user says "happy", this function might return:
    ["yellow", "pink", "orange"]

    It searches through mood_colors.csv and collects all colors
    connected to that mood.

    The .lower() calls make the comparison case insensitive,
    so "Happy" and "happy" both work.
    """
    return [
        row["color"]
        for row in mood_data
        if row["mood"].lower() == mood.lower()
    ]
 
 
# ── Wardrobe Filtering ───────────────────────────────────────────────────────
 
def filter_wardrobe(wardrobe, category, length, mood_colors):
    """
    Filter wardrobe items by category and clothing length.

    Parameters:
        wardrobe: list of all clothing items from wardrobe.csv
        category: the type of clothing we want ("top", "bottom", or "coat")
        length: the clothing length we want ("short", "long", etc.)
        mood_colors: list of colors connected to the user's mood

    How it works:
    1. First, find all items in the correct category and length.
       Example: all tops that are short
    2. Then, among those, look for items whose color matches the user's mood.
    3. If mood matching items exist, return only those.
    4. If not, return all items that matched the category and length.

    This fallback is important because it prevents the outfit from being empty
    just because no item matched the mood color.
    """
    # First filter by category and length
    length_matches = [
        item for item in wardrobe
        if item["category"] == category and item["length"] == length
    ]
 
    # Then try to narrow down by mood color
    color_matches = [
        item for item in length_matches
        if item["color"].lower() in [c.lower() for c in mood_colors]
    ]
 
    # Prefer mood-color matches, but fall back to any length match
    return color_matches if color_matches else length_matches
 
 
# ── Outfit Picker ────────────────────────────────────────────────────────────
 
def pick_outfit(wardrobe, weather_rule, mood_colors):
    """
    Build a full outfit using:
    - the weather rule for clothing length
    - the mood colors for color preference

    The outfit includes:
    - one top
    - one bottom
    - one coat if the weather rule says a coat is needed

    random.choice() is used so the program picks one random item
    from the matching options instead of always choosing the first one.

    Returns:
        A dictionary like:
        {
            "top": {...},
            "bottom": {...},
            "coat": {...} or None
        }
    """
    top_length    = weather_rule["top_length"]
    bottom_length = weather_rule["bottom_length"]
    needs_coat    = weather_rule["needs_coat"].lower() == "yes"
 
    tops    = filter_wardrobe(wardrobe, "top",    top_length,    mood_colors)
    bottoms = filter_wardrobe(wardrobe, "bottom", bottom_length, mood_colors)
 
    top    = random.choice(tops)    if tops    else None
    bottom = random.choice(bottoms) if bottoms else None
 
    coat = None
    if needs_coat:
        coats = filter_wardrobe(wardrobe, "coat", "long", mood_colors)
        coat  = random.choice(coats) if coats else None

    shoes = filter_wardrobe(wardrobe, "shoes", bottom_length, mood_colors)
    accessories = filter_wardrobe(wardrobe, "accessory", top_length, mood_colors)

    shoe = random.choice(shoes) if shoes else None
    accessory = random.choice(accessories) if accessories else None 

    return {
        "top": top, 
        "bottom": bottom, 
        "coat": coat,
        "shoes": shoe,
        "accessory": accessory
        }
 
 
# what is printed for the user 
 
def display_outfit(outfit, temperature, mood):
    """Print the final outfit recommendation."""
    print(f"\nIt's {temperature}°F outside and you're feeling {mood}.\n")
    print("Here's your outfit:\n")

    print(f"Top: {outfit['top']['name']} ({outfit['top']['color']})" if outfit["top"] else "Top:       (nothing found!)")
    print(f"Bottom: {outfit['bottom']['name']} ({outfit['bottom']['color']})" if outfit["bottom"] else "Bottom:    (nothing found!)")
    print(f"Shoes: {outfit['shoes']['name']} ({outfit['shoes']['color']})" if outfit["shoes"] else "Shoes:     (nothing found!)")
    print(f"Accessory: {outfit['accessory']['name']} ({outfit['accessory']['color']})" if outfit["accessory"] else "Accessory: none!")

    if outfit["coat"]:
        print(f"Coat:      {outfit['coat']['name']} ({outfit['coat']['color']})")
    else:
        print("Coat:      none!")

    print("Great outfit! Looking fetch!")
    print()
 
 
# main function
 
def main():
    # Load all three CSVs
    wardrobe      = load_csv("wardrobe.csv")
    weather_rules = load_csv("weather.csv")
    mood_data     = load_csv("mood_colors.csv")

    # Get and validate temperature immediately
    temp_input = input("What's the temperature outside? (°F): ")
    temperature = float(temp_input)

    weather_rule = get_weather_rule(weather_rules, temperature)
    if not weather_rule:
        print(f"No weather rule found for {temperature}°F. Try any temperature from 0-200 °F!")
        return

    # Get and validate mood immediately
    mood = input("What's your mood? (happy, calm, serious, romantic): ").strip()

    mood_colors = get_mood_colors(mood_data, mood)
    if not mood_colors:
        print(f"No colors found for mood '{mood}'. Try: happy, calm, serious, or romantic.")
        return

    # Pick and display the outfit
    outfit = pick_outfit(wardrobe, weather_rule, mood_colors)
    display_outfit(outfit, temperature, mood)
 
 
if __name__ == "__main__":
    main()