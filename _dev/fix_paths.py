
import os
import re

def fix_paths(root_dir):
    print(f"Fixing paths in {root_dir}...")
    
    # Only target HTML files in the immediate root directory
    files = [f for f in os.listdir(root_dir) if f.endswith('.html') and os.path.isfile(os.path.join(root_dir, f))]
    
    for filename in files:
        filepath = os.path.join(root_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace user usage of ../../ in root files
            # Matches src="../../ or href="../../
            # We want to replace it with src=" or href=" (effectively removing ../../)
            
            new_content = re.sub(r'(src|href)=["\']\.\./\.\./([^"\']+)["\']', r'\1="\2"', content)
            
            # Also catch single ../ in root files which is invalid
            new_content = re.sub(r'(src|href)=["\']\.\./([^"\']+)["\']', r'\1="\2"', new_content)
            
            # Also check for ../ (one level) which might be wrong too if it takes us out of root
            # But let's stick to the observed double dot bug first.
            
            if content != new_content:
                print(f"Fixed paths in {filename}")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    fix_paths(os.getcwd())
