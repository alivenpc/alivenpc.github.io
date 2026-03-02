from PIL import Image
import os

def process_logos():
    input_path = "/Users/xuziping/workspace/my_space/alivenpc-site/assets/logo/original_logo3.png"
    base_dir = "/Users/xuziping/workspace/my_space/alivenpc-site/assets/logo"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    try:
        img = Image.open(input_path)
        print(f"Original size: {img.size}")
        
        width, height = img.size
        mid_x = width // 2
        
        # Split image
        left_img = img.crop((0, 0, mid_x, height))
        right_img = img.crop((mid_x, 0, width, height))
        
        # Function to process each logo part
        def save_variants(image, name, output_subdir):
            # Trim borders
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            bbox = image.getbbox()
            if bbox:
                image = image.crop(bbox)
                print(f"Cropped {name} size: {image.size}")
            else:
                print(f"Warning: {name} seems empty or transparent.")
            
            # Create Hero Logo (High Res, max height ~400px or max width ~800px)
            # Ensure file size < 1MB (using PNG optimization if needed, or just resizing)
            
            # Calculate aspect ratio
            aspect = image.width / image.height
            
            # Hero Size Target: Height 400px
            hero_height = 400
            hero_width = int(hero_height * aspect)
            img_hero = image.resize((hero_width, hero_height), Image.Resampling.LANCZOS)
            
            hero_path = os.path.join(base_dir, output_subdir, "logo_hero.png")
            img_hero.save(hero_path, optimize=True)
            print(f"Saved {hero_path} ({hero_width}x{hero_height})")
            
            # Header Size Target: Height 160px (for retina display of 80px height)
            header_height = 160
            header_width = int(header_height * aspect)
            img_header = image.resize((header_width, header_height), Image.Resampling.LANCZOS)
            
            header_path = os.path.join(base_dir, output_subdir, "logo_header.png")
            img_header.save(header_path, optimize=True)
            print(f"Saved {header_path} ({header_width}x{header_height})")

        # Process Left -> Light Logo (for Light Theme / Light Background?)
        # User said: "Left call light_logo, Right call dark_logo"
        # "分别应用到亮暗两种模式" -> "Apply to Light and Dark modes respectively"
        # So Left Image -> Light Mode Logo (folder: light)
        # Right Image -> Dark Mode Logo (folder: dark)
        
        print("Processing Left Image (Light Mode Logo)...")
        save_variants(left_img, "Light Logo", "light")
        
        print("Processing Right Image (Dark Mode Logo)...")
        save_variants(right_img, "Dark Logo", "dark")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_logos()
