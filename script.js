document.getElementById('inputForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    // Prepare the message to send to OpenAI (in this case, "Hi")
    const userInput = "Hi";
    console.log('User input:', userInput);

    try {
        const response = await fetch('/.netlify/functions/openaiRequest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
        });
        console.log('Fetch request sent');

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const data = await response.json();
        console.log('Response data:', data);

        const generatedText = data.generated_text;
        console.log('Generated text:', generatedText);

        // Update HTML element to display the generated text
        document.getElementById('responseContainer').innerText = generatedText;
        console.log('Response displayed on HTML page');
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('responseContainer').innerText = 'Error processing input';
    }
});
