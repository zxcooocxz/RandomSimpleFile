import os
from PIL import Image

folder_path = "E:/MOVIE"
output_path = "E:/MovieConvert"

if not os.path.exists(output_path):
    os.makedirs(output_path)

for filename in os.listdir(folder_path):
    input_file = os.path.join(folder_path, filename)
    output_file = os.path.join(output_path, filename + ".jpg")
    
    try:
        with Image.open(input_file) as img:
            img.convert("RGB").save(output_file, "JPEG")
        print(f"Converted: {filename} → {output_file}")
    except Exception as e:
        print(f"Failed to convert {filename}: {e}")
