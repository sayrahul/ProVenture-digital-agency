/**
 * ProVenture Contact Form Handler
 * Works with both local backend and Vercel serverless functions
 */

(function () {
    'use strict';

    // Determine API endpoint based on environment
    const getApiEndpoint = () => {
        const hostname = window.location.hostname;

        // Local development
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:5000/submit';
        }

        // Vercel deployment (production or preview)
        return '/api/submit';
    };

    // Initialize contact form
    function initContactForm() {
        const form = document.querySelector('#ctl02');
        const submitBtn = document.querySelector('#submit-btn');

        if (!form) return;

        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Disable submit button
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.value = 'Sending...';
            }

            // Collect form data
            const formData = {
                name: document.querySelector('#name')?.value || '',
                email: document.querySelector('#email')?.value || '',
                company: document.querySelector('#company')?.value || '',
                phone: document.querySelector('#phone')?.value || '',
                message: document.querySelector('#message')?.value || '',
                interest: Array.from(document.querySelectorAll('input[name="interest"]:checked'))
                    .map(cb => cb.parentElement.textContent.trim())
            };

            try {
                const response = await fetch(getApiEndpoint(), {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (response.ok && result.ok) {
                    // Success
                    showMessage('success', result.message || 'Thank you! Your message has been sent successfully.');
                    form.reset();
                } else {
                    // Error from server
                    showMessage('error', result.error || 'Something went wrong. Please try again.');
                }
            } catch (error) {
                console.error('Form submission error:', error);
                showMessage('error', 'Network error. Please check your connection and try again.');
            } finally {
                // Re-enable submit button
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.value = 'Send Message';
                }
            }
        });
    }

    // Show message to user
    function showMessage(type, message) {
        // Remove existing messages
        const existingMsg = document.querySelector('.pv-form-message');
        if (existingMsg) {
            existingMsg.remove();
        }

        // Create message element
        const msgDiv = document.createElement('div');
        msgDiv.className = `pv-form-message pv-form-message-${type}`;
        msgDiv.textContent = message;
        msgDiv.style.cssText = `
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            animation: pvSlideIn 0.3s ease;
            ${type === 'success'
                ? 'background: #d4edda; color: #155724; border: 1px solid #c3e6cb;'
                : 'background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb;'}
        `;

        // Insert message
        const form = document.querySelector('#ctl02');
        if (form) {
            form.insertBefore(msgDiv, form.firstChild);

            // Scroll to message
            msgDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Auto-remove after 5 seconds
            setTimeout(() => {
                msgDiv.style.animation = 'pvSlideOut 0.3s ease';
                setTimeout(() => msgDiv.remove(), 300);
            }, 5000);
        }
    }

    // Add animation styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pvSlideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        @keyframes pvSlideOut {
            from {
                opacity: 1;
                transform: translateY(0);
            }
            to {
                opacity: 0;
                transform: translateY(-20px);
            }
        }
    `;
    document.head.appendChild(style);

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initContactForm);
    } else {
        initContactForm();
    }

})();
