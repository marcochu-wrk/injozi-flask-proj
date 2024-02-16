document.getElementById('logoutButton').addEventListener('click', function() {
    //removing token from local storage
    localStorage.removeItem('token'); 
    window.location.href = '/logout'; 
});