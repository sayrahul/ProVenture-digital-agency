import glob

new_nav = '''						<ul aria-label="Main Website Navigation" class="navigation navigation-level-1">
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
updated_count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_str = '<ul aria-label="Main Website Navigation" class="navigation navigation-level-1">'
    end_str = '</ul>'
    
    if start_str in content:
        start_idx = content.find(start_str)
        end_idx = content.find(end_str, start_idx) + len(end_str)
        
        new_content = content[:start_idx] + new_nav + content[end_idx:]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1
        print(f"Updated navigation in {filepath}")

print(f"Total HTML files updated: {updated_count}")
