import os
from PIL import Image
import concurrent.futures

TARGET_DIR = "thumbnails"
QUALITY = 80

def convert_image(filename):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        file_path = os.path.join(TARGET_DIR, filename)
        file_name_no_ext = os.path.splitext(filename)[0]
        new_file_path = os.path.join(TARGET_DIR, file_name_no_ext + ".webp")

        if os.path.exists(new_file_path):
            return f"Skipped (Already exists): {filename}"

        try:
            with Image.open(file_path) as img:
                # Convert RGBA to RGB if saving as format that doesn't support alpha but webp does so we good usually.
                # Actually WebP supports transparency.
                img.save(new_file_path, "WEBP", quality=QUALITY, optimize=True)
                
            old_size = os.path.getsize(file_path)
            new_size = os.path.getsize(new_file_path)
            savings = old_size - new_size
            pct = (savings / old_size) * 100 if old_size > 0 else 0
            
            return f"Converted: {filename} ({old_size//1024}KB -> {new_size//1024}KB) - Saved {pct:.1f}%"
        except Exception as e:
            return f"Error converting {filename}: {e}"
    return None

def main():
    print(f"Starting optimization in '{TARGET_DIR}'...")
    if not os.path.exists(TARGET_DIR):
        print(f"Directory '{TARGET_DIR}' not found!")
        return

    files = os.listdir(TARGET_DIR)
    images = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Found {len(images)} images to process.")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(convert_image, images))

    for res in results:
        if res:
            print(res)

    print("Optimization complete.")

if __name__ == "__main__":
    main()
