import os

CSS_LINK = '<link href="custom/css/main.css" rel="stylesheet" type="text/css"/>'
CUSTOM_CSS_LINK = '<link href="custom/css/proventure-custom.css" rel="stylesheet" type="text/css"/>'

# Target replacement point: usually before </head> or after other CSS links.
# Let's insert before </head> for simplicity, or replace an existing style block if found (risky).
# Safest: Insert before </head>.

def standardize_css():
    files = [f for f in os.listdir('.') if f.lower().endswith('.html')]
    print(f"Found {len(files)} HTML files.")

    for html_file in files:
        # separate handling for index.html as we already did it manually
        if html_file == 'index.html':
            continue

        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if "custom/css/main.css" in content:
            print(f"Skipping {html_file} (already has main.css)")
            continue

        # Check for </head>
        if "</head>" in content:
            # Inject before </head>
            # Add main.css
            # Add custom.css if missing
            injection = "\n" + CSS_LINK + "\n"
            if "custom/css/proventure-custom.css" not in content:
                injection += CUSTOM_CSS_LINK + "\n"
            
            new_content = content.replace("</head>", injection + "</head>")
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Standardized {html_file}")
        else:
            print(f"Warning: No </head> in {html_file}")

if __name__ == "__main__":
    standardize_css()
