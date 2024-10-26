const IP = '127.0.0.1:8000'

const assigned = document.getElementById('assigned');
document.addEventListener('DOMContentLoaded', async () => {
    const selectElement = document.getElementById('project');
    const task_owner = document.getElementById('task_owner');

    // const btn = document.getElementById('submit');


    try {

        const project_response = await fetch(`http://${IP}/viewprojectlist`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!project_response.ok) {
            if (project_response.status == 403) {
                alert('Your session has expired please Login again');
                window.location.href = 'login'
            } else {
                alert(`${project_response.sta}`)
            }
        }

        const owner_response = await fetch(`http://${IP}/get_all_users`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!owner_response.ok) {
            throw new Error('Network response was not ok');
        }

        const assigned_response = await fetch(`http://${IP}/get_all_users`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        if (!assigned_response.ok) {
            throw new Error('Network response was not ok');
        }

        const data1 = await project_response.json();
        let projectIds = [];
        // Populate the select dropdown with the received project data
        data1.forEach(item => {
            const option = document.createElement('option');
            option.value = item.project_id;
            projectIds.push(item.project_id)
            option.textContent = item.project_name;  // Display the project name
            selectElement.appendChild(option);
        });

        const data2 = await owner_response.json();
        let ownerIds = [];

        data2.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            ownerIds.push(item.id)
            option.textContent = item.name;
            task_owner.appendChild(option);
        });

        const data3 = await assigned_response.json();
        let userIds = [];

        data3.forEach(item => {
            const option = document.createElement('option');
            option.value = item.id;
            userIds.push(item.id)
            option.textContent = item.name;
            assigned.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }




});
let userElement = document.getElementById("assigned-names")




$(document).ready(function () {

    // Your existing data-fetching code...

    // Initialize Select2
    $('select').select2({
        placeholder: "Select an option",
        allowClear: true,
        width: '100%'
    });

    // $('#assigned').select2({
    //     placeholder: "Select an option",
    //     allowClear: true
    // });



    $('#task-form').on('submit', function (e) {
        e.preventDefault();

        if (this.checkValidity()) {
            const selectedProjectId = $('#project').val();
            const task_name = document.getElementById('task_name').value;
            const task_description = document.getElementById('task_description').value;

            // Get the datetime-local values
            const start_date_and_time = document.getElementById('start_date_and_time').value;
            const target_end_date_and_time = document.getElementById('target_end_date_and_time').value;

            // Function to convert date format
            function formatDate(dateString) {
                const date = new Date(dateString);
                const day = String(date.getDate()).padStart(2, '0');
                const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
                const year = date.getFullYear();
                const hours = String(date.getHours()).padStart(2, '0');
                const minutes = String(date.getMinutes()).padStart(2, '0');

                return `${day}-${month}-${year} ${hours}:${minutes}`;
            }

            // Reformatting the date fields
            const formatted_start_date = formatDate(start_date_and_time);
            const formatted_target_end_date = formatDate(target_end_date_and_time);

            const dependency = document.getElementById('dependency').value;
            const task_owner = $('#task_owner').val();
            const assigned = $('#assigned').val();
            const target_duration = document.getElementById('target_duration').value;
            const status = $('#status').val();

            // Create data object
            const data = {
                project: selectedProjectId,
                task_name,
                task_description,
                start_date_and_time: formatted_start_date,
                target_end_date_and_time: formatted_target_end_date,
                dependency,
                task_owner,
                assigned,
                target_duration,
                status
            };

            $.ajax({
                type: 'POST',
                url: taskCreateUrl,
                data: JSON.stringify(data),
                contentType: 'application/json',
                dataType: 'json',
                headers: { 'Authorization': "Bearer " + accessToken },
                success: function (response) {
                    console.log('Success:', response);
                    alert("Task Created Successfully");
                    window.location.href = "task_create";
                },
                error: function (xhr) {
                    console.error('Error:', xhr.status);
                }
            });
        } else {


            this.reportValidity();

        }

    });
});




