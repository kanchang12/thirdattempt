function sendInput() {
    var userInput = document.getElementById("userInput").value;

    // Create a new XMLHttpRequest object
    var xhr = new XMLHttpRequest();

    // Configure it: GET-request for the URL
    xhr.open('POST', '/submit', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Send the request over to Flask
    xhr.send(JSON.stringify({ input: userInput }));

    xhr.onload = function () {
        if (xhr.status === 200) {
            console.log('Request was successful');
        } else {
            console.log('Request failed');
        }
    };
}
