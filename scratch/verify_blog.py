import os
import re

with open('blog.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Check images
imgs = re.findall(r'src="([^"]+)"', html)
missing_imgs = [img for img in set(imgs) if not img.startswith('http') and not img.startswith('data:') and not os.path.exists(img)]

print("Missing image paths in blog.html:", missing_imgs)

# 2. Check modal matching
modal_triggers = re.findall(r"openBlogModal\('([^']+)'\)", html)
modal_divs = re.findall(r'id="(blog-modal-\d+)"', html)

missing_modals = [m for m in set(modal_triggers) if m not in modal_divs]
print("Triggers without modal DIVs:", missing_modals)

# 3. Check for any syntax errors or unclosed tags in modals
print("Total Blog Triggers:", len(modal_triggers))
print("Total Modal DIVs:", len(modal_divs))
