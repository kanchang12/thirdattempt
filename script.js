// Function to authenticate and access the API
async function authenticateAndAccessAPI() {
    const clientId = '291513496305-iub079ja2sb58h551dmj66cq51ccggvp.apps.googleusercontent.com.apps.googleusercontent.com';
    const apiEndpoint = 'https://europe-west2-aiplatform.googleapis.com/v1/projects/algebraic-ward-422922-e3/locations/europe-west2/publishers/google/models/gemini-1.0-pro:streamGenerateContent';

    try {
        // Initialize Google Auth2 client
        await gapi.auth2.init({ client_id: clientId });

        // Sign in the user
        const user = await gapi.auth2.getAuthInstance().signIn();

        // Obtain the access token
        const accessToken = user.getAuthResponse().access_token;

        // Construct the request data
        const requestData = {
            "contents": {
                "role": "user",
                "parts": {
                    "text": "Give me a recipe for banana bread."
                }
            },
            "safety_settings": {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            "generation_config": {
                "temperature": 0.2,
                "topP": 0.8,
                "topK": 40
            }
        };

        // Make the API request with the access token in the Authorization header
        const response = await fetch(apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(requestData)
        });

        // Handle response
        if (response.ok) {
            const responseData = await response.json();
            const responseContainer = document.getElementById('responseContainer');
            responseContainer.innerText = JSON.stringify(responseData);
        } else {
            throw new Error(`Request failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Authentication and API request error:', error);
        const responseContainer = document.getElementById('responseContainer');
        responseContainer.innerText = `Error: ${error.message}`;
    }
}
