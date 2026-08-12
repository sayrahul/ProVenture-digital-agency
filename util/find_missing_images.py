import os
import re
from urllib.parse import urlparse, unquote

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Regex patterns to catch various asset references
img_src_pattern = re.compile(r'src=["\']([^"\']+)["\']', re.IGNORECASE)
data_src_pattern = re.compile(r'data-src=["\']([^"\']+)["\']', re.IGNORECASE)
srcset_pattern = re.compile(r'srcset=["\']([^"\']+)["\']', re.IGNORECASE)
css_url_pattern = re.compile(r'url\s*\(\s*["\']?([^"\')]+)["\']?\s*\)', re.IGNORECASE)

missing_assets = []
checked_assets = set()

def check_asset(asset_url, source_file):
    if asset_url.startswith('data:') or asset_url.startswith('http://') or asset_url.startswith('https://') or asset_url.startswith('//'):
        return # Skip data URIs and external URLs
    
    # Remove query params and fragments
    parsed = urlparse(asset_url)
    clean_path = unquote(parsed.path)
    
    if not clean_path:
        return

    # Check absolute vs relative
    if clean_path.startswith('/'):
        # Absolute to domain root, which is base_dir
        local_path = os.path.join(base_dir, clean_path.lstrip('/'))
    else:
        # Relative to the file
        local_path = os.path.join(os.path.dirname(source_file), clean_path)
    
    local_path = os.path.normpath(local_path)
    
    # Deduplicate checks
    check_key = (local_path, source_file)
    if check_key in checked_assets:
        return
    checked_assets.add(check_key)
    
    if not os.path.exists(local_path):
        missing_assets.append({
            'file': os.path.relpath(source_file, base_dir),
            'asset': asset_url,
            'resolved_path': os.path.relpath(local_path, base_dir)
        })

# Check HTML files
for root, dirs, files in os.walk(base_dir):
    for fname in files:
        if fname.endswith('.html') or fname.endswith('.css'):
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Extract from src
                    for match in img_src_pattern.finditer(content):
                        check_asset(match.group(1), fpath)
                        
                    # Extract from data-src
                    for match in data_src_pattern.finditer(content):
                        check_asset(match.group(1), fpath)
                        
                    # Extract from srcset (needs splitting by comma, then space)
                    for match in srcset_pattern.finditer(content):
                        srcset_val = match.group(1)
                        for src_part in srcset_val.split(','):
                            src_url = src_part.strip().split(' ')[0]
                            if src_url:
                                check_asset(src_url, fpath)
                                
                    # Extract from css url()
                    for match in css_url_pattern.finditer(content):
                        check_asset(match.group(1), fpath)
                        
            except Exception as e:
                print(f"Error reading {fpath}: {e}")

if not missing_assets:
    print("All local image/asset references are intact! Zero missing files.")
else:
    print(f"Found {len(missing_assets)} missing asset references:")
    for missing in missing_assets:
        print(f"  - In {missing['file']}: {missing['asset']} (Expected at: {missing['resolved_path']})")
