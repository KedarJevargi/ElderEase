document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signup-form');
    const addGuardianBtn = document.getElementById('add-guardian');
    const addContactBtn = document.getElementById('add-contact');
    const guardiansContainer = document.getElementById('guardians-container');
    const contactsContainer = document.getElementById('contacts-container');

    // Add Guardian
    addGuardianBtn.addEventListener('click', () => {
        const guardianEntry = document.createElement('div');
        guardianEntry.className = 'guardian-entry mb-3';
        guardianEntry.innerHTML = `
            <div class="row">
                <div class="col-md-4">
                    <input type="text" class="form-control" placeholder="Name" required>
                </div>
                <div class="col-md-4">
                    <input type="text" class="form-control" placeholder="Relation" required>
                </div>
                <div class="col-md-4">
                    <input type="tel" class="form-control" placeholder="Phone Number" required>
                </div>
            </div>
        `;
        guardiansContainer.appendChild(guardianEntry);
    });

    // Add Contact
    addContactBtn.addEventListener('click', () => {
        const contactEntry = document.createElement('div');
        contactEntry.className = 'contact-entry mb-3';
        contactEntry.innerHTML = `
            <div class="row">
                <div class="col-md-4">
                    <input type="text" class="form-control" placeholder="Name" required>
                </div>
                <div class="col-md-4">
                    <input type="tel" class="form-control" placeholder="Phone Number" required>
                </div>
                <div class="col-md-4">
                    <input type="file" class="form-control" accept="image/*">
                </div>
            </div>
        `;
        contactsContainer.appendChild(contactEntry);
    });

    // Form Submission
    signupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        console.log('Form submitted'); // Debug log
        
        // Collect form data
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            age: document.getElementById('age').value,
            dob: document.getElementById('dob').value,
            password: document.getElementById('password').value,
            address: document.getElementById('address').value,
            doctor_name: document.getElementById('doctor-name').value,
            doctor_phone: document.getElementById('doctor-phone').value,
            medications: document.getElementById('medications').value
        };

        console.log('Form data:', formData); // Debug log

        try {
            const response = await fetch('/api/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            console.log('Response status:', response.status); // Debug log
            const data = await response.json();
            console.log('Response data:', data); // Debug log

            if (response.ok) {
                console.log('Signup successful, redirecting...'); // Debug log
                // Store user info in localStorage
                localStorage.setItem('userName', formData.name);
                
                // Redirect to dashboard using the correct route
                window.location.href = '/dashboard';
            } else {
                console.error('Signup failed:', data); // Debug log
                alert(data.error || 'Signup failed. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    });

    // Form validation
    signupForm.addEventListener('input', (e) => {
        const input = e.target;
        if (input.required && !input.value) {
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });
}); 