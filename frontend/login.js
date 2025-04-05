document.getElementById('login-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        username: document.getElementById('username').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            const data = await response.json();
            // Store user info in localStorage
            localStorage.setItem('userName', data.username || formData.username);
            
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        } else {
            const data = await response.json();
            alert(data.error || 'Login failed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    }
}); 