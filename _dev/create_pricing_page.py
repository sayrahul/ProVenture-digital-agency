import re

with open('services.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract header
header_match = re.search(r'(?s)(.*?<main class=\"main\" id=\"C_T_DefaultRegion\">)', content)
header = header_match.group(1)

# Modify title and description in header
header = re.sub(r'<title>.*?</title>', '<title>Pricing Plans & Packages | ProVenture Digital Agency</title>', header)
header = re.sub(r'<meta content=\"Explore ProVenture services.*?(?=\" name=\"description\" />)', '<meta content=\"Discover ProVenture\'s flexible pricing for digital marketing, web design, and video production services.', header)
header = re.sub(r'<link href=\"https://proventure.in/services\" rel=\"canonical\" />', '<link href=\"https://proventure.in/pricing\" rel=\"canonical\" />', header)
header = re.sub(r'<meta content=\".*?\" property=\"og:title\" />', '<meta content=\"Pricing Plans & Packages | ProVenture Digital Agency\" property=\"og:title\" />', header)
header = re.sub(r'<meta content=\"Explore ProVenture services.*?(?=\" property=\"og:description\" />)', '<meta content=\"Discover ProVenture\'s flexible pricing for digital marketing, web design, and video production services.', header)
header = re.sub(r'<meta content=\"https://proventure.in/services\" property=\"og:url\" />', '<meta content=\"https://proventure.in/pricing\" property=\"og:url\" />', header)

# Extract footer and scripts
footer_match = re.search(r'(?s)(</main>.*)', content)
footer = footer_match.group(1)

# Generate Main Content
main_content = '''
	<div class=\"hero bg-white hero-small\">
		<div class=\"container-big scroll-parallax\">
			<div class=\"h1 nospan\">Pricing</div>
			<div class=\"grid-row twocol\">
				<div class=\"hero-topt\">
					<h1 class=\"toptitle\">Simple & Transparent Pricing</h1>
				</div>
				<div class=\"hero-lead\">
					<p>Choose the right plan for your business. We offer flexible pricing for every creative need.</p>
				</div>
			</div>
		</div>
	</div>

	<section class=\"pricing-tabs-section\" style=\"padding-top: 2rem;\">
		<div class=\"container-big\">
			<div class=\"pricing-tabs\">
				<button class=\"pricing-tab active\" data-target=\"tab-design\">Graphic Design & Web</button>
				<button class=\"pricing-tab\" data-target=\"tab-marketing\">Digital Marketing</button>
				<button class=\"pricing-tab\" data-target=\"tab-video\">Video Production</button>
			</div>

			<style>
				.pricing-tabs {
					display: flex;
					justify-content: center;
					gap: 1rem;
					margin-bottom: 3rem;
					flex-wrap: wrap;
				}
				.pricing-tab {
					padding: 1rem 2rem;
					font-size: 1.1rem;
					font-weight: 600;
					background: rgba(255, 255, 255, 0.5);
					border: 1px solid rgba(0, 0, 0, 0.1);
					border-radius: 50px;
					cursor: pointer;
					transition: all 0.3s ease;
					backdrop-filter: blur(10px);
					color: #333;
				}
				.pricing-tab:hover {
					background: rgba(255, 255, 255, 0.9);
					transform: translateY(-2px);
				}
				.pricing-tab.active {
					background: #000;
					color: #fff;
					border-color: #000;
				}
				.pricing-content {
					display: none;
					animation: fadeIn 0.5s ease forwards;
				}
				.pricing-content.active {
					display: block;
				}
				@keyframes fadeIn {
					from { opacity: 0; transform: translateY(10px); }
					to { opacity: 1; transform: translateY(0); }
				}
				.pricing-cards {
					display: grid;
					grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
					gap: 2rem;
					align-items: stretch;
				}
				.pricing-card {
					padding: 3rem 2rem;
					border-radius: 20px;
					background: rgba(255, 255, 255, 0.7);
					backdrop-filter: blur(20px);
					border: 1px solid rgba(255,255,255,0.5);
					box-shadow: 0 10px 30px rgba(0,0,0,0.05);
					display: flex;
					flex-direction: column;
					transition: transform 0.3s ease, box-shadow 0.3s ease;
				}
				.pricing-card:hover {
					transform: translateY(-10px);
					box-shadow: 0 20px 40px rgba(0,0,0,0.1);
				}
				.pricing-card.popular {
					background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(240,245,255,0.95));
					border: 1px solid rgba(0,0,0,0.1);
					position: relative;
				}
				.popular-badge {
					position: absolute;
					top: -15px;
					left: 50%;
					transform: translateX(-50%);
					background: #000;
					color: #fff;
					padding: 0.5rem 1.5rem;
					border-radius: 20px;
					font-size: 0.85rem;
					font-weight: 600;
					letter-spacing: 1px;
					text-transform: uppercase;
					white-space: nowrap;
				}
				.pricing-tier {
					font-size: 1.5rem;
					font-weight: 700;
					margin-bottom: 0.5rem;
				}
				.pricing-price {
					font-size: 3rem;
					font-weight: 800;
					margin-bottom: 1rem;
					line-height: 1;
				}
				.pricing-price span {
					font-size: 1rem;
					font-weight: 500;
					color: #666;
				}
				.pricing-desc {
					color: #555;
					margin-bottom: 2rem;
					font-size: 1rem;
					min-height: 48px;
				}
				.pricing-features {
					list-style: none;
					padding: 0;
					margin: 0 0 2rem 0;
					flex-grow: 1;
				}
				.pricing-features li {
					padding: 0.75rem 0;
					border-bottom: 1px solid rgba(0,0,0,0.05);
					display: flex;
					align-items: flex-start;
				}
				.pricing-features li:last-child {
					border-bottom: none;
				}
				.pricing-features li svg {
					width: 20px;
					height: 20px;
					margin-right: 10px;
					color: #10b981;
					flex-shrink: 0;
					margin-top: 2px;
				}
				.pricing-action {
					margin-top: auto;
				}
				.pricing-action .btn {
					width: 100%;
					text-align: center;
					display: block;
				}
			</style>

			<!-- Design Tab -->
			<div id=\"tab-design\" class=\"pricing-content active\">
				<div class=\"pricing-cards\">
					<!-- Design Basic -->
					<div class=\"pricing-card pv-glass-card\">
						<h3 class=\"pricing-tier\">Basic Design</h3>
						<div class=\"pricing-price\">₹4,999<span>/project</span></div>
						<p class=\"pricing-desc\">Perfect for startups and small businesses needing essential branding.</p>
						<ul class=\"pricing-features\">
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Logo Design (2 Concepts)</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Business Card & Letterhead</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Basic Brand Guidelines</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 2 Revisions</li>
						</ul>
						<div class=\"pricing-action\">
							<a href=\"contact.html?plan=design-basic\" class=\"btn btn-outline pv-btn-primary\">Get Started</a>
						</div>
					</div>
					<!-- Design Pro -->
					<div class=\"pricing-card pv-glass-card popular\">
						<div class=\"popular-badge\">Most Popular</div>
						<h3 class=\"pricing-tier\">Pro Web & Branding</h3>
						<div class=\"pricing-price\">₹24,999<span>/project</span></div>
						<p class=\"pricing-desc\">Comprehensive identity and online presence for growing brands.</p>
						<ul class=\"pricing-features\">
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Complete Branding Package</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 5-Page Responsive Website</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Essential SEO Setup</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 1 Month Free Hosting Support</li>
						</ul>
						<div class=\"pricing-action\">
							<a href=\"contact.html?plan=design-pro\" class=\"btn btn-outline pv-btn-primary\">Get Started</a>
						</div>
					</div>
					<!-- Design Enterprise -->
					<div class=\"pricing-card pv-glass-card\">
						<h3 class=\"pricing-tier\">Enterprise Custom</h3>
						<div class=\"pricing-price\">Custom</div>
						<p class=\"pricing-desc\">Full-scale digital platforms for established enterprises and e-commerce.</p>
						<ul class=\"pricing-features\">
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Custom E-commerce Development</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Advanced Payment Integrations</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Advanced UI/UX Prototyping</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Dedicated Priority Support</li>
						</ul>
						<div class=\"pricing-action\">
							<a href=\"contact.html?plan=design-enterprise\" class=\"btn btn-outline pv-btn-primary\">Contact Sales</a>
						</div>
					</div>
				</div>
			</div>

			<!-- Marketing Tab -->
			<div id=\"tab-marketing\" class=\"pricing-content\">
				<div class=\"pricing-cards\">
					<!-- Marketing Basic -->
					<div class=\"pricing-card pv-glass-card\">
						<h3 class=\"pricing-tier\">Social Starter</h3>
						<div class=\"pricing-price\">₹9,999<span>/mo</span></div>
						<p class=\"pricing-desc\">Build your audience with consistent media management.</p>
						<ul class=\"pricing-features\">
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 2 Social Media Platforms</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 8 High-Quality Posts/Month</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Basic Community Management</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Monthly Analytics Report</li>
						</ul>
						<div class=\"pricing-action\">
							<a href=\"contact.html?plan=marketing-basic\" class=\"btn btn-outline pv-btn-primary\">Get Started</a>
						</div>
					</div>
					<!-- Marketing Pro -->
					<div class=\"pricing-card pv-glass-card popular\">
						<div class=\"popular-badge\">Most Popular</div>
						<h3 class=\"pricing-tier\">Growth Marketing</h3>
						<div class=\"pricing-price\">₹24,999<span>/mo</span></div>
						<p class=\"pricing-desc\">Accelerate growth with combined organic and paid strategies.</p>
						<ul class=\"pricing-features\">
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 3 Social Media Platforms</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 15 Posts + 2 Reels/Month</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Paid Ads Management (Meta/Google)</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> On-Page SEO Optimization</li>
						</ul>
						<div class=\"pricing-action\">
							<a href=\"contact.html?plan=marketing-pro\" class=\"btn btn-outline pv-btn-primary\">Get Started</a>
						</div>
					</div>
					<!-- Marketing Enterprise -->
					<div class=\"pricing-card pv-glass-card\">
						<h3 class=\"pricing-tier\">360° Agency Partner</h3>
						<div class=\"pricing-price\">Custom</div>
						<p class=\"pricing-desc\">Your dedicated external marketing department.</p>
						<ul class=\"pricing-features\">
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Unlimited Social Media Support</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Multi-Channel Ad Campaigns & Remarketing</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Full Technical & Content SEO</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Dedicated Account Manager</li>
						</ul>
						<div class=\"pricing-action\">
							<a href=\"contact.html?plan=marketing-enterprise\" class=\"btn btn-outline pv-btn-primary\">Contact Sales</a>
						</div>
					</div>
				</div>
			</div>

			<!-- Video Tab -->
			<div id=\"tab-video\" class=\"pricing-content\">
				<div class=\"pricing-cards\">
					<!-- Video Basic -->
					<div class=\"pricing-card pv-glass-card\">
						<h3 class=\"pricing-tier\">Short-Form Content</h3>
						<div class=\"pricing-price\">₹14,999<span>/pkg</span></div>
						<p class=\"pricing-desc\">Engaging reels and shorts to boost your social reach.</p>
						<ul class=\"pricing-features\">
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 5 Edited Reels/Shorts (up to 60s)</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Color Correction & Grading</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Trending Audio & Subtitles</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 1 Revision Round</li>
						</ul>
						<div class=\"pricing-action\">
							<a href=\"contact.html?plan=video-basic\" class=\"btn btn-outline pv-btn-primary\">Get Started</a>
						</div>
					</div>
					<!-- Video Pro -->
					<div class=\"pricing-card pv-glass-card popular\">
						<div class=\"popular-badge\">Most Popular</div>
						<h3 class=\"pricing-tier\">Corporate Profile</h3>
						<div class=\"pricing-price\">₹34,999<span>/video</span></div>
						<p class=\"pricing-desc\">Professional brand storytelling for your website and presentations.</p>
						<ul class=\"pricing-features\">
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 1-Day On-Site Shoot (incl. gear)</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> 2-3 Minute Final Edit</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Scriptwriting & Storyboarding</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Voiceover & Royalty-Free Music</li>
						</ul>
						<div class=\"pricing-action\">
							<a href=\"contact.html?plan=video-pro\" class=\"btn btn-outline pv-btn-primary\">Get Started</a>
						</div>
					</div>
					<!-- Video Enterprise -->
					<div class=\"pricing-card pv-glass-card\">
						<h3 class=\"pricing-tier\">Commercial Ads</h3>
						<div class=\"pricing-price\">Custom</div>
						<p class=\"pricing-desc\">High-end TVCs and ad campaigns with full crew production.</p>
						<ul class=\"pricing-features\">
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Multi-Day Shoots</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Advanced Motion Graphics & VFX</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Drone & Specialty Camera Ops</li>
							<li><svg viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" d=\"M5 13l4 4L19 7\"></path></svg> Talent Sourcing & Direction</li>
						</ul>
						<div class=\"pricing-action\">
							<a href=\"contact.html?plan=video-enterprise\" class=\"btn btn-outline pv-btn-primary\">Contact Sales</a>
						</div>
					</div>
				</div>
			</div>
		</div>
	</section>

	<section class=\"project-cta page-cta\" style=\"margin-top: 5rem;\">
		<div class=\"container-big\">
			<div class=\"section-inset bg-gradient\">
				<span class=\"toptitle\">Not Sure What You Need?</span>
				<div class=\"flex-ctr\">
					<h2>Let\'s build a custom package for you</h2>
					<div class=\"button\">
						<a class=\"pagelink btn btn-outline\" href=\"contact.html\" title=\"ProVenture digital agency - Chhatrapati Sambhajinagar (Aurangabad)\">
							Talk to an Expert
						</a>
					</div>
				</div>
			</div>
		</div>
	</section>
'''

tabs_js = '''
<script type=\"text/javascript\">
	document.addEventListener('DOMContentLoaded', function() {
		const tabs = document.querySelectorAll('.pricing-tab');
		const contents = document.querySelectorAll('.pricing-content');

		tabs.forEach(tab => {
			tab.addEventListener('click', () => {
				tabs.forEach(t => t.classList.remove('active'));
				contents.forEach(c => c.classList.remove('active'));

				tab.classList.add('active');
				const targetId = tab.getAttribute('data-target');
				document.getElementById(targetId).classList.add('active');
			});
		});
	});
</script>
'''

footer = footer.replace('</body>', tabs_js + '</body>')

with open('pricing.html', 'w', encoding='utf-8') as f:
    f.write(header + main_content + footer)

print("Pricing page created successfully.")
