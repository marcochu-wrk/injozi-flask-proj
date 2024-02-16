document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem('token');
    //Fetching role data
    if (token) {
      fetch('/auth', {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + token}
      }).then(response => response.json())
        .then(data => {
          document.getElementById('user-role').textContent = data.role;
        });
    }
  });