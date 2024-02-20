document.addEventListener("DOMContentLoaded", function() {
    const token = localStorage.getItem('token');
    //Fetching role data
    if (token) {
      fetch('/auth', {
        method: 'GET',
        headers: {'Authorization': 'Bearer ' + token}
      }).then(response => response.json())
        .then(data => {
          console.log(data);
          document.getElementById('user-name').textContent = data.username;
          document.getElementById('user-role').textContent = data.role;
        });
    }
  });