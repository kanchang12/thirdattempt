// script.js

document.getElementById('inputForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const userInput = document.getElementById('userInput').value;

    try {
        const response = await fetch('/.netlify/functions/openaiRequest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userInput })
            
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const data = await response.json();
        const generatedText = data.generated_text;

        // Update HTML element to display the generated text
        document.getElementById('responseContainer').innerText = generatedText;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('responseContainer').innerText = 'Error processing input';
    }
});
