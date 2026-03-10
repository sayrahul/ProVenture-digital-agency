import os

# Scripts to inject. Order matters (jQuery first).
SCRIPTS_BLOCK = """
<script src="util/jquery/jquery-3.5.1.slim.min.js"></script>
<script src="util/js/lenis/lenis.min.js"></script>
<script src="util/js/gsap/minified/gsap.min.js"></script>
<script src="util/js/gsap/minified/ScrollTrigger.min.js"></script>
<script src="util/jquery/flickity/flickity.pkgd.min.js"></script>
"""

def inject_scripts():
    files = [f for f in os.listdir('.') if f.endswith('.html')]
    print(f"Scanning {len(files)} HTML files for missing scripts...")
    
    count = 0
    for html_file in files:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Check if already has jQuery (basic check)
        if 'jquery-3.5.1' in content:
            print(f"Skipping {html_file} (already has scripts)")
            continue
            
        # Target: Inject before '<!-- ProVenture Custom JavaScript -->' or 'custom/js/proventure-custom.js'
        # Fallback: Inject before </body>
        
        target_marker = 'custom/js/proventure-custom.js'
        
        if target_marker in content:
            # We want to inject BEFORE the script tag that holds this src
            # Regex or simpler replace? 
            # <script src="custom/js/proventure-custom.js"></script>
            # We can replace the whole line with BLOCK + line
            
            # Simple approach: Find the line with the marker
            lines = content.splitlines()
            new_lines = []
            injected = False
            
            for line in lines:
                if target_marker in line and not injected:
                    # Inject block before this line
                    new_lines.append(SCRIPTS_BLOCK.strip())
                    new_lines.append(line)
                    injected = True
                else:
                    new_lines.append(line)
            
            if injected:
                new_content = '\n'.join(new_lines)
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Injected scripts into {html_file}")
                count += 1
                continue
        
        # Fallback if custom js marker not found
        if '</body>' in content:
            new_content = content.replace('</body>', SCRIPTS_BLOCK + '\n</body>')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Injected scripts into {html_file} (fallback)")
            count += 1

    print(f"Finished. Updated {count} files.")

if __name__ == "__main__":
    inject_scripts()
