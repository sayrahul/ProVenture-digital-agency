document.addEventListener('DOMContentLoaded', function() {
    
    // 1. CONFIGURATION - PASTE YOUR NEW WEB APP URL HERE
    // FIXED: Added the missing closing quote at the end of the URL
    const scriptURL = 'https://script.google.com/macros/s/AKfycbxRyQD1d8n0TwhW8iXOTaO8qgh92ycyrcnWvCdqymt3YnHgzS6SlI8POyY9EY-eH7lM/exec'; 

    const form = document.getElementById('ctl02'); // Matches your ASP.NET Form ID
    const submitButton = document.getElementById('submit-btn');

    if(submitButton){
        // Create Status Message Element
        const statusMessage = document.createElement('div');
        statusMessage.style.textAlign = 'center';
        statusMessage.style.fontWeight = 'bold';
        statusMessage.style.marginTop = '15px';
        statusMessage.style.display = 'none';
        submitButton.parentNode.insertBefore(statusMessage, submitButton.nextSibling);

        submitButton.addEventListener('click', e => {
            e.preventDefault(); // STOP page reload

            // Basic Validation
            const nameField = document.getElementById('name');
            const emailField = document.getElementById('email');
            const messageField = document.getElementById('message');

            if (!nameField.value || !emailField.value || !messageField.value) {
                alert("Please fill in Name, Email, and Message.");
                return;
            }

            // Show Loading
            submitButton.disabled = true;
            submitButton.value = "Sending...";
            statusMessage.style.display = 'none';

            // Gather Data
            let requestBody = new FormData(form);

            // Send to Google Script
            fetch(scriptURL, { method: 'POST', body: requestBody})
.then(response => {
    // 1. Hide the Submit Button so they don't click it twice
    submitButton.style.display = 'none';

    // 2. Inject CSS for a smooth "Pop-up" animation
    const style = document.createElement('style');
    style.innerHTML = `
      @keyframes popIn {
        0% { opacity: 0; transform: scale(0.9) translateY(10px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
      }
    `;
    document.head.appendChild(style);

    // 3. Show the Beautiful Success Card
    statusMessage.innerHTML = `
        <div style="
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            padding: 40px 30px;
            text-align: center;
            max-width: 420px;
            margin: 20px auto;
            border-top: 5px solid #00ACDF; /* ProVenture Brand Blue */
            animation: popIn 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            font-family: 'Inter', sans-serif;
        ">
            <div style="
                width: 65px;
                height: 65px;
                background: #e6fffa;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 20px auto;
            ">
                <svg style="width: 32px; height: 32px; fill: #00b894;" viewBox="0 0 24 24">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                </svg>
            </div>

            <h3 style="
                color: #2d3436; 
                margin: 0 0 10px 0; 
                font-size: 22px; 
                font-weight: 700;
            ">Message Sent Successfully!</h3>

            <p style="
                color: #636e72; 
                font-size: 15px; 
                line-height: 1.6; 
                margin: 0 0 25px 0;
            ">
                Thanks for reaching out, <strong>${nameField.value}</strong>.<br>
                We have sent a confirmation email to <br>
                <span style="color: #00ACDF;">${emailField.value}</span>.
            </p>

            <div style="height: 1px; background: #f1f2f6; margin: 20px 0;"></div>

            <p style="color: #b2bec3; font-size: 13px; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;">
                Want a faster response?
            </p>
            
            <a href="https://wa.me/919595997711?text=Hi%20ProVenture,%20I%20just%20filled%20your%20contact%20form%20and%20would%20like%20to%20discuss%20my%20project." 
               target="_blank" 
               style="
                   display: inline-flex; 
                   align-items: center; 
                   justify-content: center; 
                   background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); 
                   color: white; 
                   text-decoration: none; 
                   padding: 14px 28px; 
                   border-radius: 50px; 
                   font-weight: 600; 
                   font-size: 16px;
                   box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
                   transition: transform 0.2s;
               "
               onmouseover="this.style.transform='translateY(-2px)'" 
               onmouseout="this.style.transform='translateY(0)'"
            >
                <svg style="width: 20px; height: 20px; margin-right: 10px; fill: white;" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                </svg>
                Chat on WhatsApp
            </a>
        </div>
    `;
    
    // 4. Reveal the message
    statusMessage.style.display = 'block';

    // 5. Clear form fields
    form.reset();
    document.querySelectorAll('input[name="interest"]').forEach(cb => cb.checked = false);
})
                .catch(error => {
                    // Error Message
                    statusMessage.innerText = "Error! Something went wrong. Please try again.";
                    statusMessage.style.color = "#dc3545"; // Red
                    statusMessage.style.display = 'block';
                    submitButton.disabled = false;
                    submitButton.value = "Send Message";
                    console.error('Error!', error.message);
                });
        });
    }
});