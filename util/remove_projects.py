import os
import re

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. Delete projects.html if exists
projects_file = os.path.join(base_dir, "projects.html")
if os.path.exists(projects_file):
    os.remove(projects_file)
    print("Deleted projects.html")

# 2. Clean all references in .html files
html_files = [f for f in os.listdir(base_dir) if f.endswith(".html")]

nav_pattern1 = re.compile(r'<li\s+id="navigation_4">\s*<a\s+class="sitemenuitem[^"]*"\s+href="projects\.html">Projects</a>\s*</li>', re.IGNORECASE)
nav_pattern2 = re.compile(r'<li\s+id="navigation_4">\s*<a\s+class="sitemenuitem[^"]*"\s+href="projects\.html">Projects</a>\s*\n?\s*</li>?', re.IGNORECASE)
see_all_pattern = re.compile(r'<a\s+class="pagelink\s+lnk\s+lnk-black\s+scroll-el"\s+href="projects\.html"[^>]*>See All Projects</a>', re.IGNORECASE)

modified_count = 0
for fname in html_files:
    fpath = os.path.join(base_dir, fname)
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    new_content = nav_pattern1.sub("", content)
    new_content = nav_pattern2.sub("", new_content)
    new_content = see_all_pattern.sub("", new_content)
    
    # Also fallback regex if any whitespace variation exists
    new_content = re.sub(r'<li\s+id="navigation_4">.*?projects\.html.*?</li>', '', new_content, flags=re.DOTALL | re.IGNORECASE)
    
    if new_content != content:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_content)
        modified_count += 1
        print(f"Updated {fname}")

print(f"Cleanup finished. Modified {modified_count} files.")
