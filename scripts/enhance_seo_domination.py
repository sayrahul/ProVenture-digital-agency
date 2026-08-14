import os
import glob
import re
import json

SERVICE_DEFINITIONS = {
    "digital-marketing.html": {
        "service_name": "Digital Marketing Services in Chhatrapati Sambhajinagar",
        "service_type": "Digital Marketing & Performance Growth",
        "description": "Full-service digital marketing agency in Chhatrapati Sambhajinagar (Aurangabad) specializing in SEO, Google Ads, Meta Ads, social media growth, and ROI-driven performance marketing.",
        "faqs": [
            {
                "q": "Which is the best digital marketing agency in Chhatrapati Sambhajinagar?",
                "a": "ProVenture Digital Agency is recognized as the leading digital marketing agency in Chhatrapati Sambhajinagar, offering full-funnel digital marketing, SEO, performance ads, web design, and creative content with proven ROI."
            },
            {
                "q": "What digital marketing services does ProVenture provide in Maharashtra?",
                "a": "ProVenture provides search engine optimization (SEO), Google Search & Display Ads, Meta (Facebook & Instagram) advertising, social media management, brand positioning, and web development across Maharashtra."
            },
            {
                "q": "How can digital marketing help grow my business in Sambhajinagar?",
                "a": "Digital marketing puts your business in front of high-intent local and regional customers via targeted search results and social media ads, dramatically increasing qualified inquiries and revenue."
            }
        ]
    },
    "web-development.html": {
        "service_name": "Web Development Services in Chhatrapati Sambhajinagar",
        "service_type": "Custom Web & Application Development",
        "description": "High-performance, modern, and mobile-responsive website development in Chhatrapati Sambhajinagar using cutting-edge technologies, fast load speeds, and conversion-focused UX.",
        "faqs": [
            {
                "q": "How long does it take to develop a business website with ProVenture?",
                "a": "Standard business websites are built within 7 to 14 business days, while custom web applications or ecommerce portals typically take 3 to 5 weeks."
            },
            {
                "q": "Are ProVenture websites mobile-friendly and SEO optimized?",
                "a": "Yes, 100% of websites created by ProVenture are responsive across all mobile and desktop devices and come pre-configured with technical SEO best practices."
            }
        ]
    },
    "web-design.html": {
        "service_name": "UI/UX & Web Design in Chhatrapati Sambhajinagar",
        "service_type": "Website & Interface Design",
        "description": "Award-winning UI/UX website design in Chhatrapati Sambhajinagar (Aurangabad) crafted to captivate visitors, elevate brand authority, and maximize conversions.",
        "faqs": [
            {
                "q": "Why is professional web design crucial for businesses in Sambhajinagar?",
                "a": "First impressions happen in milliseconds. A modern, premium website builds instant credibility and trust, converting more visitors into paying clients."
            }
        ]
    },
    "search-engine-optimization.html": {
        "service_name": "Search Engine Optimization (SEO) in Chhatrapati Sambhajinagar",
        "service_type": "SEO & Organic Search Growth",
        "description": "Rank #1 on Google with ProVenture's data-driven SEO services in Chhatrapati Sambhajinagar. Comprehensive On-Page, Off-Page, Technical, and Local Google Maps SEO.",
        "faqs": [
            {
                "q": "How long does it take to rank on Google Page 1 with SEO?",
                "a": "Most local and regional campaigns begin seeing significant keyword ranking and organic traffic improvements within 60 to 90 days."
            },
            {
                "q": "Do you offer Google Business Profile (Local Map Pack) optimization in Sambhajinagar?",
                "a": "Yes, ProVenture specializes in dominating the Google Local 3-Pack so nearby customers find your business first when searching for your services."
            }
        ]
    },
    "social-media.html": {
        "service_name": "Social Media Marketing in Chhatrapati Sambhajinagar",
        "service_type": "Social Media Management & Growth",
        "description": "Build an engaged community and generate high-converting leads on Instagram, Facebook, and LinkedIn with ProVenture's social media agency services.",
        "faqs": [
            {
                "q": "Which social platforms are most effective for businesses in Maharashtra?",
                "a": "Instagram and Facebook provide the highest engagement for B2C and retail brands, while LinkedIn is exceptionally strong for B2B and industrial services."
            }
        ]
    },
    "graphic-design.html": {
        "service_name": "Graphic Design & Branding in Chhatrapati Sambhajinagar",
        "service_type": "Creative Graphic Design & Brand Identity",
        "description": "Elevate your visual identity with custom logo design, marketing collateral, social creatives, packaging, and branding solutions in Chhatrapati Sambhajinagar.",
        "faqs": [
            {
                "q": "What is included in a complete branding package with ProVenture?",
                "a": "Our branding package includes logo design, brand color palette, typography guidelines, stationery design, social media kits, and brand voice guidelines."
            }
        ]
    },
    "video-production.html": {
        "service_name": "Video Production & Editing in Chhatrapati Sambhajinagar",
        "service_type": "Commercial Video Production & Post-Production",
        "description": "High-impact brand videos, commercial ads, cinematic reels, product shoots, and corporate documentary production in Chhatrapati Sambhajinagar.",
        "faqs": [
            {
                "q": "Do you provide full video production from concept to final edit?",
                "a": "Yes, ProVenture handles scripting, storyboarding, shooting, 4K filming, voiceover, sound design, and color grading for all video formats."
            }
        ]
    },
    "ai-services.html": {
        "service_name": "AI & Automation Services in Chhatrapati Sambhajinagar",
        "service_type": "AI Solutions & Workflow Automation",
        "description": "Modernize your operations and customer engagement with custom AI chatbots, automated CRM workflows, and intelligent business solutions.",
        "faqs": [
            {
                "q": "How can AI chatbots improve customer response times for our business?",
                "a": "AI chatbots respond instantly 24/7, qualify incoming leads automatically, and book consultations directly into your calendar without human delay."
            }
        ]
    }
}

