import glob
import re

html_files = glob.glob('*.html')
count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'<!-- Mobile Limelight Bottom Nav -->\s*<nav class="pv-mobile-nav".*?</nav>'
    pattern2 = r'<nav class="pv-mobile-nav".*?</nav>'
    
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)
    new_content = re.sub(pattern2, '', new_content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Removed bottom navbar from {filepath}")

print(f"Total HTML files updated: {count}")
