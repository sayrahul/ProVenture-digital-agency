/**
 * ProVenture Performance Optimizations
 * Lazy loading, image optimization, and performance enhancements
 */

(function () {
    'use strict';

    // ========================================
    // 1. LAZY LOADING IMAGES
    // ========================================
    function initLazyLoading() {
        // Clear any stuck preloader is-loading class immediately
        document.querySelectorAll('.is-loading').forEach(el => el.classList.remove('is-loading'));

        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (img.complete) {
                img.classList.add('loaded');
            } else {
                img.addEventListener('load', function () {
                    this.classList.add('loaded');
                });
                img.addEventListener('error', function () {
                    this.classList.add('loaded');
                });
            }
        });
    }

    // ========================================
    // 2. WEBP IMAGE SUPPORT DETECTION
    // ========================================
    function checkWebPSupport() {
        const webP = new Image();
        webP.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
        webP.onload = webP.onerror = function () {
            if (webP.height === 2) {
                document.documentElement.classList.add('webp-support');
            } else {
                document.documentElement.classList.add('no-webp');
            }
        };
    }

    // ========================================
    // 3. DEFER NON-CRITICAL CSS
    // ========================================
    function loadDeferredStyles() {
        const deferredStyles = document.querySelectorAll('link[rel="preload"][as="style"]');
        deferredStyles.forEach(link => {
            link.addEventListener('load', function () {
                this.rel = 'stylesheet';
            });
        });
    }

    // ========================================
    // 4. OPTIMIZE FONT LOADING
    // ========================================
    function optimizeFontLoading() {
        if ('fonts' in document) {
            // Font loading API support
            Promise.all([
                document.fonts.load('400 1em Inter'),
                document.fonts.load('700 1em Inter'),
                document.fonts.load('400 1em Outfit'),
                document.fonts.load('700 1em Outfit')
            ]).then(() => {
                document.documentElement.classList.add('fonts-loaded');
            }).catch(err => {
                console.warn('Font loading failed:', err);
            });
        }
    }

    // ========================================
    // 5. REDUCE LAYOUT SHIFTS
    // ========================================
    function preventLayoutShift() {
        // Add aspect ratio to images without dimensions
        const images = document.querySelectorAll('img:not([width]):not([height])');
        images.forEach(img => {
            if (img.naturalWidth && img.naturalHeight) {
                const aspectRatio = (img.naturalHeight / img.naturalWidth) * 100;
                img.style.aspectRatio = `${img.naturalWidth} / ${img.naturalHeight}`;
            }
        });
    }

    // ========================================
    // 6. DEBOUNCE SCROLL/RESIZE EVENTS
    // ========================================
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // ========================================
    // 7. OPTIMIZE SCROLL PERFORMANCE
    // ========================================
    function optimizeScrollPerformance() {
        let ticking = false;
        let lastScrollY = window.pageYOffset;

        const updateScroll = () => {
            lastScrollY = window.pageYOffset;
            ticking = false;

            // Add/remove scrolled class
            document.body.classList.toggle('scrolled', lastScrollY > 50);
        };

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(updateScroll);
                ticking = true;
            }
        }, { passive: true });
    }

    // ========================================
    // 8. PRELOAD CRITICAL RESOURCES
    // ========================================
    function preloadCriticalResources() {
        // Preload hero images
        const heroImages = document.querySelectorAll('.hero img');
        heroImages.forEach(img => {
            if (img.src) {
                const link = document.createElement('link');
                link.rel = 'preload';
                link.as = 'image';
                link.href = img.src;
                document.head.appendChild(link);
            }
        });
    }

    // ========================================
    // 9. REDUCE JAVASCRIPT EXECUTION TIME
    // ========================================
    function deferNonCriticalJS() {
        // Defer analytics and non-critical scripts
        const scripts = document.querySelectorAll('script[data-defer]');
        scripts.forEach(script => {
            const newScript = document.createElement('script');
            newScript.src = script.dataset.src;
            newScript.defer = true;
            document.body.appendChild(newScript);
        });
    }

    // ========================================
    // 10. NETWORK INFORMATION API
    // ========================================
    function adaptToNetworkSpeed() {
        if ('connection' in navigator) {
            const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;

            if (connection) {
                const effectiveType = connection.effectiveType;

                // Disable heavy animations on slow connections
                if (effectiveType === 'slow-2g' || effectiveType === '2g') {
                    document.documentElement.classList.add('slow-connection');

                    // Disable cursor trail
                    const cursorTrails = document.querySelectorAll('.pv-cursor-trail');
                    cursorTrails.forEach(trail => trail.remove());

                    // Disable parallax
                    const parallaxElements = document.querySelectorAll('.pv-parallax');
                    parallaxElements.forEach(el => el.classList.remove('pv-parallax'));
                }
            }
        }
    }

    // ========================================
    // 11. INTERSECTION OBSERVER FOR ANIMATIONS
    // ========================================
    function initIntersectionObserver() {
        const animatedElements = document.querySelectorAll('[data-animate]');

        if (animatedElements.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        animatedElements.forEach(el => observer.observe(el));
    }

    // ========================================
    // 12. CACHE API RESPONSES
    // ========================================
    function cacheAPIResponses() {
        if ('caches' in window) {
            // Cache contact form submissions for offline support
            const CACHE_NAME = 'proventure-api-v1';

            window.addEventListener('fetch', event => {
                if (event.request.url.includes('/api/')) {
                    event.respondWith(
                        caches.match(event.request).then(response => {
                            return response || fetch(event.request).then(fetchResponse => {
                                return caches.open(CACHE_NAME).then(cache => {
                                    cache.put(event.request, fetchResponse.clone());
                                    return fetchResponse;
                                });
                            });
                        })
                    );
                }
            });
        }
    }

    // ========================================
    // 13. PERFORMANCE MONITORING
    // ========================================
    function monitorPerformance() {
        if ('PerformanceObserver' in window) {
            // Monitor Largest Contentful Paint
            const lcpObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                // LCP value: lastEntry.renderTime || lastEntry.loadTime
            });
            lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

            // Monitor First Input Delay
            const fidObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    // FID value: entry.processingStart - entry.startTime
                });
            });
            fidObserver.observe({ entryTypes: ['first-input'] });

            // Monitor Cumulative Layout Shift
            let clsValue = 0;
            const clsObserver = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                        // CLS value: clsValue
                    }
                }
            });
            clsObserver.observe({ entryTypes: ['layout-shift'] });
        }
    }

    // ========================================
    // 14. REDUCE MAIN THREAD WORK
    // ========================================
    function optimizeMainThread() {
        // Use requestIdleCallback for non-critical work
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => {
                // Initialize non-critical features
                initIntersectionObserver();
                monitorPerformance();
            });
        } else {
            // Fallback to setTimeout
            setTimeout(() => {
                initIntersectionObserver();
                monitorPerformance();
            }, 1000);
        }
    }

    // ========================================
    // 15. MOBILE-SPECIFIC OPTIMIZATIONS
    // ========================================
    function mobileOptimizations() {
        const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

        if (isMobile) {
            document.documentElement.classList.add('is-mobile');

            // Disable hover effects on mobile
            document.addEventListener('touchstart', function () { }, { passive: true });

            // Optimize touch events
            document.addEventListener('touchmove', function (e) {
                // Prevent default only when necessary
            }, { passive: true });
        }
    }

    // ========================================
    // INITIALIZE ALL OPTIMIZATIONS
    // ========================================
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        // Run critical optimizations immediately
        checkWebPSupport();
        mobileOptimizations();
        optimizeScrollPerformance();
        adaptToNetworkSpeed();

        // Run on load
        window.addEventListener('load', () => {
            initLazyLoading();
            loadDeferredStyles();
            optimizeFontLoading();
            preventLayoutShift();
            preloadCriticalResources();
            optimizeMainThread();
        });
    }

    // Start initialization
    init();

})()
