import glob
import re

limelight_nav_html = '''<!-- Mobile Limelight Bottom Nav -->
<nav class="pv-mobile-nav" aria-label="Mobile Navigation">
  <div class="pv-mobile-nav-inner">
    <div class="pv-limelight-bar" id="pv-limelight-bar">
      <div class="pv-limelight-beam"></div>
    </div>
    
    <a href="index.html" class="pv-nav-item pv-nav-home" data-nav="home">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 10.5L12 3l9 7.5"/><path d="M5 10.5V21h14V10.5"/></svg>
      <span>Home</span>
    </a>
    <a href="about.html" class="pv-nav-item pv-nav-about" data-nav="about">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="7" r="3"/><path d="M5 21a7 7 0 0 1 14 0"/></svg>
      <span>About</span>
    </a>
    <a href="https://portfolio.proventure.in/" target="_blank" rel="noopener noreferrer" class="pv-nav-item pv-nav-portfolio" data-nav="portfolio">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
      <span>Portfolio</span>
    </a>
    <a href="clients.html" class="pv-nav-item pv-nav-clients" data-nav="clients">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M2 21a6 6 0 0 1 12 0"/><path d="M10 21a6 6 0 0 1 12 0"/></svg>
      <span>Clients</span>
    </a>
    <a href="blog.html" class="pv-nav-item pv-nav-blog" data-nav="blog">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
      <span>Blogs</span>
    </a>
    <a href="contact.html" class="pv-nav-item pv-nav-contact" data-nav="contact">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h16v12H8l-4 4V4z"/></svg>
      <span>Contact</span>
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
        new_content = re.sub(pattern, limelight_nav_html, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Updated Limelight mobile nav in {filepath}")

print(f"Total HTML files updated with Limelight Nav: {count}")
