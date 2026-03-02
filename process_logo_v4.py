from PIL import Image
import os
import numpy as np

def process_logos():
    input_path = "/Users/xuziping/workspace/my_space/alivenpc-site/assets/logo/original_logo3.png"
    base_dir = "/Users/xuziping/workspace/my_space/alivenpc-site/assets/logo"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    try:
        img = Image.open(input_path).convert("RGBA")
        print(f"Original size: {img.size}")
        
        # Function to make white background transparent
        def remove_white_bg(image, threshold=240):
            data = np.array(image)
            r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
            # Identify white pixels (r, g, b > threshold)
            white_areas = (r > threshold) & (g > threshold) & (b > threshold)
            data[white_areas, 3] = 0 # Set alpha to 0 for white pixels
            return Image.fromarray(data)

        # Remove white background first (optional, but safer if user provided JPG-like PNG)
        # Check if image has transparency already
        # Or just apply it if it looks white.
        # But let's check extrema.
        extrema = img.getextrema()
        if extrema[3][0] == 255: # Min alpha is 255 -> No transparent pixels found
            print("No transparency detected, attempting to remove white background...")
            img = remove_white_bg(img)
        else:
            print("Transparency detected, skipping white background removal.")
        
        width, height = img.size
        mid_x = width // 2
        
        # Split image
        left_img = img.crop((0, 0, mid_x, height))
        right_img = img.crop((mid_x, 0, width, height))
        
        # Function to process each logo part
        def save_variants(image, name, output_subdir):
            # Trim borders
            bbox = image.getbbox()
            if bbox:
                image = image.crop(bbox)
                print(f"Cropped {name} size: {image.size}")
            else:
                print(f"Warning: {name} seems empty or transparent.")
                return
            
            # Ensure folder exists
            out_path = os.path.join(base_dir, output_subdir)
            os.makedirs(out_path, exist_ok=True)
            
            aspect = image.width / image.height
            
            # --- Hero Logo ---
            # Target: High quality, displayed at width=400px in CSS.
            # To support Retina (2x), we want width ~800px.
            target_hero_width = 800
            
            if image.width > target_hero_width:
                 hero_width = target_hero_width
                 hero_height = int(hero_width / aspect)
                 img_hero = image.resize((hero_width, hero_height), Image.Resampling.LANCZOS)
            else:
                 # Use original size if smaller than target width
                 # But ensure it's not HUGE (e.g. taller than 800px)
                 if image.height > 800:
                      hero_height = 800
                      hero_width = int(hero_height * aspect)
                      img_hero = image.resize((hero_width, hero_height), Image.Resampling.LANCZOS)
                 else:
                      img_hero = image
                      hero_width, hero_height = img_hero.size
            
            hero_path = os.path.join(out_path, "logo_hero.png")
            img_hero.save(hero_path, optimize=True)
            print(f"Saved {hero_path} ({hero_width}x{hero_height})")
            
            # --- Header Logo ---
            # Target: Displayed at height=60px in CSS.
            # Retina target: height=120px.
            header_height = 120
            header_width = int(header_height * aspect)
            img_header = image.resize((header_width, header_height), Image.Resampling.LANCZOS)
            
            header_path = os.path.join(out_path, "logo_header.png")
            img_header.save(header_path, optimize=True)
            print(f"Saved {header_path} ({header_width}x{header_height})")

        print("Processing Left Image (Light Mode Logo)...")
        save_variants(left_img, "Light Logo", "light")
        
        print("Processing Right Image (Dark Mode Logo)...")
        save_variants(right_img, "Dark Logo", "dark")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    process_logos()
