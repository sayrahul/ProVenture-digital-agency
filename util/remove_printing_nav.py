import os
import glob
import re

html_files = glob.glob('d:\\My Web Sites\\ProVenture-digital-agency\\*.html')

# Regexes
nav_regex = re.compile(r'\s*<div class="servicenav-item" data-img="\.img-2">\s*<a href="digital-printing\.html">.*?</ul>\s*</div>', re.DOTALL)
img_regex = re.compile(r'\s*<img alt="[^"]+" class="img-fluid img-thumbnail img-2".*?/>', re.DOTALL)
# For mobile nav which we already modified, let's make sure it's gone. Wait, the user asked to remove "printing service from entire site". I didn't see "printing" in mobile nav, it was services and pricing. 

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = nav_regex.sub('', content)
    new_content = img_regex.sub('', new_content)

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)

print('Done')
