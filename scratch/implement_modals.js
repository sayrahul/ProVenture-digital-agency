const fs = require('fs');

let html = fs.readFileSync('d:/My Web Sites/ProVenture-digital-agency/blog.html', 'utf8');

// 1. Update blog-grid CSS
html = html.replace('grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));', 'grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));');

// 2. Add Modal CSS to <style>
const modalCss = `
        /* Blog Modal Styles */
        .pv-modal-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            z-index: 9999;
            display: flex;
            justify-content: flex-end;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .pv-modal-container.active {
            pointer-events: auto;
            opacity: 1;
        }
        .pv-modal-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(4px);
        }
        .pv-modal-panel {
            position: relative;
            width: 100%;
            max-width: 800px;
            height: 100vh;
            background: #fff;
            z-index: 1;
            transform: translateX(100%);
            transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        .pv-modal-container.active .pv-modal-panel {
            transform: translateX(0);
        }
        .pv-modal-header {
            padding: 20px 40px;
            border-bottom: 1px solid #eaeaea;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            background: #fff;
            z-index: 10;
        }
        .pv-modal-close {
            background: none;
            border: none;
            font-size: 28px;
            cursor: pointer;
            color: #333;
            transition: color 0.2s;
            line-height: 1;
            padding: 0;
        }
        .pv-modal-close:hover {
            color: #00ACDF;
        }
        .pv-modal-body {
            padding: 40px;
        }
        .pv-modal-body h2 {
            font-size: 32px;
            margin-bottom: 20px;
            color: #111;
        }
        .pv-modal-body img {
            width: 100%;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .pv-modal-body p {
            font-size: 16px;
            line-height: 1.8;
            color: #555;
            margin-bottom: 20px;
        }
    </style>`;
html = html.replace('</style>', modalCss);

// 3. Add onclick and cursor to existing blog cards
html = html.replace(/<article class="blog-card">/g, '<article class="blog-card" style="cursor: pointer;">');
html = html.replace(/<a class="read-more" href="#">/g, '<a class="read-more" href="javascript:void(0);">');

let card1Idx = html.indexOf('<!-- Blog Post 1 -->');
let card2Idx = html.indexOf('<!-- Blog Post 2 -->');
let card3Idx = html.indexOf('<!-- Blog Post 3 -->');
let endCardsIdx = html.indexOf('</div>', card3Idx);

html = html.substring(0, card1Idx) + 
       html.substring(card1Idx, card2Idx).replace('<article class="blog-card" style="cursor: pointer;">', '<article class="blog-card" style="cursor: pointer;" onclick="openBlogModal(\'blog-modal-1\')">') +
       html.substring(card2Idx, card3Idx).replace('<article class="blog-card" style="cursor: pointer;">', '<article class="blog-card" style="cursor: pointer;" onclick="openBlogModal(\'blog-modal-2\')">') +
       html.substring(card3Idx, endCardsIdx).replace('<article class="blog-card" style="cursor: pointer;">', '<article class="blog-card" style="cursor: pointer;" onclick="openBlogModal(\'blog-modal-3\')">') +
       html.substring(endCardsIdx);

// 4. Insert Blog Post 4
const post4 = `
<!-- Blog Post 4 -->
<article class="blog-card" style="cursor: pointer;" onclick="openBlogModal('blog-modal-4')">
<div class="blog-thumb">
<img alt="Data Analytics" src="thumbnails/99711-533-600-Crop.jpg"/>
</div>
<div class="blog-content">
<div class="blog-meta">
<span class="blog-tag">Analytics</span>
<span>Oct 12, 2025</span>
</div>
<h2 class="blog-title"><a href="javascript:void(0);" style="color: inherit; text-decoration: none;">Data-Driven Decisions in Modern Marketing</a></h2>
<p class="blog-excerpt">Stop guessing. Learn how to leverage analytics to maximize your ROI and understand your customers better.</p>
<a class="read-more" href="javascript:void(0);">Read Article <span>&rarr;</span></a>
</div>
</article>
`;
html = html.replace('<!-- Pagination -->', post4 + '\n<!-- Pagination -->');

