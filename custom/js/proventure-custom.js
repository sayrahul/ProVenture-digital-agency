/**
 * ProVenture Custom JavaScript
 * Original interactive elements for ProVenture Digital Agency
 * Author: ProVenture Team
 * Version: 1.0.0
 */

(function () {
    'use strict';

    // ========================================
    // 1. SCROLL PROGRESS INDICATOR
    // ========================================
    function initScrollIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'pv-scroll-indicator';
        document.body.appendChild(indicator);

        window.addEventListener('scroll', () => {
            const winScroll = document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            indicator.style.width = scrolled + '%';
        });
    }

    // ========================================
    // 2. ANIMATED COUNTER FOR STATS
    // ========================================
    function animateCounter(element, target, duration = 2000) {
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;
        const suffix = element.getAttribute('data-suffix') || '';
        const prefix = element.getAttribute('data-prefix') || '';

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = prefix + target + suffix;
                clearInterval(timer);
            } else {
                element.textContent = prefix + Math.floor(current) + suffix;
            }
        }, 16);
    }

    function initCounters() {
        const counters = document.querySelectorAll('.pv-stat-number');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    entry.target.classList.add('counted');
                    const target = parseInt(entry.target.getAttribute('data-count'));
                    animateCounter(entry.target, target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    }

    // ========================================
    // 3. SMOOTH REVEAL ON SCROLL
    // ========================================
    function initScrollReveal() {
        const elements = document.querySelectorAll('.pv-reveal');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('pv-revealed');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        elements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });

        // Add revealed class styling
        const style = document.createElement('style');
        style.textContent = `
            .pv-revealed {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
        `;
        document.head.appendChild(style);
    }

    // ========================================
    // 4. PARALLAX EFFECT
    // ========================================
    function initParallax() {
        const parallaxElements = document.querySelectorAll('.pv-parallax');

        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;

            parallaxElements.forEach(el => {
                const speed = el.getAttribute('data-speed') || 0.5;
                const yPos = -(scrolled * speed);
                el.style.transform = `translateY(${yPos}px)`;
            });
        });
    }

    // ========================================
    // 5. TYPING EFFECT
    // ========================================
    function typeWriter(element, text, speed = 100) {
        let i = 0;
        element.textContent = '';

        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }

        type();
    }

    function initTypingEffect() {
        const typingElements = document.querySelectorAll('.pv-typing');

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('typed')) {
                    entry.target.classList.add('typed');
                    const text = entry.target.getAttribute('data-text');
                    const speed = parseInt(entry.target.getAttribute('data-speed')) || 100;
                    typeWriter(entry.target, text, speed);
                }
            });
        }, { threshold: 0.5 });

        typingElements.forEach(el => observer.observe(el));
    }

    // ========================================
    // 6. MAGNETIC BUTTON EFFECT
    // ========================================
    function initMagneticButtons() {
        const buttons = document.querySelectorAll('.pv-magnetic');

        buttons.forEach(button => {
            button.addEventListener('mousemove', (e) => {
                const rect = button.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;

                button.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
            });

            button.addEventListener('mouseleave', () => {
                button.style.transform = 'translate(0, 0)';
            });
        });
    }

    // ========================================
    // 7. CUSTOM CURSOR TRAIL
    // ========================================
    function initCursorTrail() {
        if (window.innerWidth < 768) return; // Skip on mobile

        const trail = [];
        const trailLength = 10;

        for (let i = 0; i < trailLength; i++) {
            const dot = document.createElement('div');
            dot.className = 'pv-cursor-trail';
            dot.style.cssText = `
                position: fixed;
                width: ${10 - i}px;
                height: ${10 - i}px;
                background: rgba(0, 172, 223, ${1 - i / trailLength});
                border-radius: 50%;
                pointer-events: none;
                z-index: 9998;
                transition: transform 0.1s ease;
            `;
            document.body.appendChild(dot);
            trail.push(dot);
        }

        let mouseX = 0, mouseY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        function animateTrail() {
            let x = mouseX;
            let y = mouseY;

            trail.forEach((dot, index) => {
                dot.style.left = x + 'px';
                dot.style.top = y + 'px';

                const nextDot = trail[index + 1] || trail[0];
                x += (parseInt(nextDot.style.left) - x) * 0.3;
                y += (parseInt(nextDot.style.top) - y) * 0.3;
            });

            requestAnimationFrame(animateTrail);
        }

        animateTrail();
    }

    // ========================================
    // 8. FORM VALIDATION
    // ========================================
    function initFormValidation() {
        const forms = document.querySelectorAll('.pv-form');

        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();

                const inputs = form.querySelectorAll('input[required], textarea[required]');
                let isValid = true;

                inputs.forEach(input => {
                    if (!input.value.trim()) {
                        isValid = false;
                        input.classList.add('pv-error');

                        // Remove error class after 3 seconds
                        setTimeout(() => input.classList.remove('pv-error'), 3000);
                    }
                });

                if (isValid) {
                    // Submit form
                    form.submit();
                }
            });
        });

        // Add error styling
        const style = document.createElement('style');
        style.textContent = `
            .pv-error {
                border-color: #ff4444 !important;
                animation: pvShake 0.5s;
            }
            @keyframes pvShake {
                0%, 100% { transform: translateX(0); }
                25% { transform: translateX(-10px); }
                75% { transform: translateX(10px); }
            }
        `;
        document.head.appendChild(style);
    }

    // ========================================
    // 9. LAZY LOAD IMAGES
    // ========================================
    function initLazyLoad() {
        const images = document.querySelectorAll('img[data-src]');

        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.getAttribute('data-src');
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    // ========================================
    // 10. BACK TO TOP BUTTON
    // ========================================
    function initBackToTop() {
        const button = document.createElement('button');
        button.className = 'pv-back-to-top';
        button.innerHTML = '↑';
        button.style.cssText = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #00ACDF, #0099cc);
            color: white;
            border: none;
            border-radius: 50%;
            font-size: 24px;
            cursor: pointer;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            z-index: 1000;
            box-shadow: 0 4px 15px rgba(0, 172, 223, 0.3);
        `;
        document.body.appendChild(button);

        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                button.style.opacity = '1';
                button.style.visibility = 'visible';
            } else {
                button.style.opacity = '0';
                button.style.visibility = 'hidden';
            }
        });

        button.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ========================================
    // 11. MOBILE NAV ACTIVE STATE
    // ========================================
    function initMobileNavActiveState() {
        const nav = document.querySelector('.pv-mobile-nav');
        if (!nav) return;

        const path = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
        const map = {
            'index.html': '.pv-nav-home',
            'services.html': '.pv-nav-services',
            'pricing.html': '.pv-nav-pricing',
            'clients.html': '.pv-nav-clients',
            'contact.html': '.pv-nav-contact'
        };

        const selector = map[path];
        if (!selector) return;
        const link = nav.querySelector(selector);
        if (link) link.classList.add('active');
    }

    // ========================================
    // 12. HEADER THEME SWITCH (NON-INDEX)
    // ========================================
    function initHeaderThemeSwitch() {
        const rootPath = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
        if (rootPath === 'index.html' || rootPath === '') return;
        if (!document.querySelector('.header')) return;

        function luminanceFromColor(color) {
            const m = color && color.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/i);
            if (!m) return null;
            const r = parseInt(m[1], 10);
            const g = parseInt(m[2], 10);
            const b = parseInt(m[3], 10);
            return (0.299 * r) + (0.587 * g) + (0.114 * b);
        }

        function isLightContextAtHeader() {
            const headerEl = document.querySelector('.header');
            let prevPointerEvents = '';
            if (headerEl) {
                prevPointerEvents = headerEl.style.pointerEvents;
                headerEl.style.pointerEvents = 'none';
            }

            const y = Math.min(74, window.innerHeight - 1);
            const x = Math.floor(window.innerWidth * 0.5);
            const el = document.elementFromPoint(x, y);

            if (headerEl) {
                headerEl.style.pointerEvents = prevPointerEvents;
            }

            if (!el) return false;

            if (el.closest('.bg-white')) return true;
            if (el.closest('.bg-dark, .bg-gradient')) return false;

            let n = el;
            while (n && n !== document.body) {
                const bg = window.getComputedStyle(n).backgroundColor;
                const lum = luminanceFromColor(bg);
                if (lum !== null && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') {
                    return lum > 180;
                }
                n = n.parentElement;
            }

            const bodyBg = window.getComputedStyle(document.body).backgroundColor;
            const bodyLum = luminanceFromColor(bodyBg);
            return bodyLum !== null ? bodyLum > 180 : false;
        }

        function applyHeaderTheme() {
            if (document.documentElement.classList.contains('shownav')) return;
            document.body.classList.toggle('bg-white-active', isLightContextAtHeader());
        }

        window.addEventListener('scroll', applyHeaderTheme, { passive: true });
        window.addEventListener('resize', applyHeaderTheme);
        window.addEventListener('load', applyHeaderTheme);
        setTimeout(applyHeaderTheme, 0);
    }

    // ========================================
    // INTERACTIVE PRICING CALCULATOR
    // ========================================
    function initPricingCalculator() {
        const totalAmountEl = document.getElementById('pv-calc-total-amount');
        const savingNoteEl = document.getElementById('pv-calc-saving-note');
        const options = document.querySelectorAll('.pv-calc-option');
        const billingSwitch = document.getElementById('billing-switch');

        if (!totalAmountEl || !options.length) return;

        function calculateTotal() {
            let isAnnual = billingSwitch ? billingSwitch.classList.contains('is-annual') : false;
            let total = 0;

            options.forEach(opt => {
                if (opt.checked) {
                    const price = parseInt(isAnnual ? opt.getAttribute('data-annual') : opt.getAttribute('data-monthly'));
                    total += isNaN(price) ? 0 : price;
                }
            });

            totalAmountEl.textContent = total.toLocaleString('en-IN');
            if (savingNoteEl) {
                savingNoteEl.textContent = isAnnual ? 'Annual Billing (10% Off Applied)' : 'Monthly Billing';
                savingNoteEl.style.color = isAnnual ? '#38bdf8' : '#94a3b8';
            }
        }

        options.forEach(opt => opt.addEventListener('change', calculateTotal));
        if (billingSwitch) {
            billingSwitch.addEventListener('click', () => setTimeout(calculateTotal, 50));
        }

        calculateTotal();
    }

    // ========================================
    // VIDEO LIGHTBOX MODAL
    // ========================================
    function initVideoLightboxModal() {
        const videoTriggers = document.querySelectorAll('.sitevideo video, [data-video-src]');
        if (!videoTriggers.length) return;

        let overlay = document.querySelector('.pv-video-modal-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.className = 'pv-video-modal-overlay';
            overlay.innerHTML = `
                <div class="pv-video-modal-container">
                    <button class="pv-video-modal-close" aria-label="Close video">&times;</button>
                    <video class="pv-video-modal-video" controls autoplay></video>
                </div>
            `;
            document.body.appendChild(overlay);
        }

        const modalVideo = overlay.querySelector('.pv-video-modal-video');
        const closeBtn = overlay.querySelector('.pv-video-modal-close');

        function closeModal() {
            overlay.classList.remove('is-open');
            if (modalVideo) {
                modalVideo.pause();
                modalVideo.src = '';
            }
        }

        videoTriggers.forEach(trigger => {
            trigger.style.cursor = 'pointer';
            trigger.addEventListener('click', (e) => {
                let videoSrc = '';
                if (trigger.tagName === 'VIDEO') {
                    const source = trigger.querySelector('source');
                    videoSrc = source ? source.src : trigger.src;
                } else {
                    videoSrc = trigger.getAttribute('data-video-src');
                }

                if (videoSrc && modalVideo) {
                    e.preventDefault();
                    modalVideo.src = videoSrc;
                    overlay.classList.add('is-open');
                    modalVideo.play().catch(() => {});
                }
            });
        });

        if (closeBtn) closeBtn.addEventListener('click', closeModal);
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) closeModal();
        });
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && overlay.classList.contains('is-open')) closeModal();
        });
    }

    // ========================================
    // STICKY CTA BAR
    // ========================================
    function initStickyCta() {
        if (document.querySelector('.pv-sticky-cta')) return;

        const bar = document.createElement('div');
        bar.className = 'pv-sticky-cta';
        bar.innerHTML = `
            <div class="pv-sticky-cta-text">
                Ready to grow your brand?
                <span>Get a free consultation today</span>
            </div>
            <div class="pv-sticky-cta-actions">
                <a href="contact.html" class="pv-btn-primary">Get a Quote</a>
            </div>
        `;
        document.body.appendChild(bar);

        window.addEventListener('scroll', () => {
            bar.classList.toggle('is-visible', window.pageYOffset > 600);
        }, { passive: true });
    }

    // ========================================
    // WHATSAPP FAB
    // ========================================
    function initWhatsAppFab() {
        if (document.querySelector('.pv-whatsapp-fab')) return;

        const fab = document.createElement('a');
        fab.className = 'pv-whatsapp-fab';
        fab.href = 'https://wa.me/919595997711';
        fab.target = '_blank';
        fab.rel = 'noopener noreferrer';
        fab.setAttribute('aria-label', 'Chat on WhatsApp');
        fab.innerHTML = '<svg viewBox="0 0 448 512" aria-hidden="true"><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>';
        document.body.appendChild(fab);
    }

    // ========================================
    // TESTIMONIALS CAROUSEL
    // ========================================
    function initTestimonialsCarousel() {
        const track = document.querySelector('.pv-testimonials-track');
        if (!track) return;

        const slides = track.querySelectorAll('.pv-testimonial-slide');
        const prevBtn = document.querySelector('.pv-testimonials-prev');
        const nextBtn = document.querySelector('.pv-testimonials-next');
        const dotsWrap = document.querySelector('.pv-testimonials-dots');
        let current = 0;

        function goTo(index) {
            current = Math.max(0, Math.min(index, slides.length - 1));
            const slide = slides[current];
            if (slide) {
                track.scrollTo({ left: slide.offsetLeft - track.offsetLeft, behavior: 'smooth' });
            }
            if (dotsWrap) {
                dotsWrap.querySelectorAll('button').forEach((dot, i) => {
                    dot.classList.toggle('is-active', i === current);
                });
            }
        }

        if (dotsWrap) {
            dotsWrap.innerHTML = '';
            slides.forEach((_, i) => {
                const dot = document.createElement('button');
                dot.setAttribute('aria-label', 'Go to testimonial ' + (i + 1));
                if (i === 0) dot.classList.add('is-active');
                dot.addEventListener('click', () => goTo(i));
                dotsWrap.appendChild(dot);
            });
        }

        if (prevBtn) prevBtn.addEventListener('click', () => goTo(current - 1));
        if (nextBtn) nextBtn.addEventListener('click', () => goTo(current + 1));
    }

    // ========================================
    // PROJECT SLIDER NAV
    // ========================================
    function initProjectSliderNav() {
        const slider = document.querySelector('.projectslider');
        const counter = document.querySelector('.pv-project-counter');
        const prevBtn = document.querySelector('.pv-project-prev');
        const nextBtn = document.querySelector('.pv-project-next');
        if (!slider || !window.jQuery) return;

        const $slider = window.jQuery(slider);
        const flkty = $slider.data('flickity');

        function updateCounter() {
            if (!counter || !flkty) return;
            counter.textContent = (flkty.selectedIndex + 1) + ' / ' + flkty.slides.length;
        }

        if (flkty) {
            $slider.on('select.flickity', updateCounter);
            updateCounter();
        }

        if (prevBtn && flkty) prevBtn.addEventListener('click', () => flkty.previous());
        if (nextBtn && flkty) nextBtn.addEventListener('click', () => flkty.next());
    }

    // ========================================
    // CLIENT FILTERS
    // ========================================
    function initClientFilters() {
        const filters = document.querySelectorAll('.pv-client-filter');
        const items = document.querySelectorAll('.clients-item[data-category]');
        if (!filters.length || !items.length) return;

        filters.forEach(btn => {
            btn.addEventListener('click', () => {
                filters.forEach(f => f.classList.remove('is-active'));
                btn.classList.add('is-active');
                const cat = btn.getAttribute('data-filter');
                items.forEach(item => {
                    const show = cat === 'all' || item.getAttribute('data-category') === cat;
                    item.classList.toggle('is-hidden', !show);
                });
            });
        });
    }

    function initMobileNavToggle() {
        const toggles = document.querySelectorAll('.navtoggle');
        toggles.forEach(toggle => {
            toggle.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                document.documentElement.classList.toggle('shownav');
            });
        });

        document.querySelectorAll('.mainnav a').forEach(link => {
            link.addEventListener('click', function () {
                document.documentElement.classList.remove('shownav');
            });
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                document.documentElement.classList.remove('shownav');
            }
        });
    }

    // ========================================
    // INITIALIZE ALL FEATURES
    // ========================================
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        // Initialize all features
        initScrollIndicator();
        initCounters();
        initScrollReveal();
        initParallax();
        initTypingEffect();
        initMagneticButtons();
        initCursorTrail();
        initFormValidation();
        initLazyLoad();
        initBackToTop();
        initMobileNavActiveState();
        initMobileNavToggle();
        initHeaderThemeSwitch();
        initPricingCalculator();
        initVideoLightboxModal();
        initTestimonialsCarousel();
        initClientFilters();
        setTimeout(initProjectSliderNav, 500);
    }

    // Start initialization
    init();

})();
