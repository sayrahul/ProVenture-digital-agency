import os
from bs4 import BeautifulSoup

def standardize_buttons():
    root_dir = r"c:\My Web Sites\ProVenture-digital-agency"
    
    # Standard class for "Call us now" buttons
    STANDARD_CLASSES = ["btn", "btn-outline", "pv-btn-primary"]
    STANDARD_HREF = "tel:+919595997711"
    
    count_files = 0
    count_total_buttons = 0
    count_magnetic_removed = 0
    
    for filename in os.listdir(root_dir):
        if filename.endswith(".html"):
            filepath = os.path.join(root_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            modified = False
            
            # 1. Remove pv-magnetic from ALL elements
            magnetic_elements = soup.find_all(class_="pv-magnetic")
            if magnetic_elements:
                for el in magnetic_elements:
                    el['class'] = [c for c in el['class'] if c != 'pv-magnetic']
                    count_magnetic_removed += 1
                    modified = True
            
            # 2. Standardize "Call us now" buttons
            # We look for <a> tags with text "Call us now" (case insensitive)
            links = soup.find_all('a')
            for link in links:
                # Get clean text
                text = link.get_text(strip=True).lower()
                
                if "call us now" in text:
                    # Update classes
                    # We preserve other classes if they are seemingly structural (like 'nav-link' maybe?) 
                    # But user said "same version", so replace is safer.
                    # However, let's just force the specific visual classes.
                    
                    link['class'] = STANDARD_CLASSES
                    link['href'] = STANDARD_HREF
                    link['title'] = "ProVenture Digital Agency" # Standardize title too? Optional, keeping it simple.
                    
                    count_total_buttons += 1
                    modified = True
            
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                print(f"Updated: {filename}")
                count_files += 1
                
    print(f"\nSummary:")
    print(f"Files updated: {count_files}")
    print(f"Magnetic classes removed: {count_magnetic_removed}")
    print(f"Buttons standardized: {count_total_buttons}")

if __name__ == "__main__":
    standardize_buttons()
