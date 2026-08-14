import glob
import re

android_5slot_nav_html = '''<!-- Android Curved FAB Bottom Navigation -->
<nav class="pv-android-nav" aria-label="Mobile Navigation">
  <div class="pv-android-nav-bar">
    <svg class="pv-android-nav-bg" viewBox="0 0 375 64" preserveAspectRatio="none">
      <path d="M 0 16 C 0 7.16 7.16 0 16 0 L 135 0 C 145 0 152 6 156 14 C 164 32 211 32 219 14 C 223 6 230 0 240 0 L 359 0 C 367.84 0 375 7.16 375 16 L 375 48 C 375 56.84 367.84 64 359 64 L 16 64 C 7.16 64 0 56.84 0 48 Z" fill="#ffffff"/>
    </svg>

    <div class="pv-android-nav-items">
      <a href="index.html" class="pv-android-item" data-nav="home" aria-label="Home" title="Home">
        <svg viewBox="0 0 24 24"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        <span class="pv-active-dot"></span>
      </a>

      <a href="about.html" class="pv-android-item" data-nav="about" aria-label="About Us" title="About Us">
        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
        <span class="pv-active-dot"></span>
      </a>

      <a href="https://portfolio.proventure.in/" target="_blank" rel="noopener noreferrer" class="pv-android-fab" data-nav="portfolio" aria-label="Portfolio" title="Portfolio">
        <div class="pv-fab-circle">
          <svg viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
        </div>
      </a>

      <a href="clients.html" class="pv-android-item" data-nav="clients" aria-label="Clients" title="Clients">
        <svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        <span class="pv-active-dot"></span>
      </a>

      <a href="contact.html" class="pv-android-item" data-nav="contact" aria-label="Contact" title="Contact">
        <svg viewBox="0 0 24 24"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
        <span class="pv-active-dot"></span>
      </a>
    </div>
  </div>
</nav>'''

html_files = glob.glob('*.html')
count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'<nav class="pv-android-nav".*?</nav>'
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, android_5slot_nav_html, content, flags=re.DOTALL)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Fixed Contact SVG in {filepath}")

print(f"Total HTML files updated: {count}")
