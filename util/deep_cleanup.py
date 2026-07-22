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

global_replacements = [
    ("Production &amp; Print", "Digital Production"),
    ("Production & Print", "Digital Production"),
    ("digital marketing, branding, printing, and video solutions we offer", "digital marketing, branding, and video solutions we offer"),
    ("Traditional advertising (print materials, outdoor ads, etc.)", "Omnichannel digital campaigns"),
    ("brochure design, packaging design", "UI/UX design, digital assets"),
    ("Brochure/Flyer/Banner", "Digital Ads &amp; Web Banners"),
    ("Mailers (digital &amp; print)", "Email Newsletters &amp; Outreach"),
    ("Mailers (digital & print)", "Email Newsletters & Outreach"),
    ("Advertising Print", "Advertising Creatives"),
    ("Print advertisements", "Digital advertisements"),
    ("Brochures &amp; catalogues", "Interactive e-catalogues"),
    ("Flyers &amp; folders", "Social media assets"),
    ("Product packaging &amp; labels", "Digital branding kits"),
    ("Premium Print Solutions", "Premium Digital Solutions"),
    ("digital and print", "digital")
]

global_regex = [
    # index.html
    (r'From cinematic video production and professional photography to premium print.*?,', 'From cinematic video production to professional photography,'),
    (r'digital marketing, video production, and premium print,', 'digital marketing and video production,'),
    (r'creativity, strategy, and innovation to craft powerful digital and print\s*experiences\.', 'creativity, strategy, and innovation to craft powerful digital experiences.'),
    # contact.html removal of the checkbox
    (r'<div class="form-check pb-2">\s*<input class="form-check-input".*?value="Printing: Custom Print Solutions".*?</div>', '')
]

for html_file in glob.glob('d:\\My Web Sites\\ProVenture-digital-agency\\*.html'):
    replace_in_file(html_file, global_replacements, global_regex)

print("Deep cleanup complete.")
