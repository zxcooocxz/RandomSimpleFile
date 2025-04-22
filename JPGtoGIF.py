from PIL import Image, ImageSequence
import os

# Define input and output directories
input_base_folder = r"E:\ConvertOutput\Sorting"
output_base_folder = r"E:\ConvertOutput\GifMaker"

# Ensure the output folder exists
if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

# Loop through each folder in Sorting
for folder_name in os.listdir(input_base_folder):
    folder_path = os.path.join(input_base_folder, folder_name)

    # Ensure it's a folder
    if not os.path.isdir(folder_path):
        continue

    # Get all .jpg files in this folder, sorted by name
    image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".jpg")])

    # Ensure there are images to process
    if not image_files:
        print(f"No JPG files found in {folder_name}, skipping...")
        continue

    # Open images and convert to RGB for better quality
    images = [Image.open(os.path.join(folder_path, img)).convert("RGB") for img in image_files]

    # Apply color quantization to improve GIF quality (reduces color banding)
    images = [img.quantize(colors=256, method=Image.MEDIANCUT) for img in images]

    # Define output GIF name using the folder name
    output_gif_path = os.path.join(output_base_folder, f"{folder_name}.gif")

    # Save as high-quality GIF
    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        duration=33,  # Match video speed (30 FPS)
        loop=0,  # Loop forever
        optimize=True,  # Reduce file size without loss
        disposal=2,  # Ensures frames don’t blend incorrectly
    )

    print(f"High-quality GIF created: {output_gif_path}")

print("All GIFs have been created successfully!")
