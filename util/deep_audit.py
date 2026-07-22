import os
import re
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from datetime import datetime

class PageParser(HTMLParser):
    def __init__(self, page_url):
        super().__init__()
        self.page_url = page_url
        self.title = None
        self.in_title = False
        self.meta_description = None
        self.canonical = None
        self.h1_tags = []
        self.in_h1 = False
        self.current_h1_content = []
        self.links = []
        self.resources = [] # images, styles, scripts, videos, etc.
        self.images = [] # specifically track images with alt tags
        
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            if attr_dict.get("name", "").lower() == "description":
                self.meta_description = attr_dict.get("content", "")
        elif tag == "link":
            rel = attr_dict.get("rel", "").lower()
            href = attr_dict.get("href")
            if href:
                if rel == "canonical":
                    self.canonical = href
                elif rel in ["stylesheet", "icon", "shortcut icon", "apple-touch-icon"]:
                    self.resources.append((tag, href))
                elif rel in ["preconnect", "dns-prefetch"]:
                    # skip preconnect/dns-prefetch domain checks
                    pass
                else:
                    # other links (preload, etc.)
                    self.resources.append((tag, href))
        elif tag == "script":
            src = attr_dict.get("src")
            if src:
                self.resources.append((tag, src))
        elif tag == "a":
            href = attr_dict.get("href")
            if href:
                self.links.append(href)
        elif tag in ["img", "source", "video", "iframe"]:
            src = attr_dict.get("src") or attr_dict.get("data-src")
            if src:
                self.resources.append((tag, src))
            if tag == "img":
                alt = attr_dict.get("alt")
                self.images.append({
                    "src": src or "unknown",
                    "alt": alt,
                    "has_alt": "alt" in attr_dict,
                    "alt_empty": alt is not None and not alt.strip()
                })
        elif tag == "h1":
            self.in_h1 = True
            self.current_h1_content = []

    def handle_data(self, data):
        if self.in_title:
            self.title = (self.title or "") + data
        elif self.in_h1:
            self.current_h1_content.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
            if self.title:
                self.title = self.title.strip()
        elif tag == "h1":
            self.in_h1 = False
            h1_text = "".join(self.current_h1_content).strip()
            if h1_text:
                self.h1_tags.append(h1_text)

def check_url(url):
    """Checks a URL and returns (status_code, error_msg)"""
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProVentureAudit/1.0'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status, None
    except urllib.error.HTTPError as e:
        return e.code, str(e)
    except Exception as e:
        return 0, str(e)

