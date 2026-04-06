import csv
import random
 
# ── Temperature thresholds ──────────────────────────────────────────────────
HOT   = 70   # >= 70°F → short everything, no coat
COLD  = 50   # <  50°F → long everything, coat required
# between COLD and HOT is "mild" → long top/bottom, coat optional
 
 
def load_closet(filepath):
    """Read the CSV and return a list of clothing item dicts."""
    closet = []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            closet.append(row)
    return closet
 
 
def filter_by(closet, category, length):
    """Return all items matching a given category and length."""
    return [
        item for item in closet
        if item["category"] == category and item["length"] == length
    ]
 
 
def pick_outfit(closet, temperature):
    """
    Given a closet (list of dicts) and a temperature (int/float in °F),
    return a dict with the chosen top, bottom, and coat (if needed).
    """
 
    if temperature >= HOT:
        # Hot: short top, short bottom, no coat
        tops    = filter_by(closet, "top",    "short")
        bottoms = filter_by(closet, "bottom", "short")
        coat    = None
 
    elif temperature < COLD:
        # Cold: long top, long bottom, coat required
        tops    = filter_by(closet, "top",    "long")
        bottoms = filter_by(closet, "bottom", "long")
        coats   = filter_by(closet, "coat",   "long")  # heavier coat when cold
        coat    = random.choice(coats) if coats else None
 
    else:
        # Mild: long top, long bottom, coat optional (50% chance)
        tops    = filter_by(closet, "top",    "long")
        bottoms = filter_by(closet, "bottom", "long")
        coats   = filter_by(closet, "coat",   "short")  # lighter coat for mild weather
        coat    = random.choice(coats) if coats and random.random() > 0.5 else None
 
    # Randomly pick one item from each filtered list
    top    = random.choice(tops)    if tops    else None
    bottom = random.choice(bottoms) if bottoms else None
 
    return {
        "top":    top,
        "bottom": bottom,
        "coat":   coat,
    }
 
 
def display_outfit(outfit, temperature):
    """Print the outfit in a readable way."""
    print(f"\n🌡️  It's {temperature}°F outside. Here's your outfit:\n")
    print(f"  👕 Top:    {outfit['top']['name']}"    if outfit["top"]    else "  👕 Top:    (nothing found!)")
    print(f"  👖 Bottom: {outfit['bottom']['name']}" if outfit["bottom"] else "  👖 Bottom: (nothing found!)")
    if outfit["coat"]:
        print(f"  🧥 Coat:   {outfit['coat']['name']}")
    else:
        print(f"  🧥 Coat:   none — enjoy the weather!")
    print()
 
 
def main():
    closet = load_closet("closet.csv")
 
    # For now, temperature is entered manually.
    # Later, this will be replaced with a real weather API call!
    temp_input = input("What's the temperature outside? (°F): ")
    temperature = float(temp_input)
 
    outfit = pick_outfit(closet, temperature)
    display_outfit(outfit, temperature)
 
 
if __name__ == "__main__":
    main()