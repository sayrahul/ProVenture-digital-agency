import os

# 1. Update proventure-custom.css
with open('custom/css/proventure-custom.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('&family=Playfair+Display:wght@600;700', '')
css = css.replace('"Playfair Display", Georgia, serif', "'Outfit', sans-serif")
css = css.replace("'Playfair Display', Georgia, serif", "'Outfit', sans-serif")

# Ensure .blog-title has explicit Outfit font
if '.blog-title {' in css:
    css = css.replace('.blog-title {\n', ".blog-title {\n    font-family: 'Outfit', sans-serif !important;\n")

with open('custom/css/proventure-custom.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update pricing.html
if os.path.exists('pricing.html'):
    with open('pricing.html', 'r', encoding='utf-8') as f:
        p_html = f.read()
    p_html = p_html.replace('family=Playfair+Display:ital,wght@0,400..900;1,400..900&', '')
    with open('pricing.html', 'w', encoding='utf-8') as f:
        f.write(p_html)

print("Playfair Display font has been completely removed across the project!")
