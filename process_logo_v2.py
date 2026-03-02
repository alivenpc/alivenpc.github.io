from PIL import Image
import os

def process_logo():
    input_path = "/Users/xuziping/workspace/my_space/alivenpc-site/assets/logo/original_logo.png"
    output_dir = "/Users/xuziping/workspace/my_space/alivenpc-site/assets/logo"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    try:
        img = Image.open(input_path)
        print(f"Original size: {img.size}")

        # Crop transparent borders if any (or white borders if it's not transparent)
        # Assuming it might be transparent background, use getbbox
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        bbox = img.getbbox()
        if bbox:
            img_cropped = img.crop(bbox)
            print(f"Cropped size: {img_cropped.size}")
        else:
            img_cropped = img
            print("No bounding box found, using original image.")

        # 1. Create Header Logo (Height ~160px for high DPI display, CSS will scale to 80px)
        # Calculate width to maintain aspect ratio
        target_height_header = 160
        aspect_ratio = img_cropped.width / img_cropped.height
        target_width_header = int(target_height_header * aspect_ratio)
        
        img_header = img_cropped.resize((target_width_header, target_height_header), Image.Resampling.LANCZOS)
        header_path = os.path.join(output_dir, "logo_header.png")
        img_header.save(header_path)
        print(f"Saved header logo to {header_path} ({target_width_header}x{target_height_header})")

        # 2. Create Hero Logo (Height ~400px for large display)
        target_height_hero = 400
        target_width_hero = int(target_height_hero * aspect_ratio)
        
        img_hero = img_cropped.resize((target_width_hero, target_height_hero), Image.Resampling.LANCZOS)
        hero_path = os.path.join(output_dir, "logo_hero.png")
        img_hero.save(hero_path)
        print(f"Saved hero logo to {hero_path} ({target_width_hero}x{target_height_hero})")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_logo()