// 5. Generate Modals HTML
const modalsHtml = `
<!-- Blog Modals -->
<div id="blog-modal-1" class="pv-modal-container">
    <div class="pv-modal-overlay" onclick="closeBlogModal('blog-modal-1')"></div>
    <div class="pv-modal-panel">
        <div class="pv-modal-header">
            <span style="font-weight: bold; color: #00ACDF;">SEO</span>
            <button class="pv-modal-close" onclick="closeBlogModal('blog-modal-1')">&times;</button>
        </div>
        <div class="pv-modal-body">
            <img alt="SEO Strategy" src="thumbnails/120297-800-500-Crop.jpg"/>
            <h2>5 SEO Strategies That Actually Work in 2025</h2>
            <p>Search engines are evolving at an unprecedented pace. With AI overviews and zero-click searches dominating the SERPs, traditional keyword stuffing is dead. Discover the key tactics you need to rank higher and drive organic traffic this year.</p>
            <p>First and foremost, focus on user intent. Google's algorithm has shifted towards semantic understanding. It's no longer just about matching keywords; it's about answering the user's underlying question comprehensively and authoritatively.</p>
            <p>Secondly, technical SEO cannot be ignored. Core Web Vitals, mobile-friendliness, and site speed are foundational. A beautiful website that takes 5 seconds to load will lose its audience before they even see it.</p>
        </div>
    </div>
</div>

<div id="blog-modal-2" class="pv-modal-container">
    <div class="pv-modal-overlay" onclick="closeBlogModal('blog-modal-2')"></div>
    <div class="pv-modal-panel">
        <div class="pv-modal-header">
            <span style="font-weight: bold; color: #00ACDF;">Social Media</span>
            <button class="pv-modal-close" onclick="closeBlogModal('blog-modal-2')">&times;</button>
        </div>
        <div class="pv-modal-body">
            <img alt="Social Media Trends" src="thumbnails/120304-800-500-Crop.jpg"/>
            <h2>The Rise of Short-Form Video Content</h2>
            <p>Why TikTok, Reels, and Shorts are dominating the marketing landscape and how your brand can leverage them. Attention spans are shrinking, and algorithms are prioritizing vertical video heavily.</p>
            <p>Brands that fail to adapt to this format are seeing their organic reach plummet. Short-form video requires a hook within the first 3 seconds, dynamic editing, and a clear value proposition, whether that's entertainment or education.</p>
        </div>
    </div>
</div>

<div id="blog-modal-3" class="pv-modal-container">
    <div class="pv-modal-overlay" onclick="closeBlogModal('blog-modal-3')"></div>
    <div class="pv-modal-panel">
        <div class="pv-modal-header">
            <span style="font-weight: bold; color: #00ACDF;">Branding</span>
            <button class="pv-modal-close" onclick="closeBlogModal('blog-modal-3')">&times;</button>
        </div>
        <div class="pv-modal-body">
            <img alt="Branding" src="thumbnails/120294-800-500-Crop.jpg"/>
            <h2>Why Your Brand Identity Matters More Than Ever</h2>
            <p>In a crowded digital marketplace, a strong, consistent brand identity is your most powerful asset. It's the difference between being a commodity and being a sought-after partner.</p>
            <p>Brand identity goes far beyond just a logo. It encompasses your tone of voice, your color palette, your typography, and the overall feeling a customer gets when they interact with your business. Consistency across all touchpoints is key to building trust.</p>
        </div>
    </div>
</div>

<div id="blog-modal-4" class="pv-modal-container">
    <div class="pv-modal-overlay" onclick="closeBlogModal('blog-modal-4')"></div>
    <div class="pv-modal-panel">
        <div class="pv-modal-header">
            <span style="font-weight: bold; color: #00ACDF;">Analytics</span>
            <button class="pv-modal-close" onclick="closeBlogModal('blog-modal-4')">&times;</button>
        </div>
        <div class="pv-modal-body">
            <img alt="Data Analytics" src="thumbnails/99711-533-600-Crop.jpg"/>
            <h2>Data-Driven Decisions in Modern Marketing</h2>
            <p>Stop guessing. Learn how to leverage analytics to maximize your ROI and understand your customers better. The days of "spray and pray" marketing are long gone.</p>
            <p>By implementing robust tracking and analyzing user behavior, you can identify which channels are driving the highest quality leads, where users are dropping off in your funnel, and what content resonates most deeply with your target audience.</p>
        </div>
    </div>
</div>
`;
html = html.replace('</main>', modalsHtml + '\n</main>');

// 6. Add JS
const jsCode = `
<script>
    function openBlogModal(id) {
        const modal = document.getElementById(id);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    function closeBlogModal(id) {
        const modal = document.getElementById(id);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
</script>
`;
html = html.replace('</body>', jsCode + '\n</body>');

fs.writeFileSync('d:/My Web Sites/ProVenture-digital-agency/blog.html', html);