def perform_deep_audit(base_url, output_file):
    print(f"Starting deep audit of {base_url}...")
    
    # Track crawled pages and resource status
    crawled_pages = {} # url -> parsed data
    checked_resources = {} # url -> (status, error)
    external_links = set()
    queue = [base_url]
    
    # Normalize base url
    parsed_base = urllib.parse.urlparse(base_url)
    base_host = parsed_base.netloc
    
    while queue:
        current_url = queue.pop(0)
        # Strip query parameters or anchors for deduplication
        clean_url = current_url.split('?')[0].split('#')[0]
        if clean_url in crawled_pages:
            continue
            
        print(f"Crawling: {clean_url}")
        try:
            req = urllib.request.Request(
                clean_url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ProVentureAudit/1.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
                status = response.status
        except Exception as e:
            print(f"Failed to fetch page {clean_url}: {e}")
            crawled_pages[clean_url] = {"error": str(e), "status": 0}
            continue
            
        # Parse page
        parser = PageParser(clean_url)
        try:
            parser.feed(html_content)
        except Exception as e:
            print(f"Error parsing HTML of {clean_url}: {e}")
            
        crawled_pages[clean_url] = {
            "status": status,
            "title": parser.title,
            "description": parser.meta_description,
            "canonical": parser.canonical,
            "h1_tags": parser.h1_tags,
            "links": parser.links,
            "resources": parser.resources,
            "images": parser.images
        }
        
        # Process links
        for link in parser.links:
            # Skip mailto, tel, javascript, anchors
            if link.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                continue
                
            # Resolve relative URLs
            resolved_url = urllib.parse.urljoin(clean_url, link)
            parsed_resolved = urllib.parse.urlparse(resolved_url)
            
            # Check if internal
            if parsed_resolved.netloc == base_host:
                resolved_clean = resolved_url.split('?')[0].split('#')[0]
                if resolved_clean not in crawled_pages and resolved_clean not in queue:
                    # Only queue actual HTML pages
                    if not any(resolved_clean.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.mp4']):
                        queue.append(resolved_clean)
            else:
                external_links.add(resolved_url)
                
        # Process resources
        for tag, src in parser.resources:
            if src.startswith(('data:', 'mailto:', 'tel:', 'javascript:', '#')):
                continue
            resolved_resource = urllib.parse.urljoin(clean_url, src)
            if resolved_resource not in checked_resources:
                print(f"  Checking resource: {src}")
                status, err = check_url(resolved_resource)
                checked_resources[resolved_resource] = (status, err)

    # Let's write the report
    print("Generating report...")
    report = []
    report.append("# ProVenture Deep Audit & Health Report\n")
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # 1. Executive Summary
    total_pages = len(crawled_pages)
    failed_pages = sum(1 for p in crawled_pages.values() if p.get("status", 0) != 200)
    
    # Find broken resources
    broken_resources = {url: val for url, val in checked_resources.items() if val[0] != 200}
    
    # Find SEO issues
    pages_missing_title = 0
    pages_missing_desc = 0
    pages_missing_h1 = 0
    pages_multiple_h1 = 0
    pages_bad_title_len = 0
    pages_bad_desc_len = 0
    total_images_checked = 0
    images_missing_alt = 0
    
    for url, data in crawled_pages.items():
        if data.get("status") != 200:
            continue
        
        title = data.get("title")
        desc = data.get("description")
        h1s = data.get("h1_tags", [])
        
        # Don't audit references/helpers for standard stats
        if "seo-enhancements.html" in url or "pricing-backup.html" in url:
            continue
            
        if not title:
            pages_missing_title += 1
        elif len(title) < 30 or len(title) > 60:
            pages_bad_title_len += 1
            
        if not desc:
            pages_missing_desc += 1
        elif len(desc) < 120 or len(desc) > 160:
            pages_bad_desc_len += 1
            
        if not h1s:
            pages_missing_h1 += 1
        elif len(h1s) > 1:
            pages_multiple_h1 += 1
            
        for img in data.get("images", []):
            total_images_checked += 1
            if not img.get("has_alt") or img.get("alt_empty"):
                images_missing_alt += 1
                
    report.append("## 📊 Executive Summary\n")
    report.append(f"- **Total Crawled Pages:** {total_pages}")
    report.append(f"- **Failed Pages (Non-200):** {failed_pages}")
    report.append(f"- **Broken Assets/Resources:** {len(broken_resources)}")
    report.append(f"- **SEO Alerts:**")
    report.append(f"  - Pages missing Title: {pages_missing_title}")
    report.append(f"  - Pages with non-optimal Title length (30-60 chars): {pages_bad_title_len}")
    report.append(f"  - Pages missing Meta Description: {pages_missing_desc}")
    report.append(f"  - Pages with non-optimal Description length (120-160 chars): {pages_bad_desc_len}")
    report.append(f"  - Pages missing H1 tag: {pages_missing_h1}")
    report.append(f"  - Pages with multiple H1 tags: {pages_multiple_h1}")
    report.append(f"  - Images missing `alt` description: {images_missing_alt} (out of {total_images_checked})\n")
    
    # 2. Broken Assets Section
    report.append("## ❌ Broken Assets & Resources\n")
    if broken_resources:
        report.append("| Resource URL | Tag/Type | Status Code | Error Message | Found On Pages |")
        report.append("|---|---|---|---|---|")
        for res_url, (status, err) in broken_resources.items():
            # Find pages referencing this resource
            referencing_pages = []
            for page_url, p_data in crawled_pages.items():
                if p_data.get("status") != 200:
                    continue
                for tag, src in p_data.get("resources", []):
                    resolved_src = urllib.parse.urljoin(page_url, src)
                    if resolved_src == res_url:
                        referencing_pages.append(os.path.basename(page_url) or "/")
                        
            ref_str = ", ".join(set(referencing_pages))
            rel_res_url = res_url.replace(base_url, "")
            report.append(f"| `{rel_res_url}` | Asset | {status} | {err} | {ref_str} |")
        report.append("\n")
    else:
        report.append("✅ No broken assets or resources found!\n")
        
    # 3. Detailed Page Audit
    report.append("## 📄 Detailed Page Analysis\n")
    for url, data in sorted(crawled_pages.items()):
        page_name = os.path.basename(url) or "Home (index.html)"
        report.append(f"### 🌐 {page_name}\n")
        report.append(f"- **URL:** `{url}`")
        
        if data.get("status") != 200:
            report.append(f"- **Status:** ❌ Failed ({data.get('status')}) - {data.get('error')}\n")
            continue
            
        report.append(f"- **Status:** Live (200 OK)")
        
        # Title Check
        title = data.get("title")
        if title:
            t_len = len(title)
            t_status = "✅" if 30 <= t_len <= 60 else "⚠️ Length warning"
            report.append(f"- **Title:** \"{title}\" ({t_len} chars) - {t_status}")
        else:
            report.append("- **Title:** ❌ Missing")
            
        # Description Check
        desc = data.get("description")
        if desc:
            d_len = len(desc)
            d_status = "✅" if 120 <= d_len <= 160 else "⚠️ Length warning"
            report.append(f"- **Meta Description:** \"{desc}\" ({d_len} chars) - {d_status}")
        else:
            report.append("- **Meta Description:** ❌ Missing")
            
        # H1 Check
        h1s = data.get("h1_tags", [])
        if h1s:
            h1s_str = ", ".join([f"\"{h}\"" for h in h1s])
            if len(h1s) > 1:
                report.append(f"- **H1 Tags:** ⚠️ Multiple ({len(h1s)} found): {h1s_str}")
            else:
                report.append(f"- **H1 Tag:** ✅ {h1s_str}")
        else:
            report.append("- **H1 Tag:** ❌ Missing")
            
        # Images Alt Check
        imgs = data.get("images", [])
        missing_alt_imgs = [i for i in imgs if not i.get("has_alt") or i.get("alt_empty")]
        if imgs:
            if missing_alt_imgs:
                report.append(f"- **Images:** Total {len(imgs)} | ⚠️ Missing Alt: {len(missing_alt_imgs)}")
                for mi in missing_alt_imgs[:5]:
                    report.append(f"  - `src=\"{mi.get('src')}\"`")
                if len(missing_alt_imgs) > 5:
                    report.append(f"  - ...and {len(missing_alt_imgs) - 5} more")
            else:
                report.append(f"- **Images:** Total {len(imgs)} | ✅ All have Alt attributes")
        else:
            report.append("- **Images:** None")
            
        # Canonical Check
        canonical = data.get("canonical")
        if canonical:
            report.append(f"- **Canonical Link:** `{canonical}`")
        else:
            report.append("- **Canonical Link:** ❌ Missing")
            
        report.append("")
        
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print(f"Deep audit completed! Report saved to {output_file}")

if __name__ == "__main__":
    perform_deep_audit("http://localhost:8000/", "deep_audit_report.md")
