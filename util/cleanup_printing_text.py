import os
import glob
import re

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for target, rep in replacements:
        new_content = new_content.replace(target, rep)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

# Global SEO replacements across all files
global_replacements = [
    ("branding, and printing solutions", "and branding solutions"),
    ("video production, and printing", "and video production"),
    (", printing services Aurangabad", ""),
    ("video production, and printing", "and video production")
]

for html_file in glob.glob('d:\\My Web Sites\\ProVenture-digital-agency\\*.html'):
    replace_in_file(html_file, global_replacements)

# Specific to index.html
replace_in_file('d:\\My Web Sites\\ProVenture-digital-agency\\index.html', [
    ("and printing, we deliver", "we deliver"),
    ("Designs &amp; Printing that Inspire", "Designs that Inspire")
])

# Specific to services.html
# Need to remove the printing grid item
services_html_path = 'd:\\My Web Sites\\ProVenture-digital-agency\\services.html'
with open(services_html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the printing section in services.html grid
# <div class="col-md-6 col-lg-4 d-flex"> ... <h3>Printing</h3> ... </div>
import re
printing_section_regex = re.compile(r'\s*<div class="col-md-6 col-lg-4 d-flex">.*?<h3>Printing</h3>.*?</div>\s*</div>\s*</div>', re.DOTALL)
# It's better to just use a non-greedy match that captures the whole column div.
# But since HTML structure is nested, regex can be tricky. Let's just find the start of the column containing "Printing" and the end.
# A safer way is to let the user know, or write a quick regex that specifically targets the wrapping div.
# Let's inspect services.html first to get the exact HTML if needed, or use a simple replace.
