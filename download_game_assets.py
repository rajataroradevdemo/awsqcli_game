import os
import requests
from PIL import Image
from io import BytesIO
import pygame

# Create directories if they don't exist
os.makedirs("images", exist_ok=True)
os.makedirs("sounds", exist_ok=True)

# URLs for Tom and Jerry images (replace with actual URLs if you have specific ones)
# These are placeholder URLs for demonstration - they will be replaced with colored rectangles
image_urls = {
    # Tom animations
    "tom_run1.png": "https://example.com/tom_run1.png",
    "tom_run2.png": "https://example.com/tom_run2.png",
    "tom_run3.png": "https://example.com/tom_run3.png",
    "tom_run4.png": "https://example.com/tom_run4.png",
    "tom_jump.png": "https://example.com/tom_jump.png",
    "tom_crash.png": "https://example.com/tom_crash.png",
    
    # Jerry animations
    "jerry1.png": "https://example.com/jerry1.png",
    "jerry2.png": "https://example.com/jerry2.png",
    
    # Obstacles
    "water.png": "https://example.com/water.png",
    "iron.png": "https://example.com/iron.png",
    "sofa.png": "https://example.com/sofa.png",
    "bat.png": "https://example.com/bat.png",
    "cloth.png": "https://example.com/cloth.png",
    
    # Environment
    "cloud.png": "https://example.com/cloud.png",
    "background.png": "https://example.com/background.png",
}

def create_tom_images():
    """Create Tom character images with different colors for running animation"""
    # Tom running frames (gray cat with different poses)
    tom_colors = [(100, 100, 100), (120, 120, 120), (140, 140, 140), (160, 160, 160)]
    
    for i, color in enumerate(tom_colors):
        img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
        # Draw cat body
        for y in range(30, 80):
            for x in range(20, 80):
                img.putpixel((x, y), color)
        
        # Draw cat head
        for y in range(10, 40):
            for x in range(60, 90):
                img.putpixel((x, y), color)
        
        # Draw cat ears
        for y in range(5, 15):
            for x in range(65, 75):
                img.putpixel((x, y), color)
            for x in range(80, 90):
                img.putpixel((x, y), color)
        
        # Draw cat legs in different positions based on frame
        leg_offset = i * 5
        for y in range(80, 95):
            for x in range(30 + leg_offset, 40 + leg_offset):
                img.putpixel((x, y), color)
            for x in range(60 - leg_offset, 70 - leg_offset):
                img.putpixel((x, y), color)
        
        img.save(f"images/tom_run{i+1}.png")
    
    # Tom jumping image (similar but with legs together)
    img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
    color = (130, 130, 130)
    # Body
    for y in range(30, 80):
        for x in range(20, 80):
            img.putpixel((x, y), color)
    # Head
    for y in range(10, 40):
        for x in range(60, 90):
            img.putpixel((x, y), color)
    # Ears
    for y in range(5, 15):
        for x in range(65, 75):
            img.putpixel((x, y), color)
        for x in range(80, 90):
            img.putpixel((x, y), color)
    # Legs together for jumping
    for y in range(80, 95):
        for x in range(45, 55):
            img.putpixel((x, y), color)
    img.save("images/tom_jump.png")
    
    # Tom crash image (red tint to indicate crash)
    img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
    color = (200, 100, 100)  # Reddish color
    # Body
    for y in range(30, 80):
        for x in range(20, 80):
            img.putpixel((x, y), color)
    # Head
    for y in range(10, 40):
        for x in range(60, 90):
            img.putpixel((x, y), color)
    # Ears
    for y in range(5, 15):
        for x in range(65, 75):
            img.putpixel((x, y), color)
        for x in range(80, 90):
            img.putpixel((x, y), color)
    # Legs spread out for crash
    for y in range(80, 95):
        for x in range(20, 30):
            img.putpixel((x, y), color)
        for x in range(70, 80):
            img.putpixel((x, y), color)
    img.save("images/tom_crash.png")

def create_jerry_images():
    """Create Jerry character images with different colors for running animation"""
    # Jerry running frames (brown mouse with different poses)
    jerry_color = (139, 69, 19)  # Brown
    
    for i in range(2):
        img = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
        # Draw mouse body
        for y in range(20, 40):
            for x in range(10, 40):
                img.putpixel((x, y), jerry_color)
        
        # Draw mouse head
        for y in range(15, 30):
            for x in range(35, 50):
                img.putpixel((x, y), jerry_color)
        
        # Draw mouse ears
        for y in range(10, 15):
            for x in range(40, 45):
                img.putpixel((x, y), jerry_color)
            for x in range(45, 50):
                img.putpixel((x, y), jerry_color)
        
        # Draw mouse tail
        for y in range(25, 30):
            for x in range(5, 15):
                img.putpixel((x, y), jerry_color)
        
        # Draw mouse legs in different positions based on frame
        leg_offset = i * 5
        for y in range(40, 50):
            for x in range(15 + leg_offset, 20 + leg_offset):
                img.putpixel((x, y), jerry_color)
            for x in range(30 - leg_offset, 35 - leg_offset):
                img.putpixel((x, y), jerry_color)
        
        img.save(f"images/jerry{i+1}.png")

def create_obstacle_images():
    """Create obstacle images with different colors"""
    # Water (blue)
    img = Image.new('RGBA', (80, 30), (0, 0, 255, 180))
    img.save("images/water.png")
    
    # Iron (gray)
    img = Image.new('RGBA', (50, 70), (192, 192, 192))
    img.save("images/iron.png")
    
    # Sofa (brown)
    img = Image.new('RGBA', (120, 60), (139, 69, 19))
    img.save("images/sofa.png")
    
    # Cricket bat (wooden color)
    img = Image.new('RGBA', (20, 80), (160, 82, 45))
    img.save("images/bat.png")
    
    # Cloth (light blue)
    img = Image.new('RGBA', (60, 40), (173, 216, 230))
    img.save("images/cloth.png")

def create_environment_images():
    """Create environment images"""
    # Cloud (white)
    img = Image.new('RGBA', (100, 50), (255, 255, 255, 200))
    img.save("images/cloud.png")
    
    # Background (light yellow for house interior)
    img = Image.new('RGB', (800, 400), (255, 248, 220))
    # Add some details to the background
    for y in range(0, 400, 40):
        for x in range(0, 800, 40):
            for i in range(5):
                for j in range(5):
                    img.putpixel((x+i, y+j), (220, 220, 200))
    img.save("images/background.png")

def main():
    print("Creating game assets...")
    
    # Try to download images from URLs (this will fail with the example URLs)
    for name, url in image_urls.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.save(os.path.join("images", name))
                print(f"Downloaded {name}")
            else:
                print(f"Failed to download {name}, will create placeholder")
        except:
            print(f"Error downloading {name}, will create placeholder")
    
    # Create placeholder images
    create_tom_images()
    create_jerry_images()
    create_obstacle_images()
    create_environment_images()
    
    print("All game assets created successfully!")

if __name__ == "__main__":
    main()
