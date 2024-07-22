from PIL import Image
import os

def split_image(input_path, output_folder, ignore_pixels=800, split_height=1300):
    # Open the image
    with Image.open(input_path) as img:
        # Convert to RGB if the image is in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        # Get image dimensions
        width, height = img.size
        
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Calculate the number of splits
        remaining_height = height - ignore_pixels
        num_splits = remaining_height // split_height
        if remaining_height % split_height != 0:
            num_splits += 1
        
        # Split and save images
        for i in range(num_splits):
            top = ignore_pixels + (i * split_height)
            bottom = min(top + split_height, height)
            
            # Crop the image
            cropped = img.crop((0, top, width, bottom))
            
            # Save the cropped image
            output_path = os.path.join(output_folder, f"split_{i+1}.jpg")
            cropped.save(output_path, "JPEG")
            print(f"Saved: {output_path}")

# Usage
input_image = "screencapture-facebook-ads-library-2024-07-22-13_52_41 copy 5.png"
output_folder = "output_photo"
split_image(input_image, output_folder)