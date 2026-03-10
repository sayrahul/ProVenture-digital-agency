import os
import re
from html.parser import HTMLParser

class AuditHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = None
        self.in_title = False
        self.description = None
        self.h1_count = 0
        self.images_total = 0
        self.images_missing_alt = 0
        
    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            attr_dict = dict(attrs)
            if attr_dict.get("name", "").lower() == "description":
                self.description = attr_dict.get("content", "")
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "img":
            self.images_total += 1
            attr_dict = dict(attrs)
            if "alt" not in attr_dict or not attr_dict["alt"].strip():
                self.images_missing_alt += 1

    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
            
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

def analyze_directory(root_dir):
    report_lines = []
    report_lines.append("# Website SEO & Content Audit Report\n")
    report_lines.append("## Executive Summary\n")
    
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.venv' in dirs:
            dirs.remove('.venv')
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    total_pages = len(html_files)
    missing_title = 0
    missing_desc = 0
    missing_h1 = 0
    total_images = 0
    total_missing_alt = 0
    
    page_details = []

    for file_path in html_files:
        rel_path = os.path.relpath(file_path, root_dir)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
            
        parser = AuditHTMLParser()
        parser.feed(content)
        
        has_title = bool(parser.title)
        has_desc = bool(parser.description)
        has_h1 = parser.h1_count > 0
        
        if not has_title: missing_title += 1
        if not has_desc: missing_desc += 1
        if not has_h1: missing_h1 += 1
        
        total_images += parser.images_total
        total_missing_alt += parser.images_missing_alt
        
        page_details.append({
            "path": rel_path,
            "title": parser.title,
            "desc_len": len(parser.description) if parser.description else 0,
            "h1_count": parser.h1_count,
            "img_total": parser.images_total,
            "img_missing_alt": parser.images_missing_alt
        })
        
    report_lines.append(f"- **Total HTML Pages Analyzed:** {total_pages}")
    report_lines.append(f"- **Pages missing Title tag:** {missing_title}")
    report_lines.append(f"- **Pages missing Meta Description:** {missing_desc}")
    report_lines.append(f"- **Pages missing H1 tag:** {missing_h1}")
    report_lines.append(f"- **Images missing Alt attribute:** {total_missing_alt} (out of {total_images} total images)\n")
    
    report_lines.append("## Page Details\n")
    for detail in sorted(page_details, key=lambda x: x['path']):
        report_lines.append(f"### `{detail['path']}`")
        if detail['title']:
            report_lines.append(f"- **Title:** {detail['title']} ({len(detail['title'])} chars)")
            if len(detail['title']) < 30 or len(detail['title']) > 60:
                report_lines.append("  - ⚠️ *Warning: Title length is outside optimal range (30-60 chars).*")
        else:
            report_lines.append("- **Title:** ❌ Missing")
            
        if detail['desc_len'] > 0:
            report_lines.append(f"- **Description Length:** {detail['desc_len']} chars")
            if detail['desc_len'] < 120 or detail['desc_len'] > 160:
                report_lines.append("  - ⚠️ *Warning: Description length is outside optimal range (120-160 chars).*")
        else:
            report_lines.append("- **Description:** ❌ Missing")
            
        if detail['h1_count'] == 1:
            report_lines.append(f"- **H1 Tags:** {detail['h1_count']}")
        elif detail['h1_count'] > 1:
            report_lines.append(f"- **H1 Tags:** {detail['h1_count']} (⚠️ Multiple H1s)")
        else:
            report_lines.append(f"- **H1 Tags:** ❌ 0 (Missing H1)")
            
        if detail['img_total'] > 0:
            report_lines.append(f"- **Images:** {detail['img_total']} (Missing Alt: {detail['img_missing_alt']})")
            if detail['img_missing_alt'] > 0:
                report_lines.append("  - ⚠️ *Warning: Some images are missing alt attributes (accessibility issue).*")
        else:
             report_lines.append(f"- **Images:** 0")
        report_lines.append("")

    with open(os.path.join(root_dir, "audit_report.md"), "w", encoding='utf-8') as f:
        f.write("\n".join(report_lines))
        
    print(f"Audit completed: processed {total_pages} files.")
    print("Report saved to audit_report.md")

if __name__ == "__main__":
    analyze_directory(os.getcwd())
