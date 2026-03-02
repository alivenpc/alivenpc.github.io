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

        # Remove white background if necessary
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
        
        # Function to process each logo part with crop
        def save_hero_variant(image, name, output_subdir):
            # 1. Trim borders (get bounding box of non-transparent area)
            bbox = image.getbbox()
            if bbox:
                image = image.crop(bbox)
                print(f"[{name}] Trimmed size: {image.size}")
            else:
                print(f"[{name}] Warning: Image seems empty or transparent.")
                return
            
            # 2. Crop to 2:1 aspect ratio (Landscape) from Center
            # Target ratio = 2.0 (Width / Height)
            current_w, current_h = image.size
            current_ratio = current_w / current_h
            target_ratio = 2.0
            
            crop_w, crop_h = current_w, current_h
            
            if current_ratio > target_ratio:
                # Image is too wide (panorama), crop width
                # New Width = Height * 2
                crop_w = int(current_h * target_ratio)
                crop_h = current_h
                x_offset = (current_w - crop_w) // 2
                y_offset = 0
            else:
                # Image is too tall (portrait/square), crop height
                # New Height = Width / 2
                crop_w = current_w
                crop_h = int(current_w / target_ratio)
                x_offset = 0
                y_offset = (current_h - crop_h) // 2
                
            # Perform crop
            crop_box = (x_offset, y_offset, x_offset + crop_w, y_offset + crop_h)
            image_cropped = image.crop(crop_box)
            print(f"[{name}] Center cropped to 2:1 ratio: {image_cropped.size} (from {current_w}x{current_h})")

            # 3. Resize to target dimensions: 600x300
            target_size = (600, 300)
            # Use LANCZOS for high quality downscaling/upscaling
            image_final = image_cropped.resize(target_size, Image.Resampling.LANCZOS)
            
            # Ensure folder exists
            out_path = os.path.join(base_dir, output_subdir)
            os.makedirs(out_path, exist_ok=True)
            
            hero_path = os.path.join(out_path, "logo_hero.png")
            image_final.save(hero_path, optimize=True)
            print(f"[{name}] Saved {hero_path} ({target_size[0]}x{target_size[1]})")

        print("Processing Left Image (Light Mode Logo)...")
        save_hero_variant(left_img, "Light Logo", "light")
        
        print("Processing Right Image (Dark Mode Logo)...")
        save_hero_variant(right_img, "Dark Logo", "dark")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    process_logos()
