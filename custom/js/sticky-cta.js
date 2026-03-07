/**
 * Sticky CTA Button Component
 * Displays a floating "Get a Quote" button with smooth animations
 */

(function() {
    'use strict';

    // Configuration
    const config = {
        showDelay: 2000,        // Show after 2 seconds
        scrollThreshold: 300,   // Show after scrolling 300px
        ctaText: 'Get a Quote',
        ctaLink: 'contact.html',
        position: 'bottom-right' // bottom-right, bottom-left
    };

    // Create CTA button
    function createCTAButton() {
        const ctaContainer = document.createElement('div');
        ctaContainer.className = 'sticky-cta';
        ctaContainer.id = 'sticky-cta';
        ctaContainer.style.opacity = '0';
        
        const ctaButton = document.createElement('a');
        ctaButton.href = config.ctaLink;
        ctaButton.className = 'sticky-cta-btn pv-magnetic';
        ctaButton.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 8px; vertical-align: middle;">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
            <span>${config.ctaText}</span>
        `;
        
        ctaContainer.appendChild(ctaButton);
        document.body.appendChild(ctaContainer);
        
        return ctaContainer;
    }

    // Show/hide CTA based on scroll
    function handleScroll() {
        const ctaElement = document.getElementById('sticky-cta');
        if (!ctaElement) return;
        
        const scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollPosition > config.scrollThreshold) {
            ctaElement.style.opacity = '1';
            ctaElement.style.transform = 'translateY(0)';
        } else {
            ctaElement.style.opacity = '0';
            ctaElement.style.transform = 'translateY(20px)';
        }
    }

    // Initialize
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        // Create CTA button after delay
        setTimeout(function() {
            const ctaElement = createCTAButton();
            
            // Add scroll listener
            let scrollTimeout;
            window.addEventListener('scroll', function() {
                if (scrollTimeout) {
                    window.cancelAnimationFrame(scrollTimeout);
                }
                scrollTimeout = window.requestAnimationFrame(handleScroll);
            });
            
            // Initial check
            handleScroll();
        }, config.showDelay);
    }

    // Start initialization
    init();
})();
