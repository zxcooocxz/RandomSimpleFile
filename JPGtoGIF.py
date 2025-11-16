from PIL import Image
import os

# Input folder containing subfolders of JPG frames
input_base_folder = r"E:\Temp\Input"

# Output folder where GIFs will be saved
output_base_folder = r"E:\Temp\Output"

# Create output folder if it doesn't exist
if not os.path.exists(output_base_folder):
    os.makedirs(output_base_folder)

# Loop through each subfolder inside the input directory
for folder_name in os.listdir(input_base_folder):
    folder_path = os.path.join(input_base_folder, folder_name)

    # Skip if it's not a folder
    if not os.path.isdir(folder_path):
        continue

    # Get all JPG images sorted by name → ensures correct GIF order
    image_files = sorted([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".jpg")
    ])

    # Skip empty folders
    if not image_files:
        print(f"No JPG files found in {folder_name}, skipping...")
        continue

    # Load every JPG as full RGB (best source for quantization)
    images = [
        Image.open(os.path.join(folder_path, f)).convert("RGB")
        for f in image_files
    ]

    # ---------------------------------------------------------------
    # STEP 1 — Quantize ONLY the first frame to create the palette
    # ---------------------------------------------------------------
    #
    # Why?
    #   GIF can only store 256 colors.
    #   If each frame generates its own colors → flicker/waves appear.
    #   So we build ONE global palette and apply it to all frames.
    #
    # Dithering:
    #   Floyd–Steinberg reduces banding and prevents "wave traces".
    #
    first = images[0].quantize(
        colors=256,
        method=Image.MEDIANCUT,
        dither=Image.FLOYDSTEINBERG
    )

    # Extract palette as a list (768 values = 256 colors × RGB)
    palette_list = first.getpalette()

    # ---------------------------------------------------------------
    # STEP 2 — Convert palette list into a real 'P' mode palette image
    # ---------------------------------------------------------------
    #
    # Why?
    #   Pillow requires the palette to be passed as a PAL IMAGE,
    #   not as a Python list. Otherwise it throws the "list has no load()"
    #   error.
    #
    palette_image = Image.new("P", (1, 1))
    palette_image.putpalette(palette_list)

    # List of ALL final GIF frames (after quantization)
    frames = [first]

    # ---------------------------------------------------------------
    # STEP 3 — Quantize all remaining frames using the SAME palette
    # ---------------------------------------------------------------
    #
    # Why?
    #   Using the same palette on every frame completely eliminates:
    #     • color flickering
    #     • gradient shimmering
    #     • wave artifacts on bright areas
    #     • inconsistent color jumps
    #
    for img in images[1:]:
        q = img.quantize(
            colors=256,
            method=Image.MEDIANCUT,
            dither=Image.FLOYDSTEINBERG,
            palette=palette_image  # ← IMPORTANT: enforce global palette
        )
        frames.append(q)

    # Duration for each frame (20ms = 50 FPS)
    # Using a LIST avoids timing errors in some viewers
    durations = [50] * len(frames)

    # Output GIF path
    output_gif_path = os.path.join(output_base_folder, f"{folder_name}.gif")

    # ---------------------------------------------------------------
    # STEP 4 — Save the GIF
    # ---------------------------------------------------------------
    #
    # Important:
    #   optimize=False
    #     If True, Pillow may merge/delete frames → causes waves.
    #
    #   disposal=2
    #     Ensures each frame replaces the last cleanly.
    #
    frames[0].save(
        output_gif_path,
        save_all=True,              # Save an animated GIF
        append_images=frames[1:],   # Add remaining frames
        duration=durations,         # Frame timing
        loop=0,                     # Loop forever
        disposal=2,                 # Prevent blending between frames
        optimize=False              # Avoid GIF optimizer artifacts
    )

    print(f"High-quality GIF created: {output_gif_path}")

print("All GIFs have been created successfully!")
