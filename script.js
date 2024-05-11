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

        if (response.ok) {
            const data = await response.json();
            const responseContainer = document.getElementById('responseContainer');
            responseContainer.innerText = data.generated_text || 'Error processing input';
        } else {
            throw new Error(`Request failed with status: ${response.status}`);
        }
    } catch (error) {
        console.error('Error:', error);
        const responseContainer = document.getElementById('responseContainer');
        responseContainer.innerText = 'Error processing input';
    }
});
