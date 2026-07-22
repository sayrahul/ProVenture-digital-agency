import os
import glob
import re

def replace_in_file(filepath, replacements, regex_replacements=None):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for target, rep in replacements:
        new_content = new_content.replace(target, rep)
        
    if regex_replacements:
        for pattern, rep in regex_replacements:
            new_content = re.sub(pattern, rep, new_content)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

# Global replacements
global_replacements = [
    ("and print solutions", "and solutions"),
    ("printing services, ", ""),
    (", printing services", ""),
    ("and print campaigns", "and digital campaigns"),
    ("Print &amp; Digital Designs", "Digital Designs"),
    ("Photography for Digital &amp; Print", "Photography for Digital"),
    ("print-ready artwork", "digital artwork"),
    ("Digital or print, online or offline", "Digital campaigns, online or offline")
]

# specific regex replacements
global_regex = [
    (r'We collaborate with trusted partners for printing, signage, and displays,.*?</p>', ''),
    (r'<h3>Business Print</h3>', '<h3>Business Branding</h3>'),
    (r'<strong>Print Media Support</strong>.*?</span>', '<strong>Brand Support</strong></span>'),
    (r'<span>Print Media Support</span>', '<span>Brand Support</span>'),
    (r'<strong>All Print Media Design</strong>.*?</span>', '<strong>All Brand Design</strong></span>'),
    (r'print \+ SEO support', 'SEO support'),
    (r'print media or paid ads', 'paid ads'),
    (r'"Print & Offline Marketing"', '"Offline Marketing"')
]

for html_file in glob.glob('d:\\My Web Sites\\ProVenture-digital-agency\\*.html'):
    replace_in_file(html_file, global_replacements, global_regex)

print("Cleanup complete.")