ORGANIZATION_SCHEMA = {
    "@type": ["Organization", "ProfessionalService", "MarketingAgency"],
    "@id": "https://proventure.in/#organization",
    "name": "ProVenture Digital Agency",
    "alternateName": ["ProVenture", "ProVenture Marketing Agency", "ProVenture Aurangabad", "ProVenture Sambhajinagar"],
    "url": "https://proventure.in/",
    "logo": "https://proventure.in/thumbnails/proventure-white-logo.png",
    "image": "https://proventure.in/og-image.png",
    "telephone": "+919595997711",
    "email": "info@proventure.in",
    "priceRange": "$$",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Kanchanwadi",
        "addressLocality": "Chhatrapati Sambhajinagar",
        "addressRegion": "Maharashtra",
        "postalCode": "431001",
        "addressCountry": "IN"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 19.8762,
        "longitude": 75.3433
    },
    "hasMap": "https://maps.google.com/?q=Kanchanwadi,Chhatrapati+Sambhajinagar",
    "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        "opens": "09:30",
        "closes": "19:00"
    },
    "sameAs": [
        "https://www.linkedin.com/company/proventurein/",
        "https://www.facebook.com/ProVentureIN/",
        "https://www.instagram.com/proventureIN/",
        "https://wa.me/919595997711"
    ],
    "areaServed": [
        {
            "@type": "AdministrativeArea",
            "name": "Chhatrapati Sambhajinagar"
        },
        {
            "@type": "AdministrativeArea",
            "name": "Aurangabad"
        },
        {
            "@type": "AdministrativeArea",
            "name": "Maharashtra"
        },
        {
            "@type": "Country",
            "name": "India"
        }
    ],
    "knowsAbout": [
        "Digital Marketing",
        "Search Engine Optimization (SEO)",
        "Social Media Marketing",
        "Web Design and Development",
        "Graphic Design & Branding",
        "Video Production and Editing",
        "Performance Advertising",
        "AI Chatbots & Automation"
    ],
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.9",
        "reviewCount": "52",
        "bestRating": "5",
        "worstRating": "1"
    }
}

