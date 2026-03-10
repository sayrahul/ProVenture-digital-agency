import os
import re

def remove_is_loading():
    files = [f for f in os.listdir('.') if f.lower().endswith('.html')]
    count_files = 0
    count_total = 0

    print(f"Checking {len(files)} files...")

    # Regex to remove "is-loading" class, accounting for surrounding spaces
    # It handles: class="... is-loading ..." or class="is-loading"
    # Matches:
    # 1. "is-loading "
    # 2. " is-loading"
    # 3. "is-loading" (only one)
    
    # Simple replace is safer than regex to avoid messing up other classes, 
    # but we need to handle spaces.
    
    for html_file in files:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # We perform 3 replacements to cover edge cases
        new_content = content.replace(' is-loading', '')
        new_content = new_content.replace('is-loading ', '')
        new_content = new_content.replace('is-loading', '') # Fallback for exact match in quotes
        
        if content != new_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Fixed {html_file}")
            count_files += 1
        
    print(f"Removed 'is-loading' from {count_files} files.")

if __name__ == "__main__":
    remove_is_loading()
