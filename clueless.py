import csv
import random
 
 
# ── CSV Loaders ─────────────────────────────────────────────────────────────
 
def load_csv(filepath):
    """Generic CSV loader — returns a list of dicts, strips whitespace from all values."""
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        return [
            {key.strip(): value.strip() for key, value in row.items()}
            for row in reader
        ]
 
 
# ── Weather Rule Lookup ──────────────────────────────────────────────────────
 
def get_weather_rule(weather_rules, temperature):
    """
    Given a temperature, find the matching row in weather.csv and return it.
    Returns a dict with top_length, bottom_length, needs_coat.
    """
    for rule in weather_rules:
        if int(rule["temp_min"]) <= temperature <= int(rule["temp_max"]):
            return rule
    return None  # no matching rule found
 
 
# ── Mood Color Lookup ────────────────────────────────────────────────────────
 
def get_mood_colors(mood_data, mood):
    """Return a list of colors associated with the given mood."""
    return [
        row["color"]
        for row in mood_data
        if row["mood"].lower() == mood.lower()
    ]
 
 
# ── Wardrobe Filtering ───────────────────────────────────────────────────────
 
def filter_wardrobe(wardrobe, category, length, mood_colors):
    """
    Filter wardrobe items by category and length.
    If any items match the mood colors, return only those.
    Otherwise fall back to all length-matching items (so outfit is never empty).
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
    Build an outfit dict with a top, bottom, and coat (if needed).
    Uses weather rule for lengths and mood colors for color preference.
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
 
    return {"top": top, "bottom": bottom, "coat": coat}
 
 
# ── Display ──────────────────────────────────────────────────────────────────
 
def display_outfit(outfit, temperature, mood):
    """Print the final outfit recommendation."""
    print(f"\nIt's {temperature}°F outside and you're feeling {mood}.\n")
    print("Here's your outfit:\n")
    print(f"Top:    {outfit['top']['name']} ({outfit['top']['color']})"       if outfit["top"]    else "Top:    (nothing found!)")
    print(f"Bottom: {outfit['bottom']['name']} ({outfit['bottom']['color']})" if outfit["bottom"] else "Bottom: (nothing found!)")
    if outfit["coat"]:
        print(f"Coat:   {outfit['coat']['name']} ({outfit['coat']['color']})")
    else:
        print(f"Coat:   none!")
        print("Great outfit! Looking fetch!")
    print()
 
 
# ── Main ─────────────────────────────────────────────────────────────────────
 
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