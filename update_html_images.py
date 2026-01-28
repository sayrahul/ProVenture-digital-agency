import re
import os

def update_html_files():
    # Get all HTML files
    files = [f for f in os.listdir('.') if f.lower().endswith('.html')]
    print(f"Found {len(files)} HTML files to process.")

    # Regex to find thumbnails/... .(jpg|png)
    pattern = r'(thumbnails/[^"\']+\.)(jpg|jpeg|png)'
    
    def replacer(match):
        base = match.group(1)
        return f"{base}webp"

    total_updated = 0

    for html_file in files:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        new_content, count = re.subn(pattern, replacer, content, flags=re.IGNORECASE)
        
        if count > 0:
            # Backup optional effectively disabled for batch to save space/time, 
            # or we could do it. Let's skip backup for batch to allow fast iteration 
            # as these are simple string replacements.
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {count} links in {html_file}")
            total_updated += 1
        else:
            # print(f"No changes in {html_file}")
            pass

    print(f"Finished. Updated {total_updated} files.")

if __name__ == "__main__":
    update_html_files()
