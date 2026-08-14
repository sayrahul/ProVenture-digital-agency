import glob
import time

timestamp = int(time.time())
html_files = glob.glob('*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update CSS query string version to force browser cache invalidation
    new_content = content.replace('proventure-custom.css?v=20260308', f'proventure-custom.css?v={timestamp}')
    new_content = new_content.replace('default-20252e34.css?v=112', f'default-20252e34.css?v={timestamp}')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated cache bust version in {filepath}")

print("Cache busting version update completed!")
