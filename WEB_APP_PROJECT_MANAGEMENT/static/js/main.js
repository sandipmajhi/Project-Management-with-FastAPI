// Toggle Sidebar

document.querySelector('.toggle-button').addEventListener('click', function () {
    document.querySelector('.sidebar').classList.toggle('collapsed');
    document.querySelector('.content').classList.toggle('collapsed');
});

$(document).ready(function () {
    // Your custom scripts can go here
    $('#logout').on('click', function (event) {
        event.preventDefault();


        if (confirm("Are you sure you want to log out?")) {
            $.ajax({
                url: logoutUrl, // Replace with your actual logout endpoint
                type: "GET",
                headers: {
                    "Authorization": "Bearer " + accessToken // If required, include the authorization token
                },
                success: function (response) {
                    // Handle successful logout
                    alert("Logged out successfully!");
                    // Optionally redirect to login page or homepage
                    window.location.href = loginUrl;

                },
                error: function (xhr, status, error) {
                    // Handle errors
                    window.location.href = loginUrl;
                }
            });
        }

    })

});