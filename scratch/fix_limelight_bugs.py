import glob
import re

clean_limelight_html = '''<!-- Mobile Limelight Bottom Nav -->
<nav class="pv-mobile-nav" aria-label="Mobile Navigation">
  <div class="pv-mobile-nav-inner">
    <div class="pv-limelight-bar" id="pv-limelight-bar">
      <div class="pv-limelight-beam"></div>
    </div>
    
    <a href="index.html" class="pv-nav-item pv-nav-home" data-nav="home" aria-label="Home" title="Home">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
    </a>
    <a href="about.html" class="pv-nav-item pv-nav-about" data-nav="about" aria-label="About Us" title="About Us">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
    </a>
    <a href="https://portfolio.proventure.in/" target="_blank" rel="noopener noreferrer" class="pv-nav-item pv-nav-portfolio" data-nav="portfolio" aria-label="Portfolio" title="Portfolio">
      <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
    </a>
    <a href="clients.html" class="pv-nav-item pv-nav-clients" data-nav="clients" aria-label="Clients" title="Clients">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
    </a>
    <a href="blog.html" class="pv-nav-item pv-nav-blog" data-nav="blog" aria-label="Blogs" title="Blogs">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
    </a>
    <a href="contact.html" class="pv-nav-item pv-nav-contact" data-nav="contact" aria-label="Contact Us" title="Contact Us">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81 7A2 2 0 0 1 22 16.92z"/></svg>
    </a>
  </div>
</nav>'''

html_files = glob.glob('*.html')
count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'<nav class="pv-mobile-nav".*?</nav>'
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, clean_limelight_html, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Cleaned Limelight mobile nav in {filepath}")

print(f"Total HTML files updated with Clean Limelight Nav: {count}")
