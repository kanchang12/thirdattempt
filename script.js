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
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        if (data && data.generated_text) {
            document.getElementById('responseContainer').innerText = data.generated_text;
        } else {
            throw new Error('Invalid response format');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('responseContainer').innerText = 'Error processing input';
    }
});
