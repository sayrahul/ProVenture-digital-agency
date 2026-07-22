import os
import glob

html_files = glob.glob('d:\\My Web Sites\\ProVenture-digital-agency\\*.html')

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    target_to_remove = '\n    <a href="pricing.html" class="pv-nav-pricing">\n      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>\n      <span>Pricing</span>\n    </a>'
    
    if target_to_remove in content:
        content = content.replace(target_to_remove, '')
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

print('Done')
