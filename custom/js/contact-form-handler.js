document.addEventListener('DOMContentLoaded', function() {

    // 1. CONFIGURATION
    const scriptURL = 'https://script.google.com/macros/s/AKfycbxRyQD1d8n0TwhW8iXOTaO8qgh92ycyrcnWvCdqymt3YnHgzS6SlI8POyY9EY-eH7lM/exec';
    
    // REPLACE THIS with your actual Calendly or Google Calendar link
    const bookingURL = "https://calendly.com/"; 

    // 2. Select Elements
    const form = document.getElementById('ctl02'); 
    const submitButton = document.getElementById('submit-btn');

    if (submitButton) {
        // Create Status Message Element
        const statusMessage = document.createElement('div');
        statusMessage.style.textAlign = 'center';
        statusMessage.style.fontWeight = 'bold';
        statusMessage.style.marginTop = '15px';
        statusMessage.style.display = 'none';
        submitButton.parentNode.insertBefore(statusMessage, submitButton.nextSibling);

        // 3. Add Click Listener
        submitButton.addEventListener('click', e => {
            e.preventDefault(); // STOP page reload

            // Basic Validation
            const nameField = document.getElementById('name');
            const emailField = document.getElementById('email');
            const messageField = document.getElementById('message');

            // Empty Field Check
            if (!nameField.value || !emailField.value || !messageField.value) {
                alert("Please fill in Name, Email, and Message.");
                return;
            }

            // --- Character Limit Check ---
            const msgLength = messageField.value.length;
            if (msgLength < 5) {
                alert("Your message is too short. Please enter at least 5 characters.");
                return;
            }
            if (msgLength > 500) {
                alert(`Your message is too long (${msgLength} chars). Please shorten it to 500 characters.`);
                return;
            }
            // ----------------------------------

            // Show Loading State
            submitButton.disabled = true;
            submitButton.value = "Sending...";
            statusMessage.style.display = 'none';

            // Gather Data
            let requestBody = new FormData(form);

            // Send to Google Script
            fetch(scriptURL, { method: 'POST', body: requestBody })
                .then(response => {
                    // ------------------------------------------------
                    // SUCCESS: Show Beautiful Card with TWO Buttons
                    // ------------------------------------------------
                    
                    // 1. Hide the Submit Button
                    submitButton.style.display = 'none';

                    // 2. Inject CSS for "Pop-up" animation
                    const style = document.createElement('style');
                    style.innerHTML = `
                      @keyframes popIn {
                        0% { opacity: 0; transform: scale(0.95) translateY(10px); }
                        100% { opacity: 1; transform: scale(1) translateY(0); }
                      }
                    `;
                    document.head.appendChild(style);

                    // 3. Inject the Success HTML Card
                    statusMessage.innerHTML = `
                        <div style="
                            background: #ffffff;
                            border-radius: 12px;
                            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
                            padding: 30px 20px;
                            text-align: center;
                            width: 100%;
                            max-width: 420px;
                            margin: 0 auto;
                            box-sizing: border-box;
                            border-top: 5px solid #00ACDF;
                            animation: popIn 0.5s ease-out forwards;
                            font-family: 'Inter', sans-serif;
                        ">
                            <div style="
                                width: 60px;
                                height: 60px;
                                background: #e6fffa;
                                border-radius: 50%;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                margin: 0 auto 15px auto;
                            ">
                                <svg style="width: 30px; height: 30px; fill: #00b894;" viewBox="0 0 24 24">
                                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                                </svg>
                            </div>

                            <h3 style="color: #2d3436; margin: 0 0 10px 0; font-size: 20px; font-weight: 700;">Message Sent!</h3>

                            <p style="color: #636e72; font-size: 14px; line-height: 1.5; margin: 0 0 20px 0; word-wrap: break-word;">
                                Thanks, <strong>${nameField.value}</strong>.<br>
                                We have received your message.
                            </p>

                            <div style="height: 1px; background: #f1f2f6; margin: 15px 0;"></div>

                            <p style="color: #b2bec3; font-size: 12px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
                                Want to discuss now?
                            </p>
                            
                            <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center;">
                                
                                <a href="https://wa.me/919595997711?text=Hi%20ProVenture,%20I%20just%20filled%20your%20contact%20form." 
                                   target="_blank" 
                                   style="
                                       display: inline-flex; align-items: center; justify-content: center;
                                       background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                                       color: white; text-decoration: none; padding: 12px 20px;
                                       border-radius: 50px; font-weight: 600; font-size: 14px;
                                       box-shadow: 0 4px 12px rgba(37, 211, 102, 0.3);
                                       flex: 1 1 140px; /* Grows to fit, min width 140px */
                                       box-sizing: border-box;
                                   ">
                                    <svg style="width: 18px; height: 18px; margin-right: 6px; fill: white;" viewBox="0 0 24 24">
                                        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                                    </svg>
                                    WhatsApp
                                </a>

                                <a href="${bookingURL}" 
                                   target="_blank" 
                                   style="
                                       display: inline-flex; align-items: center; justify-content: center;
                                       background: white;
                                       color: #00ACDF; text-decoration: none; padding: 12px 20px;
                                       border: 2px solid #00ACDF;
                                       border-radius: 50px; font-weight: 600; font-size: 14px;
                                       box-shadow: 0 4px 12px rgba(0, 172, 223, 0.15);
                                       flex: 1 1 140px; /* Grows to fit, min width 140px */
                                       box-sizing: border-box;
                                   ">
                                    <svg style="width: 18px; height: 18px; margin-right: 6px; fill: #00ACDF;" viewBox="0 0 24 24">
                                        <path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zm0-12H5V6h14v2zm-7 5h5v5h-5z"/>
                                    </svg>
                                    Book Call
                                </a>
                            </div>

                        </div>
                    `;
                    
                    // 4. Reveal the message
                    statusMessage.style.display = 'block';

                    // 5. Clear form fields
                    form.reset();
                    document.querySelectorAll('input[name="interest"]').forEach(cb => cb.checked = false);
                })
                .catch(error => {
                    // Error Handling
                    statusMessage.innerText = "Error! Something went wrong. Please try again.";
                    statusMessage.style.color = "#dc3545"; 
                    statusMessage.style.display = 'block';
                    submitButton.disabled = false;
                    submitButton.value = "Send Message";
                    console.error('Error!', error.message);
                });
        });
    }
});