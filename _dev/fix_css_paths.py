import os

def fix_css_paths():
    css_file = 'custom/css/main.css'
    
    if not os.path.exists(css_file):
        print(f"Error: {css_file} not found.")
        return

    with open(css_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace "custom/images/" with "../images/"
    # Reason: main.css is in custom/css/. 
    # To get to custom/images/, we need to go up one level (..) then to images/.
    # Path becomes: custom/css/../images/ = custom/images/
    
    new_content = content.replace('custom/images/', '../images/')
    
    # Also handle leading slash if present (unlikely based on my view)
    new_content = new_content.replace('/custom/images/', '../images/')

    if content != new_content:
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed paths in {css_file}")
    else:
        print("No paths needed fixing.")

if __name__ == "__main__":
    fix_css_paths()
