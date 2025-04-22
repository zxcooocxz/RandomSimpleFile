import os
import shutil

# Set the path where your files are located
source_folder = "E:/ConvertOutput/MovieConvert"

# Set the destination where subfolders will be created
destination_folder = "E:/ConvertOutput/Sorting"

# Ensure the destination exists
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Loop through files in the source folder
for filename in os.listdir(source_folder):
    if "-" in filename and filename.endswith(".jpg"):  # Adjust file extension if needed
        folder_name = filename.split("-")[0]  # Extract the prefix (e.g., "00" from "00-01.jpg")
        folder_path = os.path.join(destination_folder, folder_name)

        # Create folder if it doesn’t exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Move the file
        source_path = os.path.join(source_folder, filename)
        destination_path = os.path.join(folder_path, filename)

        shutil.move(source_path, destination_path)
        print(f"Moved {filename} → {folder_path}/")

print("All files have been organized!")
