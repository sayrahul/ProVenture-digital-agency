/**
 * Contact Form Validation
 * Real-time validation with helpful error messages
 */

(function () {
    'use strict';

    // Validation rules
    const validationRules = {
        name: {
            required: true,
            minLength: 2,
            pattern: /^[a-zA-Z\s]+$/,
            errorMessages: {
                required: 'Please enter your name',
                minLength: 'Name must be at least 2 characters',
                pattern: 'Please enter a valid name (letters only)'
            }
        },
        email: {
            required: true,
            pattern: /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/,
            errorMessages: {
                required: 'Please enter your email address',
                pattern: 'Please enter a valid email address'
            }
        },
        company: {
            required: true,
            minLength: 2,
            errorMessages: {
                required: 'Please enter your company name',
                minLength: 'Company name must be at least 2 characters'
            }
        },
        phone: {
            required: false,
            pattern: /^\+\d{1,4}[\d\s\-]{7,15}$/,
            errorMessages: {
                pattern: 'Please enter a valid phone number (e.g., +91 9876543210)'
            }
        },
        message: {
            required: true,
            minLength: 10,
            errorMessages: {
                required: 'Please enter your message',
                minLength: 'Message must be at least 10 characters'
            }
        }
    };

    // Validate single field
    function validateField(field) {
        const fieldName = field.name;
        const value = field.value.trim();
        const rules = validationRules[fieldName];

        if (!rules) return true;

        // Check required
        if (rules.required && !value) {
            showError(field, rules.errorMessages.required);
            return false;
        }

        // Check min length
        if (rules.minLength && value && value.length < rules.minLength) {
            showError(field, rules.errorMessages.minLength);
            return false;
        }

        // Check pattern
        if (rules.pattern && value && !rules.pattern.test(value)) {
            showError(field, rules.errorMessages.pattern);
            return false;
        }

        // Valid
        showSuccess(field);
        return true;
    }

    // Show error message
    function showError(field, message) {
        const formGroup = field.closest('.form-group');
        if (!formGroup) return;

        // Remove existing error
        const existingError = formGroup.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Add error class
        formGroup.classList.add('has-error');
        formGroup.classList.remove('has-success');
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');

        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        errorDiv.style.color = '#dc3545';
        errorDiv.style.fontSize = '14px';
        errorDiv.style.marginTop = '5px';
        errorDiv.style.animation = 'slideDown 0.3s ease';

        formGroup.appendChild(errorDiv);
    }

    // Show success state
    function showSuccess(field) {
        const formGroup = field.closest('.form-group');
        if (!formGroup) return;

        // Remove error
        const existingError = formGroup.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Add success class
        formGroup.classList.remove('has-error');
        formGroup.classList.add('has-success');
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    }

    // Validate entire form
    function validateForm(form) {
        let isValid = true;
        const fields = form.querySelectorAll('input[name], textarea[name]');

        fields.forEach(field => {
            if (!validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    // Show success modal
    function showSuccessModal() {
        const modal = document.createElement('div');
        modal.className = 'success-modal';
        modal.innerHTML = `
            <div class="success-modal-content">
                <div class="success-icon">
                    <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#00ACDF" stroke-width="2">
                        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                        <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                </div>
                <h3>Thank You!</h3>
                <p>Your message has been sent successfully. We'll get back to you within 24 hours.</p>
                <button class="btn btn-primary pv-btn-primary" onclick="this.closest('.success-modal').remove()">Close</button>
            </div>
        `;

        // Add styles
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: fadeIn 0.3s ease;
        `;

        const content = modal.querySelector('.success-modal-content');
        content.style.cssText = `
            background: white;
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            max-width: 500px;
            animation: slideUp 0.4s ease;
        `;

        document.body.appendChild(modal);

        // Track conversion
        if (typeof gtag !== 'undefined') {
            gtag('event', 'form_submission', {
                'event_category': 'Contact',
                'event_label': 'Contact Form',
                'value': 1
            });
        }
    }

    // Initialize
    function init() {
        const form = document.querySelector('form#ctl02');
        if (!form) return;

        // Add real-time validation
        const fields = form.querySelectorAll('input[name], textarea[name]');
        fields.forEach(field => {
            // Validate on blur
            field.addEventListener('blur', function () {
                if (this.value.trim()) {
                    validateField(this);
                }
            });

            // Clear error on focus
            field.addEventListener('focus', function () {
                const formGroup = this.closest('.form-group');
                if (formGroup) {
                    const error = formGroup.querySelector('.error-message');
                    if (error) {
                        error.style.opacity = '0.5';
                    }
                }
            });

            // Validate on input (debounced)
            let timeout;
            field.addEventListener('input', function () {
                clearTimeout(timeout);
                timeout = setTimeout(() => {
                    if (this.value.trim()) {
                        validateField(this);
                    }
                }, 500);
            });
        });

        // Handle form submission
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            if (validateForm(this)) {
                // Disable submit button
                const submitBtn = this.querySelector('input[type="submit"]');
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.value = 'Sending...';
                }

                // Save to localStorage (since no backend)
                const formData = {
                    name: this.querySelector('[name="name"]').value,
                    email: this.querySelector('[name="email"]').value,
                    company: this.querySelector('[name="company"]').value,
                    phone: this.querySelector('[name="phone"]')?.value || '',
                    message: this.querySelector('[name="message"]').value,
                    interests: Array.from(this.querySelectorAll('[name="interest"]:checked')).map(cb => cb.value),
                    timestamp: new Date().toISOString()
                };

                // Get existing submissions
                let submissions = [];
                try {
                    submissions = JSON.parse(localStorage.getItem('contactSubmissions') || '[]');
                } catch (e) {
                    submissions = [];
                }

                // Add new submission
                submissions.push(formData);
                localStorage.setItem('contactSubmissions', JSON.stringify(submissions));

                // Also save to submissions.json via simple write
                // Note: This requires server-side handling in production

                // Show success
                setTimeout(() => {
                    showSuccessModal();
                    this.reset();

                    // Re-enable button
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.value = 'Send Message';
                    }
                }, 1000);
            } else {
                // Scroll to first error
                const firstError = this.querySelector('.has-error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    }

    // Start when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .form-control.is-invalid {
            border-color: #dc3545;
            box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
        }
        
        .form-control.is-valid {
            border-color: #28a745;
            box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
        }
        
        .success-icon {
            margin-bottom: 20px;
            animation: scaleIn 0.5s ease;
        }
        
        @keyframes scaleIn {
            from {
                transform: scale(0);
            }
            to {
                transform: scale(1);
            }
        }
    `;
    document.head.appendChild(style);
})();
