import os
import re

root = r"E:\Temp\Input"

for folder in os.listdir(root):
    folder_path = os.path.join(root, folder)

    if not os.path.isdir(folder_path):
        continue

    # Collect all numbers inside folder
    numbers = []
    files = []

    regex = re.compile(r"([a-zA-Z]+)(\d+)(.*)")

    for filename in os.listdir(folder_path):
        match = regex.match(filename)
        if match:
            prefix, num, suffix = match.groups()
            numbers.append(int(num))
            files.append((filename, prefix, num, suffix))

    if not files:
        continue

    # Determine padding length by max number
    pad = len(str(max(numbers)))

    # Rename files
    for old_name, prefix, num, suffix in files:
        new_num = num.zfill(pad)
        new_name = f"{prefix}{new_num}{suffix}"
        os.rename(
            os.path.join(folder_path, old_name),
            os.path.join(folder_path, new_name)
        )

    print(f"Padded folder '{folder}' → {pad} digits")

print("Done!")
