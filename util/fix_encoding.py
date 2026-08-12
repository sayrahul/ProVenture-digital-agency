import os

def fix_encoding(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Try decoding as utf-16
        try:
            text = content.decode('utf-16')
        except UnicodeDecodeError:
            # Maybe it's already utf-8
            text = content.decode('utf-8')
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Fixed encoding for {filepath}")
    except Exception as e:
        print(f"Failed to fix {filepath}: {e}")

fix_encoding('d:\\My Web Sites\\ProVenture-digital-agency\\services.html')
fix_encoding('d:\\My Web Sites\\ProVenture-digital-agency\\index.html')
