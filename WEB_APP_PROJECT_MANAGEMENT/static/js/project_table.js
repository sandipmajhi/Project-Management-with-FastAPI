const IP = '127.0.0.1:8000'
$(document).ready(function () {

    $('.datepicker').datepicker({
        format: 'dd-mm-yyyy',
        autoclose: true,
        todayHighlight: true
    });


    // Initialize DataTable

    var table = $('#project_table').DataTable({
        "ajax": {
            "url": `http://${IP}/viewprojectlist`, // Replace with your API endpoint
            "dataSrc": "",
            "headers": {
                "Authorization": "Bearer " + accessToken // Set the Authorization header with the token
            },
            "error": function (xhr, error, code) {
                // Token expired
                alert(`Your session has expired. Please log in again.${xhr.responseText}`);
                // Redirect to login or show login option
                window.location.href = loginUrl; // Or update the UI to show login option

            }
        },
        "scrollX": true,
        "columns": [

            { "data": "project_name" }, // Adjusted according to your API response
            { "data": "project_code" }, // Adjusted according to your API response
            { "data": "project_start_date" }, // Adjusted according to your API response
            { "data": "project_end_date" } // Adjusted according to your API response
        ],
        "order": [[0, "asc"]],
        "pageLength": 10, // Maximum rows per page
        "lengthMenu": [
            [10, 20, 50, 100, -1], // values for pagination
            [10, 20, 50, 100, "All"] // corresponding display texts
        ],
        "pagingType": "full_numbers", // Simple pagination with next/prev buttons
        "language": {

            "lengthMenu": "Display _MENU_ entries",

            "paginate": {
                "previous": "Previous",
                "next": "Next"
            }
        }
    });

    // Search button functionality
    $('#search-button').on('click', function () {
        var searchTerm = $('#search-input').val();
        table.search(searchTerm).draw();
    });

    // Optional: You can also listen for input change for real-time search
    $('#search-input').on('keyup', function () {
        var searchTerm = $('#search-input').val();
        table.search(searchTerm).draw();
    });




    document.getElementById('download-excel').addEventListener('click', function () {
        // Convert table to a worksheet
        const table = document.getElementById('project_table');
        const workbook = XLSX.utils.table_to_book(table, { sheet: "Sheet1" });

        // Generate a binary string representation of the workbook
        XLSX.writeFile(workbook, 'Project_Details.xlsx');
    });




});