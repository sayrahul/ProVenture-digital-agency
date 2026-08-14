import glob
import os
import re

def get_footer_html(prefix=''):
    return f'''<footer class="footer pv-aesthetic-footer">
				<!-- Ambient Aurora Glows -->
				<div class="pv-footer-glow pv-footer-glow-1"></div>
				<div class="pv-footer-glow pv-footer-glow-2"></div>

				<!-- Main Footer Body -->
				<div class="pv-footer-main">
					<div class="container-big">
						<div class="pv-footer-grid">
							<!-- Column 1: Brand Hub & Live Time Widget -->
							<div class="pv-footer-col pv-footer-brand-col">
								<a href="{prefix}index.html" class="pv-footer-logo-link" aria-label="ProVenture Digital Agency">
									<img src="{prefix}thumbnails/proventure-white-logo.png" alt="ProVenture Digital Agency" class="pv-footer-logo-img" width="220" height="52" loading="lazy" />
								</a>
								<p class="pv-footer-tagline">Transforming ambitious brands through strategic design, video storytelling, cutting-edge web technology, and performance marketing.</p>
								
								<!-- Live IST Clock Widget -->
								<div class="pv-footer-live-badge">
									<div class="pv-live-loc">
										<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
										<span>Chhatrapati Sambhajinagar, IN</span>
									</div>
									<div class="pv-live-time">
										<span class="pv-pulse-dot"></span>
										<span class="pv-footer-clock-time" id="pv-footer-ist-clock">Live Clock IST</span>
									</div>
								</div>

								<!-- Glowing Glassmorphic Social Orbs -->
								<div class="pv-footer-socials">
									<span class="pv-socials-label">Follow Our Journey</span>
									<div class="pv-socials-group">
										<a href="https://www.linkedin.com/company/proventurein/" target="_blank" rel="noopener noreferrer" class="pv-social-orb pv-orb-linkedin" aria-label="ProVenture LinkedIn" title="LinkedIn">
											<svg viewBox="0 0 448 512"><path d="M100.3 448H7V148.9h93.3V448zm-46.6-341C24 107 0 83 0 53.3 0 23.6 24 0 53.7 0s53.7 23.6 53.7 53.3c0 29.6-24 53.7-53.7 53.7zM447.9 448h-92.4V302.4c0-34.7-12.5-58.4-43.7-58.4-23.9 0-38.1 16.1-44.4 31.6-2.3 5.4-2.9 12.9-2.9 20.4V448h-92.4s1.2-270.4 0-299.1h92.4v42.4c12.3-19 34.4-46 83.7-46 61.2 0 107.1 39.9 107.1 125.4V448z"/></svg>
										</a>
										<a href="https://www.instagram.com/proventureIN/" target="_blank" rel="noopener noreferrer" class="pv-social-orb pv-orb-instagram" aria-label="ProVenture Instagram" title="Instagram">
											<svg viewBox="0 0 448 512"><path d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z"/></svg>
										</a>
										<a href="https://www.facebook.com/ProVentureIN/" target="_blank" rel="noopener noreferrer" class="pv-social-orb pv-orb-facebook" aria-label="ProVenture Facebook" title="Facebook">
											<svg viewBox="0 0 320 512"><path d="M279.14 288l14.22-92.66h-88.91v-60.13c0-25.35 12.42-50.06 52.24-50.06H293V6.26S259.77 0 225.36 0c-73.61 0-121.36 44.38-121.36 124.72v70.62H22.89V288h81.11v224h100.17V288z"/></svg>
										</a>
										<a href="https://wa.me/919595997711" target="_blank" rel="noopener noreferrer" class="pv-social-orb pv-orb-whatsapp" aria-label="ProVenture WhatsApp" title="WhatsApp">
											<svg viewBox="0 0 448 512"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>
										</a>
									</div>
								</div>
							</div>

							<!-- Column 2: Agency Services -->
							<div class="pv-footer-col">
								<h3 class="pv-footer-heading">Our Services</h3>
								<ul class="pv-footer-nav-list">
									<li><a href="{prefix}digital-marketing.html" class="pv-footer-link"><span>Digital Marketing</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="{prefix}web-development.html" class="pv-footer-link"><span>Web Development</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="{prefix}search-engine-optimization.html" class="pv-footer-link"><span>SEO &amp; Growth</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="{prefix}social-media.html" class="pv-footer-link"><span>Social Media</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="{prefix}graphic-design.html" class="pv-footer-link"><span>Graphic &amp; Branding</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="{prefix}video-production.html" class="pv-footer-link"><span>Video Production</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="{prefix}ai-services.html" class="pv-footer-link"><span>AI &amp; Automation</span><span class="pv-link-arrow">→</span></a></li>
								</ul>
							</div>

							<!-- Column 3: Company Navigation -->
							<div class="pv-footer-col">
								<h3 class="pv-footer-heading">Company</h3>
								<ul class="pv-footer-nav-list">
									<li><a href="{prefix}about.html" class="pv-footer-link"><span>About Agency</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="https://portfolio.proventure.in/" target="_blank" rel="noopener noreferrer" class="pv-footer-link"><span>Our Portfolio</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="{prefix}clients.html" class="pv-footer-link"><span>Client Stories</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="{prefix}pricing.html" class="pv-footer-link"><span>Pricing Packages</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="{prefix}blog.html" class="pv-footer-link"><span>Insights &amp; Blog</span><span class="pv-link-arrow">→</span></a></li>
									<li><a href="{prefix}contact.html" class="pv-footer-link"><span>Contact Us</span><span class="pv-link-arrow">→</span></a></li>
								</ul>
							</div>

							<!-- Column 4: Contact & Quick Inquiry -->
							<div class="pv-footer-col pv-footer-contact-col">
								<h3 class="pv-footer-heading">Get in Touch</h3>
								<div class="pv-footer-contact-items">
									<a href="tel:+919595997711" class="pv-contact-card">
										<div class="pv-contact-icon">
											<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
										</div>
										<div class="pv-contact-text">
											<span class="pv-contact-sub">Direct Call</span>
											<span class="pv-contact-val">+91 95959 97711</span>
										</div>
									</a>

									<a href="mailto:info@proventure.in" class="pv-contact-card">
										<div class="pv-contact-icon">
											<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
										</div>
										<div class="pv-contact-text">
											<span class="pv-contact-sub">Email Us</span>
											<span class="pv-contact-val">info@proventure.in</span>
										</div>
									</a>

									<div class="pv-contact-card">
										<div class="pv-contact-icon">
											<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
										</div>
										<div class="pv-contact-text">
											<span class="pv-contact-sub">Headquarters</span>
											<span class="pv-contact-val">Kanchanwadi, Chhatrapati Sambhajinagar (MH), IN</span>
										</div>
									</div>
								</div>

								<!-- Quick Inquiry Form -->
								<div class="pv-footer-newsletter-wrap">
									<span class="pv-newsletter-title">Subscribe to Growth Insights</span>
									<div class="pv-footer-newsletter-form">
										<div class="pv-newsletter-input-group">
											<input type="email" class="pv-newsletter-input" placeholder="Enter your business email" required aria-label="Business Email" />
											<button type="button" class="pv-newsletter-submit" aria-label="Subscribe">
												<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
											</button>
										</div>
										<div class="pv-newsletter-feedback"></div>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Bottom Legal Bar -->
				<div class="pv-footer-bottom">
					<div class="container-big">
						<div class="pv-footer-bottom-inner">
							<div class="pv-copyright-text">
								&copy; 2026 <strong>ProVenture Digital Agency</strong>. All rights reserved.
							</div>
							
							<div class="pv-legal-links">
								<a href="{prefix}legal.html" class="pv-legal-link">Legal Notice</a>
								<span class="pv-legal-sep">•</span>
								<a href="{prefix}privacy.html" class="pv-legal-link">Privacy Policy</a>
								<span class="pv-legal-sep">•</span>
								<a href="{prefix}terms.html" class="pv-legal-link">Terms &amp; Conditions</a>
								<span class="pv-legal-sep">•</span>
								<a href="{prefix}pricing.html" class="pv-legal-link">Pricing</a>
							</div>

							<div class="pv-footer-extra">
								<span class="pv-badge-india">Crafted with Passion &amp; Precision in India 🇮🇳</span>
								<button type="button" class="pv-footer-top-trigger" id="pv-footer-top-btn" aria-label="Scroll to top">
									<span>Top</span>
									<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg>
								</button>
							</div>
						</div>
					</div>
				</div>
			</footer>'''

def run():
    footer_regex = re.compile(r'<footer[\s\S]*?</footer>', re.IGNORECASE)
    files = glob.glob('*.html') + glob.glob('blog/*.html')
    updated_count = 0
    for f in files:
        prefix = '../' if os.path.dirname(f) == 'blog' else ''
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        # Fix legacy preventure typo if found
        content = content.replace('https://www.preventure.in', 'https://www.proventure.in')
        
        new_footer = get_footer_html(prefix)
        new_content, n = footer_regex.subn(new_footer, content, count=1)
        if n > 0:
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(new_content)
            updated_count += 1
            print(f'Successfully updated: {f}')
        else:
            print(f'Warning: Could not match footer in {f}')

    print(f'Total updated files: {updated_count}/{len(files)}')

if __name__ == '__main__':
    run()
