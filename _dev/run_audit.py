import os
from pathlib import Path
from bs4 import BeautifulSoup

def run_audit(directory):
    html_files = list(Path(directory).rglob("*.html"))
    # Filter out _dev folder and other internal things
    html_files = [f for f in html_files if '_dev' not in str(f) and '.analysis' not in str(f) and 'files' not in str(f) and 'custom' not in str(f)]
    
    report = []
    
    total_pages = len(html_files)
    missing_title = 0
    missing_desc = 0
    missing_h1 = 0
    total_images = 0
    missing_alt = 0
    
    report.append(f"# Complete Audit Report\n")
    report.append(f"## Executive Summary\n")
    
    details = []
    
    for file in sorted(html_files):
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
        except Exception as e:
            details.append(f"### `{file.name}`\n- Error reading file: {e}\n\n")
            continue
            
        # Title
        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else None
        
        # Description
        desc_meta = soup.find('meta', attrs={'name': 'description'})
        desc = desc_meta.get('content', '').strip() if desc_meta else None
        
        # H1
        h1_tags = soup.find_all('h1')
        
        # Images
        img_tags = soup.find_all('img')
        imgs_in_file = len(img_tags)
        total_images += imgs_in_file
        
        missing_alt_in_file = sum(1 for img in img_tags if not img.get('alt') and img.get('alt') != "")
        missing_alt += missing_alt_in_file
        
        if not title: missing_title += 1
        if not desc: missing_desc += 1
        if len(h1_tags) == 0: missing_h1 += 1
        
        file_issues = []
        if not title: file_issues.append("❌ Missing Title")
        elif len(title) < 30 or len(title) > 60: file_issues.append(f"⚠️ Title length ({len(title)}) outside optimal 30-60 range")
        else: file_issues.append(f"✅ Title OK ({len(title)} chars)")
            
        if not desc: file_issues.append("❌ Missing Meta Description")
        elif len(desc) < 120 or len(desc) > 160: file_issues.append(f"⚠️ Description length ({len(desc)}) outside optimal 120-160 range")
        else: file_issues.append(f"✅ Description OK ({len(desc)} chars)")
            
        if len(h1_tags) == 0: file_issues.append("❌ Missing H1")
        elif len(h1_tags) > 1: file_issues.append(f"⚠️ Multiple H1s ({len(h1_tags)})")
        else: file_issues.append("✅ H1 OK")
            
        if missing_alt_in_file > 0: file_issues.append(f"❌ Images missing alt: {missing_alt_in_file}/{imgs_in_file}")
        else: file_issues.append(f"✅ Images OK (Total: {imgs_in_file}, all have alt attribute)")
            
        details.append(f"### `{file.name}`\n")
        for issue in file_issues:
            details.append(f"- {issue}\n")
        details.append("\n")

    report.append(f"- **Total HTML Pages Analyzed:** {total_pages}\n")
    report.append(f"- **Pages missing Title tag:** {missing_title}\n")
    report.append(f"- **Pages missing Meta Description:** {missing_desc}\n")
    report.append(f"- **Pages missing H1 tag:** {missing_h1}\n")
    report.append(f"- **Images missing Alt attribute:** {missing_alt} (out of {total_images} total images)\n\n")
    
    report.append(f"## Page Details\n\n")
    report.extend(details)
    
    with open('current_audit_report.md', 'w', encoding='utf-8') as f:
        f.writelines(report)
        
    print("Audit generated at current_audit_report.md")

if __name__ == "__main__":
    run_audit(os.getcwd())
