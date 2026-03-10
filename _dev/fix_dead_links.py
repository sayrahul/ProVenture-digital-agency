
import os
import re

def fix_dead_links(root_dir):
    print(f"Fixing dead links in {root_dir}...")
    
    patterns = [
        (r'href="[^"]*md/creation/[^"]*"', 'href="#"'),
        (r'href="[^"]*kreation/[^"]*"', 'href="#"'),
        (r'href="[^"]*audit-site-web/[^"]*"', 'href="contact.html"'),
        (r'href="[^"]*applications/systemes-de-gestion-des-contenus/[^"]*"', 'href="#"'),
        (r'href="[^"]*blog/news-actualites/[^"]*"', 'href="#"'),
        (r'href="[^"]*services/index.html"', 'href="services.html"'),
        (r'href="[^"]*md/[^"]*"', 'href="#"'),
        (r'href="[^"]*ihr-projekt-formular/[^"]*"', 'href="#"'),
        (r'href="[^"]*digital-marketing/index.html"', 'href="digital-marketing.html"'),
        (r'href="[^"]*e-mail-marketing/index.html"', 'href="#"'),
        (r'href="[^"]*seo-referencement-naturel/index.html"', 'href="#"'),
        (r'href="[^"]*social-media/index.html"', 'href="social-media.html"'),
        (r'href="[^"]*strategie/index.html"', 'href="#"'),
        (r'href="[^"]*publicite-en-ligne/index.html"', 'href="online-advertising.html"'),
        (r'href="[^"]*blog/web-marketing/[^"]*"', 'href="#"'),
        # Remove link rel=alternate tags entirely
        (r'<link[^>]+href="[^"]*md/[^"]*"[^>]*>', ''),
        (r'<link[^>]+href="[^"]*kreation/[^"]*"[^>]*>', '')
    ]

    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    for pattern, replacement in patterns:
                        content = re.sub(pattern, replacement, content)
                    
                    if content != original_content:
                        print(f"Fixed dead links in {file}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    fix_dead_links(os.getcwd())
