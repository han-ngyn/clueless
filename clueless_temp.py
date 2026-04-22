import csv
import random
import requests
 
 
def load_csv(filepath): #csv loader. strip values of whitespace and allows us to access/load the different csv files  
    with open(filepath, newline="") as f: #file is opened to access csv files. newline = "" allows for proper recognition of ending lines
        reader = csv.DictReader(f)
        return [
            {key.strip(): value.strip() for key, value in row.items()}
            for row in reader
        ]
 
 
def get_todays_temperature(latitude=42.3876, longitude=-71.0995): #fetches today's high and low from Open-Meteo and returns the average
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max", "temperature_2m_min"],
        "temperature_unit": "fahrenheit",
        "forecast_days": 1,
        "timezone": "America/New_York"
    }
    response = requests.get(url, params=params)
    response.raise_for_status() #raises an error if the request fails
    data = response.json()
 
    high = data["daily"]["temperature_2m_max"][0]
    low  = data["daily"]["temperature_2m_min"][0]
    avg  = (high + low) / 2
 
    print(f"Today's forecast — High: {high}°F  Low: {low}°F  Average: {avg:.1f}°F")
    return avg
 
 
def get_weather_rule(weather_rules, temperature): #weather rules include max and minimum temperature values. 
    for rule in weather_rules:
        if int(rule["temp_min"]) <= temperature <= int(rule["temp_max"]): #does the temp fall in the defined range?
            return rule
    return None  #if no rule is found the function returns None
 
 
def get_mood_colors(mood_data, mood): #key that associates mood to color
    return [
        row["color"] #extracts the associated color for the given mood
        for row in mood_data
        if row["mood"].lower() == mood.lower() #standardize no capitalization (CALM, Calm, calm all work)
    ]
 
 
def filter_wardrobe(wardrobe, category, length, mood_colors): #there are more parameters to filter through here (category, length, color)
    length_matches = [ #we need to find what articles of clothing are eligible based on length and type first
        item for item in wardrobe
        if item["category"] == category and item["length"] == length #will shorten our list and specify category + length = eligible
    ]
    color_matches = [ #now we bring in the color parameter and further narrow down our results
        item for item in length_matches
        if item["color"].lower() in [c.lower() for c in mood_colors] #lowercase standardization. filters length_matches for eligible color(s)
    ]
    return color_matches if color_matches else length_matches #return a color matched, length matched item. 
    #                                                          if there are no items in length_matched that are
    #                                                          the desired color, return a length matched item. 
 
 
def pick_outfit(wardrobe, weather_rule, mood_colors): #this function builds our outfit!
 
    top_length    = weather_rule["top_length"] #determine what sleeve length for top based on weather
    bottom_length = weather_rule["bottom_length"] #determine what pant length for bottom based on weather
    needs_coat    = weather_rule["needs_coat"].lower() == "yes" #string yes/no --> boolean
 
    tops    = filter_wardrobe(wardrobe, "top",    top_length,    mood_colors) #call filter_wardrobe for TOPS
    bottoms = filter_wardrobe(wardrobe, "bottom", bottom_length, mood_colors) #call filter_wardrobe for BOTTOMS
 
    top    = random.choice(tops)    if tops    else None #from list of eligible items, randomly pick one
    bottom = random.choice(bottoms) if bottoms else None
 
    coat = None #default is no coat. 
    if needs_coat: #coat will only be assigned if needs_coat = True
        coats = filter_wardrobe(wardrobe, "coat", "long", mood_colors) #all coats are long, but filter for color
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
 
 
def main():
    #load csv files
    wardrobe      = load_csv("wardrobe.csv")
    weather_rules = load_csv("weather.csv")
    mood_data     = load_csv("mood_colors.csv")
 
    #fetch today's average temperature automatically from Open-Meteo
    try:
        temperature = get_todays_temperature()
    except Exception as e:
        print(f"Could not fetch weather data: {e}")
        temp_input = input("Enter temperature manually (°F): ")
        temperature = float(temp_input)
 
    weather_rule = get_weather_rule(weather_rules, temperature)
    if not weather_rule:
        print(f"No weather rule found for {temperature:.1f}°F. Try any temperature from 0-200°F!")
        return #if the inputted weather is outside the given range or doesn't match a rule, user is prompted to input a valid temp
 
    #takes user inputted mood and strips it of any extra white space
    mood = input("What's your mood? (happy, calm, serious, romantic): ").strip()
 
    mood_colors = get_mood_colors(mood_data, mood)
    if not mood_colors:
        print(f"No colors found for mood '{mood}'. Try: happy, calm, serious, or romantic.")
        return #if user inputted mood does not match mood options, user is prompted to input a valid mood.  
 
    #building + displaying outfit 
    outfit = pick_outfit(wardrobe, weather_rule, mood_colors)
    display_outfit(outfit, temperature, mood)
 
 
if __name__ == "__main__":
    main()
 
