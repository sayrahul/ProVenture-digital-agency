import re

with open('blog.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS additions
css_additions = """
        /* New Minimalistic Blog Design */
        .blog-card {
            border-radius: 12px;
            overflow: hidden;
            background: #fff;
            border: 1px solid #eaeaea;
            box-shadow: none !important;
            transition: none !important;
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .blog-card:hover {
            box-shadow: none !important;
            transform: none !important;
        }
        .blog-thumb {
            position: relative;
            width: 100%;
            height: 180px;
        }
        .blog-thumb img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .blog-tag-overlay {
            position: absolute;
            top: 15px;
            left: 15px;
            background-color: #00ACDF;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
            letter-spacing: 0.5px;
        }
        .blog-content {
            padding: 25px 20px;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        .blog-date {
            font-size: 11px;
            text-transform: uppercase;
            color: #999;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }
        .blog-title {
            font-size: 18px;
            font-weight: 700;
            line-height: 1.4;
            color: #111;
            margin-bottom: 15px;
            margin-top: 0;
        }
        .blog-excerpt {
            font-size: 14px;
            color: #666;
            line-height: 1.6;
            margin-bottom: 25px;
        }
        .read-more {
            color: #00ACDF;
            font-weight: 700;
            font-size: 14px;
            text-decoration: none;
            margin-top: auto;
            display: inline-block;
        }
        .read-more:hover {
            color: #0088b3;
        }
        .read-more span {
            margin-left: 4px;
        }
        /* Hide old meta styles if any */
        .blog-meta { display: none; }
"""

# Inject CSS before </style>
html = html.replace('</style>', css_additions + '\n    </style>')


def convert_card(match):
    # Regex extracts:
    # 1: id for openBlogModal
    # 2: img src
    # 3: tag (e.g. SEO)
    # 4: date
    # 5: title
    # 6: excerpt
    card_html = match.group(0)
    
    id_match = re.search(r"openBlogModal\('([^']+)'\)", card_html)
    img_match = re.search(r'src="([^"]+)"', card_html)
    tag_match = re.search(r'<span class="blog-tag">([^<]+)</span>', card_html)
    date_match = re.search(r'<span>([A-Z][a-z]{2} \d{2}, \d{4})</span>', card_html)
    title_match = re.search(r'<h2 class="blog-title"><a[^>]*>([^<]+)</a></h2>', card_html)
    excerpt_match = re.search(r'<p class="blog-excerpt">([^<]+)</p>', card_html)
    
    if not (id_match and img_match and tag_match and date_match and title_match and excerpt_match):
        return card_html # fallback
        
    modal_id = id_match.group(1)
    img_src = img_match.group(1)
    tag = tag_match.group(1)
    date_text = date_match.group(1)
    # Format date to uppercase short month (e.g. DEC 03, 2025)
    # The existing date is "Dec 03, 2025"
    date_text = date_text.upper()
    title = title_match.group(1)
    excerpt = excerpt_match.group(1)
    
    new_card = f'''<article class="blog-card" style="cursor: pointer;" onclick="openBlogModal('{modal_id}')">
<div class="blog-thumb">
<img alt="{tag}" src="{img_src}"/>
<span class="blog-tag-overlay">{tag}</span>
</div>
<div class="blog-content">
<span class="blog-date">{date_text}</span>
<h2 class="blog-title">{title}</h2>
<p class="blog-excerpt">{excerpt}</p>
<a class="read-more" href="javascript:void(0);">Read Article <span>&rarr;</span></a>
</div>
</article>'''
    return new_card

# We can replace all article tags
html = re.sub(r'<article class="blog-card" style="cursor: pointer;" onclick="openBlogModal.*?</article>', convert_card, html, flags=re.DOTALL)

with open('blog.html', 'w', encoding='utf-8') as f:
    f.write(html)
