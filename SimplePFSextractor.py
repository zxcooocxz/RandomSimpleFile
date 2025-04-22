import os
import struct
import re

# === CONFIG ===
PFS_PATH = "root.pfs" #Change path name here
OUTPUT_DIR = "extracted_files"

# === UTILS ===
def read_strings(data, min_length=4):
    pattern = re.compile(rb'[ -~]{' + str(min_length).encode() + rb',}')
    for match in pattern.finditer(data):
        yield match.group().decode('utf-8', errors='replace'), match.start()

# === MAIN ===
def extract_pfs(filepath, output_dir):
    with open(filepath, 'rb') as f:
        raw = f.read()

    # Step 1: Extract file names & positions
    print("[+] Scanning for file names...")
    file_entries = []
    for name, pos in read_strings(raw):
        if any(name.endswith(ext) for ext in [".ogg", ".png", ".jpg", ".txt", ".bmp", ".wav"]):
            file_entries.append({'name': name, 'pos': pos})

    print(f"[+] Found {len(file_entries)} possible files.")

    # Step 2: Try to extract files (this is a rough guess based on position)
    os.makedirs(output_dir, exist_ok=True)
    for i, entry in enumerate(file_entries):
        start = None
        end = None

        # Heuristic: file data might be after the header, find gaps
        if i + 1 < len(file_entries):
            start = file_entries[i]['pos'] + 128  # Skip past name and metadata
            end = file_entries[i+1]['pos']  # Stop before next file name
        else:
            start = file_entries[i]['pos'] + 128
            end = len(raw)

        guessed_data = raw[start:end]

        # Avoid extracting junk
        if len(guessed_data) < 50:
            continue

        # Sanitize name
        safe_name = entry['name'].replace('\\', os.sep).replace('/', os.sep)
        out_path = os.path.join(output_dir, safe_name)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        with open(out_path, 'wb') as out_file:
            out_file.write(guessed_data)

        print(f"[+] Extracted: {safe_name} ({len(guessed_data)} bytes)")

if __name__ == '__main__':
    extract_pfs(PFS_PATH, OUTPUT_DIR)
