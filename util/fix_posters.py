import os

file_path = "d:\\My Web Sites\\ProVenture-digital-agency\\index.html"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove the broken posters
    content = content.replace('poster="videos/video.jpg"', '')
    content = content.replace('poster="videos/video-2.jpg"', '')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("Successfully removed broken poster attributes from index.html")
except Exception as e:
    print(f"Error: {e}")
