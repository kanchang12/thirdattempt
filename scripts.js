function submitForm() {
    // Get user input
    var userInput = document.getElementById('user_input').value;

    // Prepare the request payload
    var formData = new FormData();
    formData.append('user_input', userInput);

    // Send POST request to Flask backend
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/submit', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                document.getElementById('responseContainer').innerHTML = '<p>' + response.response + '</p>';
            } else {
                console.error('Error:', xhr.statusText);
                document.getElementById('responseContainer').innerHTML = '<p>Error: ' + xhr.statusText + '</p>';
            }
        }
    };

    xhr.send(formData);
}
