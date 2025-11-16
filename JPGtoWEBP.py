from PIL import Image
import os

# Input folder containing subfolders of JPG sequences
input_base_folder = r"E:\Temp\Input"

# Output folder for the resulting .webp animations
output_base_folder = r"E:\Temp\Output"

# Ensure the output folder exists
if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

# Loop through each subfolder
for folder_name in os.listdir(input_base_folder):
    folder_path = os.path.join(input_base_folder, folder_name)

    # Skip non-folders
    if not os.path.isdir(folder_path):
        continue

    # Collect all JPG files, sorted (important for correct frame order)
    image_files = sorted([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".jpg")
    ])

    if not image_files:
        print(f"No JPG files found in {folder_name}, skipping...")
        continue

    # Load all images as RGBA (full color + transparency support)
    # WebP can store full 24/32-bit color, so no quantization needed.
    frames = [
        Image.open(os.path.join(folder_path, f)).convert("RGBA")
        for f in image_files
    ]

    # Output WebP filename
    output_webp_path = os.path.join(output_base_folder, f"{folder_name}.webp")

    # ---------------------------------------------------------------
    # Save as Animated WebP
    #
    # save_all=True    → enables animation
    # append_images     → add remaining frames
    # duration=20       → 20ms per frame (50 FPS)
    # loop=0            → infinite loop
    # lossless=True     → PERFECT quality (no artifacts)
    #
    # WebP supports both lossless and lossy modes:
    #     lossless=True = highest possible quality (recommended)
    # ---------------------------------------------------------------
    frames[0].save(
        output_webp_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,        # animation speed (20 ms = 50 FPS)
        loop=0,             # loop forever
        format="WEBP",
        lossless=True,      # FULL-QUALITY, no compression artifacts
    )

    print(f"High-quality animated WebP created: {output_webp_path}")

print("All WebP animations created successfully!")
