"""
 
Requirements:
    pip install pillow
"""
 
import sys
import math
from pathlib import Path
from PIL import Image
from collections import Counter
 

NAMED_COLORS = {
    "red":    (220,  20,  60),
    "orange": (255, 140,   0),
    "yellow": (255, 220,   0),
    "green":  (34,  139,  34),
    "blue":   (30,  144, 255),
    "indigo": (75,    0, 130),
    "violet": (148,   0, 211),
    "pink":   (255, 182, 193),
    "white":  (255, 255, 255),
    "gray":   (128, 128, 128),
    "black":  (20,   20,  20),
    "brown":  (139,  69,  19),
}
 
 
def rgb_distance(a, b):
    #distance a given pixel is from RGB 
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
 
 
def nearest_named_color(rgb):
    #returns what RGB color a pixel is closest to in value 
    best = min(NAMED_COLORS, key=lambda n: rgb_distance(rgb, NAMED_COLORS[n]))
    return best, NAMED_COLORS[best]
 
 
def is_background(rgb, tolerance=30):
    #plain white or blank background
    brightness = sum(rgb)
    return brightness > (255 * 3 - tolerance * 3) or brightness < (tolerance * 3)
 
 
def detect_dominant_color(image_path, n_colors=16, remove_bg=True):
    """
    Detect the dominant color in a clothing image.
 
    Args:
        image_path:  Path to the image file.
        n_colors:    Quantization buckets — more means finer color distinctions.
        remove_bg:   Strip near-white / near-black background pixels first.
 
    Returns a dict with dominant_rgb, dominant_hex, color_name, named_rgb, all_colors.
    """
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
 
    img = Image.open(path).convert("RGB")
    img.thumbnail((200, 200))
 
    # Quantize merges similar pixel values into buckets, then count them
    quantized = img.quantize(colors=n_colors, method=Image.Quantize.MEDIANCUT)
    pixels = list(quantized.convert("RGB").getdata())
 
    if remove_bg:
        pixels = [p for p in pixels if not is_background(p)]
 
    if not pixels:
        raise ValueError("No foreground pixels found — try remove_bg=False.")
 
    counts = Counter(pixels)
    total = sum(counts.values())
    ranked = counts.most_common()
 
    dominant_rgb = ranked[0][0]
    color_name, named_rgb = nearest_named_color(dominant_rgb)
 
    return {
        "dominant_rgb": dominant_rgb,
        "dominant_hex": "#{:02x}{:02x}{:02x}".format(*dominant_rgb),
        "color_name":   color_name,
        "named_rgb":    named_rgb,
        "all_colors":   [(rgb, round(c / total * 100, 1)) for rgb, c in ranked],
    }
 
 
def print_swatch(rgb, label, width=30):
    r, g, b = rgb
    lum = 0.299 * r + 0.587 * g + 0.114 * b      #normalization to human eye color sensitivity
    text = "\033[30m" if lum > 140 else "\033[97m"
    print(f"  \033[48;2;{r};{g};{b}m{text}{'█' * width}\033[0m  {label}")
 
 
def main(image_path):
    result = detect_dominant_color(image_path)
 
    print(f"\nAnalyzing: {image_path}\n")
    print(f"  Result -> {result['color_name'].upper()}")
    print_swatch(result["dominant_rgb"], f"detected  {result['dominant_hex']}")
    print_swatch(result["named_rgb"],    f"matched   {result['color_name']}")
 
    print("\n  All colors found:")
    for rgb, pct in result["all_colors"]:
        name, _ = nearest_named_color(rgb)
        print_swatch(rgb, f"{pct:5.1f}%  {name}")
    print()
 
 
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_color.py <image.jpg>")
        sys.exit(1)
    main(sys.argv[1])
