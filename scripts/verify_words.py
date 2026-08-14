import os
import glob

files = sorted(glob.glob(os.path.join(os.path.dirname(__file__), '..', 'content', 'blogs', '*.md')))
print(f"Total blog markdown files: {len(files)}\n")

total_words = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
        words = len(text.split())
        total_words += words
        print(f"[{os.path.basename(f)}] -> {words} words")

print(f"\nGrand Total: {total_words} words across {len(files)} articles!")
print(f"Average: {total_words // len(files)} words per article.")