def generate_page_schema(filename):
    basename = os.path.basename(filename)
    graph = [ORGANIZATION_SCHEMA]
    
    if basename in SERVICE_DEFINITIONS:
        info = SERVICE_DEFINITIONS[basename]
        service_schema = {
            "@type": "Service",
            "name": info["service_name"],
            "serviceType": info["service_type"],
            "description": info["description"],
            "provider": {"@id": "https://proventure.in/#organization"},
            "areaServed": {
                "@type": "AdministrativeArea",
                "name": "Chhatrapati Sambhajinagar, Maharashtra, India"
            }
        }
        graph.append(service_schema)
        
        if "faqs" in info and info["faqs"]:
            faq_schema = {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item["q"],
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": item["a"]
                        }
                    }
                    for item in info["faqs"]
                ]
            }
            graph.append(faq_schema)
            
    elif basename == "index.html":
        # Add Homepage Core FAQ Schema
        faq_schema = {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "Why is ProVenture the top digital marketing agency in Chhatrapati Sambhajinagar?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "ProVenture blends 10+ years of creative expertise with cutting-edge data and performance marketing to deliver measurable ROI, ranking dominance, and elevated brand authority for businesses across Maharashtra."
                    }
                },
                {
                    "@type": "Question",
                    "name": "What services does ProVenture Digital Agency offer?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "We offer full-suite digital solutions including SEO, Google & Meta Ads, Social Media Marketing, Custom Web Development, UI/UX Design, Video Production, Graphic Branding, and AI Solutions."
                    }
                }
            ]
        }
        graph.append(faq_schema)

    return {
        "@context": "https://schema.org",
        "@graph": graph
    }

def update_file_seo(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    schema_data = generate_page_schema(filepath)
    schema_json = json.dumps(schema_data, indent=2, ensure_ascii=False)
    schema_block = f'<script type="application/ld+json">\n{schema_json}\n</script>'

    # Replace or inject schema
    if '<script type="application/ld+json">' in content:
        content = re.sub(
            r'<script type="application/ld\+json">[\s\S]*?</script>',
            schema_block,
            content,
            count=1
        )
    else:
        content = content.replace('<head>', f'<head>\n{schema_block}')

    # Ensure Geo Meta tags are present
    geo_tags = '''\t<meta content="IN-MH" name="geo.region" />
\t<meta content="Chhatrapati Sambhajinagar, Maharashtra, India" name="geo.placename" />
\t<meta content="19.8762;75.3433" name="geo.position" />
\t<meta content="19.8762, 75.3433" name="ICBM" />
\t<meta property="og:locale" content="en_IN" />
\t<meta property="og:site_name" content="ProVenture Digital Agency" />'''

    if 'name="geo.region"' in content:
        content = re.sub(
            r'<meta content="[^"]*" name="geo\.region" />[\s\S]*?<meta content="[^"]*" name="ICBM" />',
            geo_tags,
            content,
            count=1
        )
    else:
        content = content.replace('</head>', f'{geo_tags}\n</head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated SEO & Schema in: {filepath}")

def generate_complete_sitemap():
    files = sorted(glob.glob('*.html') + glob.glob('blog/*.html'))
    now_date = "2026-08-14"
    
    xml_entries = []
    for f in files:
        rel = f.replace('\\', '/')
        clean_name = rel.replace('.html', '')
        if clean_name == 'index':
            loc = "https://proventure.in/"
            priority = "1.00"
            changefreq = "weekly"
        elif clean_name in ['demo-preview', 'legal', 'privacy', 'terms']:
            loc = f"https://proventure.in/{clean_name}"
            priority = "0.30"
            changefreq = "yearly"
        elif 'blog' in clean_name:
            loc = f"https://proventure.in/{clean_name}"
            priority = "0.80"
            changefreq = "weekly"
        elif clean_name in ['services', 'digital-marketing', 'web-development', 'search-engine-optimization', 'social-media', 'pricing']:
            loc = f"https://proventure.in/{clean_name}"
            priority = "0.90"
            changefreq = "weekly"
        else:
            loc = f"https://proventure.in/{clean_name}"
            priority = "0.80"
            changefreq = "monthly"

        entry = f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{now_date}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        xml_entries.append(entry)

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(xml_entries)}
</urlset>
"""
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print("Regenerated complete sitemap.xml with all pages.")

def main():
    files = glob.glob('*.html') + glob.glob('blog/*.html')
    for f in files:
        update_file_seo(f)
    generate_complete_sitemap()
    print(f"Finished updating SEO and Schema across all {len(files)} pages.")

if __name__ == '__main__':
    main()
