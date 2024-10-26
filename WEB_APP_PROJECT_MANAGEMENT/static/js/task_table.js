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
            "url": `http://${IP}/show_task_admin`, // Your API endpoint
            "dataSrc": "",
            "headers": {
                "Authorization": "Bearer " + accessToken // Set the Authorization header with the token
            },
            "error": function (xhr, error, code) {
                // Token expired
                alert("Your session has expired. Please log in again.");
                // Redirect to login or show login option
                window.location.href = loginUrl; // Or update the UI to show login option

            }
        },
        "scrollX": true,
        "columns": [
            // { "data": "project" },                  // Project ID
            { "data": "task_name" },                // Task Name
            { "data": "task_description" },                // Task Name
            { "data": "project_name" },              // Project Name
            { "data": "task_owner_name" },          // Task Owner Name
            {
                "data": "assigned",                  // Assigned Users
                "render": function (data) {
                    return data.join(", ");         // Join array into a comma-separated string
                }
            },
            { "data": "dependency" },
            { "data": "start_date_and_time" },      // Start Date & Time
            { "data": "target_end_date_and_time" }, // Target End Date & Time
            { "data": "target_duration" },
            { "data": "actual_end_date_and_time" },
            { "data": "actual_duration" },
            { "data": "status" },                     // Status
            { "data": "remarks" },                     // Status
            { "data": "created_at" },
            {
                "data": "id",  // No specific data field, used for the Edit column
                "render": function (item) {
                    return `<a href="${taskEditPageUrl}/?id=${item}" class="btn btn-warning btn-sm">Edit</a>`;
                },
                "orderable": false  // Disable ordering for the Edit column, if needed
            }
        ],
        "order": [[6, "desc"]],
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
        },
        "columnDefs": [
            { "visible": false, "targets": [13] } // Assuming the last column index is 13
        ]
    });

    $('#search-button').on('click', function () {
        var searchTerm = $('#search-input').val();

        // Update the DataTable to fetch data based on the search term
        $.ajax({
            url: `http://${IP}/tasks_by_date`,
            method: "POST", // Use POST method
            contentType: "application/json", // Specify content type as JSON
            data: JSON.stringify({ date: searchTerm }), // Send the date in JSON format
            headers: {
                "Authorization": "Bearer " + accessToken // Include the access token
            },
            success: function (data) {
                table.clear().rows.add(data).draw(); // Clear and add new data to the table
            },
            error: function (xhr, status, error) {
                console.error("Error fetching data:", error);
            }
        });
    });

    document.getElementById('download-excel').addEventListener('click', function () {
        // Convert table to a worksheet
        const table = document.getElementById('project_table');
        const workbook = XLSX.utils.table_to_book(table, { sheet: "Sheet1" });

        // Generate a binary string representation of the workbook
        XLSX.writeFile(workbook, 'Task_Details.xlsx');
    });



});


