import os
import glob

html_files = glob.glob('d:\\My Web Sites\\ProVenture-digital-agency\\*.html')

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Navbar replace
    target_nav = '<li id="navigation_3"><a class="sitemenuitem" href="services.html">Services</a></li>'
    replace_nav = '<li id="navigation_3"><a class="sitemenuitem" href="services.html">Services</a></li>\n\t\t\t\t\t\t\t<li id="navigation_pricing"><a class="sitemenuitem" href="pricing.html">Pricing</a></li>'
    if target_nav in content:
        content = content.replace(target_nav, replace_nav)

    # Mobile nav replace
    target_mobile_nav = '<a href="services.html" class="pv-nav-services">\n      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2v6"/><path d="M4.2 4.2l4.2 4.2"/><path d="M2 12h6"/><path d="M4.2 19.8l4.2-4.2"/><path d="M12 16v6"/><path d="M19.8 19.8l-4.2-4.2"/><path d="M16 12h6"/><path d="M19.8 4.2l-4.2 4.2"/><circle cx="12" cy="12" r="2"/></svg>\n      <span>Services</span>\n    </a>'
    replace_mobile_nav = target_mobile_nav + '\n    <a href="pricing.html" class="pv-nav-pricing">\n      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>\n      <span>Pricing</span>\n    </a>'
    if target_mobile_nav in content:
        content = content.replace(target_mobile_nav, replace_mobile_nav)
        
    # Footer replace
    target_footer = 'Terms &amp;\n\t\t\t\t\t\t\t\t\tConditions</a>'
    replace_footer = target_footer + '\n\t\t\t\t\t\t\t\t-\n\t\t\t\t\t\t\t\t<a class="pagelink" href="pricing.html" title="ProVenture Digital Agency - Pricing">Pricing</a>'
    if target_footer in content:
        content = content.replace(target_footer, replace_footer)

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
print('Done')
