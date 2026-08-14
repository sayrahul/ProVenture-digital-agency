/**
 * ProVenture Automated Blog Publisher Engine
 * 
 * Features:
 * - Parses Markdown files with YAML-like frontmatter in /content/blogs/
 * - Filters posts where publishDate <= Current Date (or processes all if --all flag is passed)
 * - Renders standalone SEO-optimized HTML pages into /blog/[slug].html
 * - Injects full LocalBusiness + BlogPosting JSON-LD schemas
 * - Strict WCAG AA contrast compliance (no dark-on-dark or low-contrast text)
 * - Dynamically updates blog.html listing grid
 * - Dynamically updates sitemap.xml with proper lastmod and URLs
 * - Supports CLI flags: --all, --dry-run, --date=YYYY-MM-DD, --force
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.resolve(__dirname, '..');
const CONTENT_DIR = path.join(ROOT_DIR, 'content', 'blogs');
const BLOG_OUTPUT_DIR = path.join(ROOT_DIR, 'blog');
const BLOG_HTML_PATH = path.join(ROOT_DIR, 'blog.html');
const SITEMAP_PATH = path.join(ROOT_DIR, 'sitemap.xml');
const BASE_URL = 'https://proventure.in';

// CLI args
const args = process.argv.slice(2);
const isAll = args.includes('--all');
const isDryRun = args.includes('--dry-run');
const isForce = args.includes('--force');
const dateArg = args.find(a => a.startsWith('--date='));
const targetDateStr = dateArg ? dateArg.split('=')[1] : new Date().toISOString().split('T')[0];
const targetDate = new Date(targetDateStr);

console.log(`\n======================================================`);
console.log(`🚀 ProVenture Automated Blog Publisher`);
console.log(`📅 Target Evaluation Date: ${targetDateStr}`);
console.log(`⚙️  Mode: ${isAll ? 'ALL POSTS (--all)' : 'SCHEDULED DRIP'}`);
if (isDryRun) console.log(`🔍 DRY RUN MODE (No files will be modified)`);
console.log(`======================================================\n`);

// Ensure output dirs exist
if (!fs.existsSync(BLOG_OUTPUT_DIR)) {
  fs.mkdirSync(BLOG_OUTPUT_DIR, { recursive: true });
}

// Simple Frontmatter & Markdown Parser
function parseMarkdownFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const frontmatterRegex = /^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);

  if (!match) {
    throw new Error(`File ${filePath} is missing frontmatter headers (--- ... ---)`);
  }

  const rawYaml = match[1];
  const body = match[2];

  const metadata = {};
  rawYaml.split('\n').forEach(line => {
    const colonIdx = line.indexOf(':');
    if (colonIdx !== -1) {
      const key = line.slice(0, colonIdx).trim();
      let value = line.slice(colonIdx + 1).trim();
      if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }
      metadata[key] = value;
    }
  });

  return { metadata, body, filename: path.basename(filePath) };
}

// Format inline text (Bold, Italic, Links, Code)
function formatInline(str) {
  if (!str) return '';
  // Escape HTML entities first safely
  let text = str;
  // Bold
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Italic
  text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
  // Inline code
  text = text.replace(/`(.*?)`/g, '<code>$1</code>');
  // Markdown links [Anchor](URL)
  text = text.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');
  return text;
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// Convert markdown to clean semantic HTML
function markdownToHtml(md) {
  const lines = md.split(/\r?\n/);
  const htmlParts = [];
  let inList = false;
  let listType = null;
  let inTable = false;
  let tableRows = [];
  let inCode = false;
  let codeBuffer = [];
  let paragraphBuffer = [];

  function flushParagraph() {
    if (paragraphBuffer.length > 0) {
      const text = paragraphBuffer.join(' ').trim();
      if (text) {
        htmlParts.push(`<p>${formatInline(text)}</p>`);
      }
      paragraphBuffer = [];
    }
  }

  function flushList() {
    if (inList) {
      htmlParts.push(listType === 'ul' ? '</ul>' : '</ol>');
      inList = false;
      listType = null;
    }
  }

  function flushTable() {
    if (inTable && tableRows.length > 0) {
      let tableHtml = '<div class="overflow-x-auto my-8"><table>';
      tableRows.forEach((row, idx) => {
        if (row.includes('---')) return; // skip delimiter
        const cells = row.split('|').filter((_, i, arr) => i > 0 && i < arr.length - 1).map(c => c.trim());
        if (idx === 0) {
          tableHtml += '<thead><tr>';
          cells.forEach(c => tableHtml += `<th>${formatInline(c)}</th>`);
          tableHtml += '</tr></thead><tbody>';
        } else {
          tableHtml += '<tr>';
          cells.forEach(c => tableHtml += `<td>${formatInline(c)}</td>`);
          tableHtml += '</tr>';
        }
      });
      tableHtml += '</tbody></table></div>';
      htmlParts.push(tableHtml);
      inTable = false;
      tableRows = [];
    }
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // Code block toggle
    if (trimmed.startsWith('```')) {
      flushParagraph();
      flushList();
      flushTable();
      if (inCode) {
        htmlParts.push(`<pre><code>${escapeHtml(codeBuffer.join('\n'))}</code></pre>`);
        codeBuffer = [];
        inCode = false;
      } else {
        inCode = true;
      }
      continue;
    }

    if (inCode) {
      codeBuffer.push(line);
      continue;
    }

    // Empty line
    if (!trimmed) {
      flushParagraph();
      flushList();
      flushTable();
      continue;
    }

    // Horizontal Rule
    if (trimmed === '---' || trimmed === '***') {
      flushParagraph();
      flushList();
      flushTable();
      htmlParts.push('<hr/>');
      continue;
    }

    // Headings
    if (trimmed.startsWith('# ')) {
      flushParagraph();
      flushList();
      flushTable();
      htmlParts.push(`<h1>${formatInline(trimmed.slice(2))}</h1>`);
      continue;
    }
    if (trimmed.startsWith('## ')) {
      flushParagraph();
      flushList();
      flushTable();
      htmlParts.push(`<h2>${formatInline(trimmed.slice(3))}</h2>`);
      continue;
    }
    if (trimmed.startsWith('### ')) {
      flushParagraph();
      flushList();
      flushTable();
      htmlParts.push(`<h3>${formatInline(trimmed.slice(4))}</h3>`);
      continue;
    }

    // Blockquote
    if (trimmed.startsWith('> ')) {
      flushParagraph();
      flushList();
      flushTable();
      htmlParts.push(`<blockquote>${formatInline(trimmed.slice(2))}</blockquote>`);
      continue;
    }

    // Table rows
    if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
      flushParagraph();
      flushList();
      inTable = true;
      tableRows.push(trimmed);
      continue;
    } else if (inTable) {
      flushTable();
    }

    // Unordered List (- or *)
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      flushParagraph();
      flushTable();
      if (!inList || listType !== 'ul') {
        flushList();
        htmlParts.push('<ul>');
        inList = true;
        listType = 'ul';
      }
      htmlParts.push(`<li>${formatInline(trimmed.slice(2))}</li>`);
      continue;
    }

    // Ordered List (1., 2., etc.)
    const orderedMatch = trimmed.match(/^(\d+)\.\s+(.*)$/);
    if (orderedMatch) {
      flushParagraph();
      flushTable();
      if (!inList || listType !== 'ol') {
        flushList();
        htmlParts.push('<ol>');
        inList = true;
        listType = 'ol';
      }
      htmlParts.push(`<li>${formatInline(orderedMatch[2])}</li>`);
      continue;
    }

    // Regular paragraph line
    flushList();
    flushTable();
    paragraphBuffer.push(trimmed);
  }

  flushParagraph();
  flushList();
  flushTable();

  return htmlParts.join('\n');
}

// Generate Blog Post HTML Document
function generatePostHtml(post, allPublished) {
  const meta = post.metadata;
  const canonicalUrl = `${BASE_URL}/blog/${meta.slug}`;
  const publishIso = new Date(meta.publishDate).toISOString();
  const bodyHtml = markdownToHtml(post.body);
  
  // Calculate read time
  const wordCount = post.body.split(/\s+/).length;
  const readTime = Math.max(3, Math.ceil(wordCount / 220));

  // Related posts (pick other published ones)
  const relatedPosts = allPublished
    .filter(p => p.metadata.slug !== meta.slug)
    .slice(0, 3);

  const relatedHtml = relatedPosts.map(p => `
    <a href="/blog/${p.metadata.slug}" class="block group p-5 bg-white rounded-xl border border-gray-200 hover:border-[#00ACDF] hover:shadow-lg transition-all duration-300">
      <span class="text-xs uppercase tracking-wider font-bold text-[#0077a3]">${p.metadata.category || 'Article'}</span>
      <h4 class="font-bold text-gray-900 group-hover:text-[#0077a3] transition mt-2 mb-2 line-clamp-2">${p.metadata.title}</h4>
      <p class="text-xs text-gray-500">${p.metadata.publishDate} • ${Math.ceil(p.body.split(/\s+/).length / 220)} min read</p>
    </a>
  `).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport"/>
  <title>${escapeHtml(meta.title)} | ProVenture</title>
  <meta name="description" content="${escapeHtml(meta.metaDescription || meta.excerpt)}"/>
  <meta name="keywords" content="${escapeHtml(meta.keywords || '')}"/>
  <link rel="canonical" href="${canonicalUrl}"/>

  <!-- Open Graph / Social -->
  <meta property="og:type" content="article"/>
  <meta property="og:title" content="${escapeHtml(meta.title)}"/>
  <meta property="og:description" content="${escapeHtml(meta.metaDescription || meta.excerpt)}"/>
  <meta property="og:url" content="${canonicalUrl}"/>
  <meta property="og:image" content="${meta.ogImage || `${BASE_URL}/og-image.png`}"/>
  <meta property="og:site_name" content="ProVenture Digital Agency"/>
  <meta property="article:published_time" content="${publishIso}"/>
  <meta property="article:author" content="ProVenture Editorial Team"/>

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="${escapeHtml(meta.title)}"/>
  <meta name="twitter:description" content="${escapeHtml(meta.metaDescription || meta.excerpt)}"/>
  <meta name="twitter:image" content="${meta.ogImage || `${BASE_URL}/og-image.png`}"/>

  <!-- Favicon -->
  <link rel="icon" type="image/x-icon" href="/favicon.ico"/>
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"/>

  <!-- CSS & Fonts -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet"/>
  <link href="/custom/css/default-20252e34.css" rel="stylesheet" type="text/css"/>
  <link href="/custom/css/proventure-custom.css" rel="stylesheet" type="text/css"/>

  <!-- Explicit Contrast & Typography Control Stylesheet -->
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc !important; color: #0f172a !important; }
    h1, h2, h3, h4, .font-heading { font-family: 'Space Grotesk', sans-serif; }
    
    /* Strict high-contrast text rules inside article */
    .article-content { color: #1e293b !important; }
    .article-content h1 { color: #0f172a !important; font-size: 2.25rem !important; font-weight: 800 !important; margin-top: 1.5rem !important; margin-bottom: 1.25rem !important; line-height: 1.25 !important; }
    .article-content h2 { color: #0f172a !important; font-size: 1.75rem !important; font-weight: 700 !important; margin-top: 2.5rem !important; margin-bottom: 1.25rem !important; border-bottom: 2px solid #e2e8f0 !important; padding-bottom: 0.5rem !important; line-height: 1.3 !important; }
    .article-content h3 { color: #0f172a !important; font-size: 1.35rem !important; font-weight: 700 !important; margin-top: 2rem !important; margin-bottom: 0.75rem !important; line-height: 1.4 !important; }
    .article-content p { color: #334155 !important; font-size: 1.05rem !important; line-height: 1.8 !important; margin-bottom: 1.25rem !important; }
    .article-content ul, .article-content ol { color: #334155 !important; margin: 1rem 0 1.5rem 1.5rem !important; list-style-position: outside !important; }
    .article-content ul { list-style-type: disc !important; }
    .article-content ol { list-style-type: decimal !important; }
    .article-content li { color: #334155 !important; margin-bottom: 0.6rem !important; line-height: 1.7 !important; font-size: 1.02rem !important; }
    .article-content strong { color: #0f172a !important; font-weight: 700 !important; }
    .article-content em { color: #334155 !important; font-style: italic !important; }
    .article-content hr { border: 0 !important; border-top: 1px solid #e2e8f0 !important; margin: 2.5rem 0 !important; }
    
    /* High contrast accessible links */
    .article-content a { color: #0077a3 !important; font-weight: 600 !important; text-decoration: underline !important; text-underline-offset: 3px !important; }
    .article-content a:hover { color: #005577 !important; }

    /* Tables */
    .article-content table { width: 100% !important; border-collapse: collapse !important; margin: 2rem 0 !important; background: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; overflow: hidden !important; }
    .article-content th { background-color: #f1f5f9 !important; color: #0f172a !important; font-weight: 700 !important; padding: 14px 16px !important; text-align: left !important; border: 1px solid #cbd5e1 !important; }
    .article-content td { padding: 12px 16px !important; color: #334155 !important; border: 1px solid #cbd5e1 !important; font-size: 0.95rem !important; line-height: 1.6 !important; }
    .article-content tr:nth-child(even) td { background-color: #f8fafc !important; }

    /* Blockquotes */
    .article-content blockquote { border-left: 4px solid #00ACDF !important; background-color: #f0f9ff !important; color: #0369a1 !important; padding: 1rem 1.25rem !important; margin: 1.5rem 0 !important; border-radius: 0 8px 8px 0 !important; font-style: italic !important; }

    /* Code blocks */
    .article-content pre { background-color: #0f172a !important; color: #f8fafc !important; padding: 1.25rem !important; border-radius: 8px !important; overflow-x: auto !important; font-family: monospace !important; font-size: 0.875rem !important; margin: 1.5rem 0 !important; border: 1px solid #1e293b !important; }
    .article-content pre code { color: #f8fafc !important; background: transparent !important; }
    .article-content code { background-color: #f1f5f9 !important; color: #b91c1c !important; padding: 2px 6px !important; border-radius: 4px !important; font-size: 0.875rem !important; font-family: monospace !important; }

    /* Dark CTA Box Protection - Explicit High-Contrast White Text */
    .pv-dark-cta { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important; color: #ffffff !important; }
    .pv-dark-cta h3 { color: #ffffff !important; }
    .pv-dark-cta p { color: #e2e8f0 !important; }
    .pv-dark-cta .pv-tag { color: #38bdf8 !important; }
    .pv-dark-cta .pv-btn-primary { background-color: #00ACDF !important; color: #051c24 !important; font-weight: 800 !important; }
    .pv-dark-cta .pv-btn-primary:hover { background-color: #38c8f5 !important; }
    .pv-dark-cta .pv-btn-secondary { background-color: rgba(255,255,255,0.12) !important; color: #ffffff !important; border: 1px solid rgba(255,255,255,0.3) !important; }
    .pv-dark-cta .pv-btn-secondary:hover { background-color: rgba(255,255,255,0.22) !important; color: #ffffff !important; }

    /* Header Nav Protection */
    .pv-header-nav a { color: #334155 !important; }
    .pv-header-nav a:hover, .pv-header-nav a.active { color: #0077a3 !important; }

    /* Footer High-Contrast Protection */
    footer { background-color: #0f172a !important; color: #94a3b8 !important; }
    footer h4, footer .font-bold { color: #ffffff !important; }
    footer a { color: #cbd5e1 !important; text-decoration: none !important; }
    footer a:hover { color: #38bdf8 !important; }
  </style>

  <!-- Structured Data JSON-LD (LocalBusiness + BlogPosting + BreadcrumbList) -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "LocalBusiness",
        "@id": "${BASE_URL}/#localbusiness",
        "name": "ProVenture",
        "url": "${BASE_URL}/",
        "logo": "${BASE_URL}/og-image.png",
        "image": "${BASE_URL}/og-image.png",
        "description": "Leading Digital Marketing, Web Development, and Graphic Design Agency in Chhatrapati Sambhajinagar (Aurangabad).",
        "telephone": "+91-XXXXXXXXXX",
        "priceRange": "₹₹",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "Cidco / Jalna Road",
          "addressLocality": "Chhatrapati Sambhajinagar (Aurangabad)",
          "addressRegion": "Maharashtra",
          "postalCode": "431001",
          "addressCountry": "IN"
        },
        "geo": {
          "@type": "GeoCoordinates",
          "latitude": 19.8762,
          "longitude": 75.3433
        },
        "areaServed": [
          "Chhatrapati Sambhajinagar",
          "Aurangabad",
          "Maharashtra",
          "India"
        ]
      },
      {
        "@type": "BreadcrumbList",
        "@id": "${canonicalUrl}/#breadcrumb",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "${BASE_URL}/"
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": "Blog",
            "item": "${BASE_URL}/blog"
          },
          {
            "@type": "ListItem",
            "position": 3,
            "name": "${escapeHtml(meta.title)}",
            "item": "${canonicalUrl}"
          }
        ]
      },
      {
        "@type": "BlogPosting",
        "@id": "${canonicalUrl}/#article",
        "isPartOf": {
          "@type": "WebPage",
          "@id": "${canonicalUrl}"
        },
        "headline": "${escapeHtml(meta.title)}",
        "description": "${escapeHtml(meta.metaDescription || meta.excerpt)}",
        "url": "${canonicalUrl}",
        "datePublished": "${publishIso}",
        "dateModified": "${publishIso}",
        "publisher": {
          "@id": "${BASE_URL}/#localbusiness"
        },
        "author": {
          "@type": "Organization",
          "name": "ProVenture Editorial Team"
        },
        "inLanguage": "en-US",
        "mainEntityOfPage": "${canonicalUrl}"
      }
    ]
  }
  </script>
</head>
<body class="bg-slate-50 text-slate-900 antialiased flex flex-col min-h-screen">

  <!-- Header / Navigation Bar -->
  <header class="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
      <a href="/" class="flex items-center gap-2">
        <span class="text-2xl font-black text-gray-900 tracking-tight font-heading">Pro<span class="text-[#00ACDF]">Venture</span></span>
      </a>

      <nav class="pv-header-nav hidden md:flex items-center gap-8 text-sm font-semibold">
        <a href="/" class="hover:text-[#0077a3] transition">Home</a>
        <a href="/services" class="hover:text-[#0077a3] transition">Services</a>
        <a href="/pricing" class="hover:text-[#0077a3] transition">Pricing</a>
        <a href="/blog" class="active font-bold">Blog</a>
        <a href="/about" class="hover:text-[#0077a3] transition">About</a>
        <a href="/contact" class="hover:text-[#0077a3] transition">Contact</a>
      </nav>

      <div class="flex items-center gap-4">
        <a href="https://wa.me/91XXXXXXXXXX?text=Hi%20ProVenture,%20I%20would%20like%20a%20free%20digital%20audit" target="_blank" rel="noopener" class="hidden sm:inline-flex items-center gap-2 bg-[#00ACDF] hover:bg-[#0092bd] text-[#051c24] px-5 py-2.5 rounded-full text-sm font-bold shadow-md transition-all">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/></svg>
          Free Audit
        </a>
      </div>
    </div>
  </header>

  <!-- Breadcrumbs -->
  <div class="bg-gray-100 border-b border-gray-200 py-3 text-xs text-gray-600">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 flex items-center gap-2">
      <a href="/" class="hover:text-gray-900 font-medium">Home</a>
      <span>/</span>
      <a href="/blog" class="hover:text-gray-900 font-medium">Blog</a>
      <span>/</span>
      <span class="text-gray-800 font-semibold truncate">${escapeHtml(meta.title)}</span>
    </div>
  </div>

  <!-- Main Article Content -->
  <main class="flex-grow py-12 px-4 sm:px-6 lg:px-8">
    <article class="max-w-4xl mx-auto bg-white p-6 sm:p-10 md:p-14 rounded-2xl shadow-sm border border-gray-200">
      
      <!-- Article Header -->
      <header class="mb-10 pb-8 border-b border-gray-200">
        <div class="flex flex-wrap items-center gap-3 mb-4">
          <span class="bg-sky-100 text-[#006282] font-bold text-xs px-3 py-1 rounded-full uppercase tracking-wider border border-sky-200">
            ${escapeHtml(meta.category || 'Local SEO & Growth')}
          </span>
          <span class="text-gray-400 text-xs">•</span>
          <time datetime="${meta.publishDate}" class="text-gray-600 text-xs font-semibold">Published on ${meta.publishDate}</time>
          <span class="text-gray-400 text-xs">•</span>
          <span class="text-gray-600 text-xs font-semibold">${readTime} min read</span>
        </div>

        <h1 class="text-3xl sm:text-4xl md:text-5xl font-extrabold text-gray-900 leading-tight mb-6 font-heading">
          ${escapeHtml(meta.title)}
        </h1>

        <p class="text-lg md:text-xl text-gray-700 leading-relaxed font-normal">
          ${escapeHtml(meta.excerpt || meta.metaDescription)}
        </p>

        <!-- Author Tag -->
        <div class="flex items-center gap-3 mt-6 pt-6 border-t border-gray-200">
          <div class="w-10 h-10 rounded-full bg-[#0077a3] text-white font-bold flex items-center justify-center text-sm shadow">
            PV
          </div>
          <div>
            <div class="font-bold text-gray-900 text-sm">ProVenture Editorial Team</div>
            <div class="text-xs text-gray-600">Chhatrapati Sambhajinagar (Aurangabad), MH</div>
          </div>
        </div>
      </header>

      <!-- Post Body with Strict High-Contrast Typography -->
      <div class="article-content leading-relaxed">
        ${bodyHtml}
      </div>

      <!-- High-Conversion Local CTA Box with High Contrast White Text -->
      <div class="pv-dark-cta mt-14 p-8 sm:p-10 rounded-2xl shadow-xl relative overflow-hidden">
        <div class="relative z-10 max-w-xl">
          <span class="pv-tag font-bold text-xs uppercase tracking-widest block mb-2">Grow With ProVenture</span>
          <h3 class="text-2xl sm:text-3xl font-bold font-heading mb-3">Want More Customers in Chhatrapati Sambhajinagar?</h3>
          <p class="text-sm sm:text-base mb-6 leading-relaxed">
            Get a free 30-minute digital marketing & SEO audit for your business. We will analyze your Google Business Profile, search rankings, and competitors to give you a clear roadmap.
          </p>
          <div class="flex flex-wrap items-center gap-4">
            <a href="https://wa.me/91XXXXXXXXXX?text=Hi%20ProVenture,%20I%20read%20your%20blog%20and%20would%20like%20a%20free%20audit" target="_blank" rel="noopener" class="pv-btn-primary inline-flex items-center gap-2 px-6 py-3 rounded-full text-sm font-bold shadow-lg transition-all">
              Chat on WhatsApp
            </a>
            <a href="/pricing" class="pv-btn-secondary inline-flex items-center gap-2 px-6 py-3 rounded-full text-sm font-bold transition-all">
              View Pricing Plans
            </a>
          </div>
        </div>
      </div>

      <!-- Related Local Articles -->
      ${relatedPosts.length > 0 ? `
      <section class="mt-16 pt-10 border-t border-gray-200">
        <h3 class="text-xl font-bold text-gray-900 font-heading mb-6">Related Guides for Sambhajinagar Businesses</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          ${relatedHtml}
        </div>
      </section>
      ` : ''}

    </article>
  </main>

  <!-- Footer -->
  <footer class="py-12 text-sm border-t border-gray-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
      <div>
        <div class="text-xl font-bold text-white mb-3">Pro<span class="text-[#00ACDF]">Venture</span></div>
        <p class="text-xs text-gray-300 leading-relaxed mb-4">
          Premier Digital Marketing, SEO, and Web Development Agency serving businesses across Chhatrapati Sambhajinagar (Aurangabad) and Maharashtra.
        </p>
      </div>
      <div>
        <div class="font-bold text-white mb-3 text-sm">Services</div>
        <ul class="space-y-2 text-xs">
          <li><a href="/digital-marketing" class="hover:text-[#38bdf8]">Digital Marketing</a></li>
          <li><a href="/web-design" class="hover:text-[#38bdf8]">Web Design</a></li>
          <li><a href="/search-engine-optimization" class="hover:text-[#38bdf8]">SEO Optimization</a></li>
          <li><a href="/graphic-design" class="hover:text-[#38bdf8]">Graphic Design</a></li>
        </ul>
      </div>
      <div>
        <div class="font-bold text-white mb-3 text-sm">Quick Links</div>
        <ul class="space-y-2 text-xs">
          <li><a href="/pricing" class="hover:text-[#38bdf8]">Pricing Guide</a></li>
          <li><a href="/blog" class="hover:text-[#38bdf8]">Blog & Guides</a></li>
          <li><a href="/about" class="hover:text-[#38bdf8]">About Us</a></li>
          <li><a href="/contact" class="hover:text-[#38bdf8]">Contact Us</a></li>
        </ul>
      </div>
      <div>
        <div class="font-bold text-white mb-3 text-sm">Local Office</div>
        <p class="text-xs text-gray-300 leading-relaxed">
          Cidco / Jalna Road, Chhatrapati Sambhajinagar (Aurangabad), Maharashtra 431001
        </p>
      </div>
    </div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 border-t border-gray-800 text-center text-xs text-gray-400">
      &copy; 2026 ProVenture. All rights reserved. | <a href="/privacy" class="hover:underline text-gray-300">Privacy Policy</a> | <a href="/terms" class="hover:underline text-gray-300">Terms of Service</a>
    </div>
  </footer>

</body>
</html>`;
}

// Update sitemap.xml with published blog posts
function updateSitemap(publishedPosts) {
  if (!fs.existsSync(SITEMAP_PATH)) {
    console.warn(`⚠️ sitemap.xml not found at ${SITEMAP_PATH}, skipping sitemap update.`);
    return;
  }

  let sitemap = fs.readFileSync(SITEMAP_PATH, 'utf-8');
  let addedCount = 0;

  publishedPosts.forEach(p => {
    const postUrl = `${BASE_URL}/blog/${p.metadata.slug}`;
    if (!sitemap.includes(postUrl)) {
      const urlBlock = `  <url>\n    <loc>${postUrl}</loc>\n    <lastmod>${p.metadata.publishDate}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n`;
      sitemap = sitemap.replace('</urlset>', `${urlBlock}</urlset>`);
      addedCount++;
    }
  });

  if (addedCount > 0 && !isDryRun) {
    fs.writeFileSync(SITEMAP_PATH, sitemap, 'utf-8');
    console.log(`🗺️  Updated sitemap.xml with ${addedCount} new URLs.`);
  }
}

// Update blog.html cards listing
function updateBlogListHtml(publishedPosts) {
  if (!fs.existsSync(BLOG_HTML_PATH)) {
    return;
  }

  let blogHtml = fs.readFileSync(BLOG_HTML_PATH, 'utf-8');
  const startTag = '<!-- AUTO_PUBLISHED_CARDS_START -->';
  const endTag = '<!-- AUTO_PUBLISHED_CARDS_END -->';

  if (!blogHtml.includes(startTag) || !blogHtml.includes(endTag)) {
    return;
  }

  const cardsHtml = publishedPosts.map(p => `
<!-- Auto Post: ${escapeHtml(p.metadata.title)} -->
<article class="blog-card" style="cursor: pointer;" onclick="window.location.href='/blog/${p.metadata.slug}';">
  <div class="blog-thumb">
    <img alt="${escapeHtml(p.metadata.category || 'Digital Marketing')}" src="/thumbnails/120297-800-500-Crop.jpg"/>
    <span class="blog-tag-overlay">${escapeHtml(p.metadata.category || 'SEO')}</span>
  </div>
  <div class="blog-content">
    <span class="blog-date">${p.metadata.publishDate}</span>
    <h2 class="blog-title">${escapeHtml(p.metadata.title)}</h2>
    <p class="blog-excerpt">${escapeHtml(p.metadata.excerpt)}</p>
    <a class="read-more" href="/blog/${p.metadata.slug}">Read Article <span>&rarr;</span></a>
  </div>
</article>
`).join('\n');

  const newBlogHtml = blogHtml.replace(
    new RegExp(`${startTag}[\\s\\S]*?${endTag}`),
    `${startTag}\n${cardsHtml}\n${endTag}`
  );

  if (!isDryRun) {
    fs.writeFileSync(BLOG_HTML_PATH, newBlogHtml, 'utf-8');
    console.log(`📰 Updated blog.html with ${publishedPosts.length} published post cards.`);
  }
}

// Main execution routine
function run() {
  if (!fs.existsSync(CONTENT_DIR)) {
    console.error(`❌ Content directory not found: ${CONTENT_DIR}`);
    process.exit(1);
  }

  const files = fs.readdirSync(CONTENT_DIR).filter(f => f.endsWith('.md')).sort();
  console.log(`📂 Found ${files.length} markdown content files in /content/blogs/\n`);

  const allPosts = files.map(f => parseMarkdownFile(path.join(CONTENT_DIR, f)));

  // Filter posts based on schedule date
  const eligiblePosts = allPosts.filter(p => {
    if (isAll || isForce) return true;
    if (!p.metadata.publishDate) return false;
    const pDate = new Date(p.metadata.publishDate);
    return pDate <= targetDate;
  });

  console.log(`📊 Evaluation Results:`);
  console.log(`   - Total Queue: ${allPosts.length} posts`);
  console.log(`   - Scheduled / Ready to Publish: ${eligiblePosts.length} posts`);
  console.log(`   - Future Scheduled: ${allPosts.length - eligiblePosts.length} posts\n`);

  if (eligiblePosts.length === 0) {
    console.log(`✨ No new posts scheduled for release on or before ${targetDateStr}.`);
    return;
  }

  console.log(`📝 Processing eligible posts:`);
  eligiblePosts.forEach((post, i) => {
    const slug = post.metadata.slug || path.basename(post.filename, '.md');
    const outFile = path.join(BLOG_OUTPUT_DIR, `${slug}.html`);
    console.log(`   [${i + 1}/${eligiblePosts.length}] ${post.metadata.publishDate} | ${post.metadata.title}`);

    if (!isDryRun) {
      const htmlContent = generatePostHtml(post, eligiblePosts);
      fs.writeFileSync(outFile, htmlContent, 'utf-8');
    }
  });

  if (!isDryRun) {
    updateSitemap(eligiblePosts);
    updateBlogListHtml(eligiblePosts);
    console.log(`\n🎉 Successfully published ${eligiblePosts.length} blog pages to /blog/!`);
  } else {
    console.log(`\n🔍 Dry run completed. 0 files modified.`);
  }
}

run();
