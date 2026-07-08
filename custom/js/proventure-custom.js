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

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
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
            'about.html': '.pv-nav-about',
            'services.html': '.pv-nav-services',
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
        initHeaderThemeSwitch();
    }

    // Start initialization
    init();

})();
