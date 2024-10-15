document.getElementById('loginBtn').addEventListener('click', function() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Checking the email and password
    if (email === 'testing@gmail.com' && password === '2024') {
        alert('Login successful! Redirecting...');
        // Redirect to the dashboard or another page if needed
        window.location.href = 'http://127.0.0.1:5000';
    } else {
        alert('Invalid email or password. Please try again.');
    }
});
