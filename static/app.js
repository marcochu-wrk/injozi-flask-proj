document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: new URLSearchParams({'username': username, 'password': password})
    }).then(response => response.json())
      .then(data => {
        if(data.token) {
          localStorage.setItem('token', data.token); // Store token
          window.location.href = '/'; // Redirect to home page
        } else {
          alert('Login failed'); // Basic error handling
        }
      });
});