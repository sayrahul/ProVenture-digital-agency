import glob
import re

clean_nav = '''<ul aria-label="Main Website Navigation" class="navigation navigation-level-1">
							<li id="navigation_2" class="pv-has-dropdown">
								<a class="sitemenuitem pv-dropdown-btn" href="about.html">About Us <span class="pv-nav-arrow">▾</span></a>
								<ul class="pv-sub-navigation">
									<li><a href="about.html">About Us</a></li>
									<li><a href="services.html">Services</a></li>
									<li><a href="pricing.html">Pricing</a></li>
								</ul>
							</li>
							<li id="navigation_portfolio"><a class="sitemenuitem" href="https://portfolio.proventure.in/" target="_blank" rel="noopener noreferrer">Portfolio</a></li>
							<li id="navigation_5"><a class="sitemenuitem" href="clients.html">Clients</a></li>
							<li id="navigation_blog"><a class="sitemenuitem" href="blog.html">Blogs</a></li>
							<li id="navigation_6"><a class="sitemenuitem" href="contact.html">Contact Us</a></li>
						</ul>'''

html_files = glob.glob('*.html')
fixed_count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Use regex to find everything from <ul aria-label="Main Website Navigation"... up to <div class="container-big">
    pattern = r'<ul aria-label="Main Website Navigation" class="navigation navigation-level-1">.*?<div class="container-big">'
    
    if re.search(pattern, content, re.DOTALL):
        replacement = clean_nav + '\n\t\t\t\t\t\t<div class="container-big">'
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed_count += 1
        print(f"Fixed navigation in {filepath}")

print(f"Total HTML files fixed: {fixed_count}")
