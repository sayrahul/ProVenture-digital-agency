
import os
import re
from urllib.parse import unquote, urlparse

def check_integrity(root_dir):
    print(f"Scanning {root_dir}...")
    errors = []
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            errors.append(f"Could not read {file_path}: {e}")
            continue

        # Find all src and href attributes
        # This regex is simple and might miss some edge cases but should catch most
        links = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', content)
        
        for link in links:
            if link.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'javascript:')):
                continue
            
            # Remove query params and anchors
            clean_link = link.split('?')[0].split('#')[0]
            if not clean_link:
                continue

            # Absolute path from root (starts with /)
            if clean_link.startswith('/'):
                target_path = os.path.join(root_dir, clean_link[1:])
            else:
                # Relative path
                target_path = os.path.join(os.path.dirname(file_path), clean_link)
            
            # Decode URL encoding (e.g. %20)
            target_path = unquote(target_path)
            
            if not os.path.exists(target_path):
                # Try checking if it's a directory index
                if os.path.isdir(target_path) and os.path.exists(os.path.join(target_path, 'index.html')):
                    continue
                    
                rel_file = os.path.relpath(file_path, root_dir)
                errors.append(f"Missing resource in {rel_file}: {link}")

    if errors:
        print(f"Found {len(errors)} potential issues:")
        for err in errors:
            print(err)
    else:
        print("No broken internal links found!")

if __name__ == "__main__":
    check_integrity(os.getcwd())
