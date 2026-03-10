def fix_contact():
    target_file = 'contact.html'
    
    with open(target_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Lines are 0-indexed in list, but my analysis used 1-indexed.
    # I want to remove 502 to 696 (inclusive).
    # 502 in 1-index is 501 in 0-index.
    # 696 in 1-index is 695 in 0-index.
    
    # Verification:
    # Line 502 (1-idx) should be <footer...
    # Line 696 (1-idx) should be </main>
    # Line 697 (1-idx) should be <footer...
    
    print(f"Line 502: {lines[501].strip()}")
    print(f"Line 696: {lines[695].strip()}")
    print(f"Line 697: {lines[696].strip()}")
    
    if '<footer' not in lines[501]:
        print("Error: Line 502 is not footer. Aborting.")
        return

    if '</main>' not in lines[695]:
        print("Error: Line 696 is not </main>. Aborting.")
        return

    if '<footer' not in lines[696]:
         print("Error: Line 697 is not footer. Aborting.")
         return
         
    # Remove lines 502 to 696
    # Slice: lines[:501] + lines[696:]
    # This keeps 1..501, skips 502..696, keeps 697..end
    
    new_lines = lines[:501] + lines[696:]
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
        
    print(f"Successfully removed {696-501} lines.")

if __name__ == "__main__":
    fix_contact()
