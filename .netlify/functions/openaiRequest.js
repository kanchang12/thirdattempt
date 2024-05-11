// functions/openaiRequest.js

const fetch = require('node-fetch');
const apiKey = process.env.OPENAI_API_KEY;

exports.handler = async (event) => {
    const userInput = JSON.parse(event.body).user_input;

    try {
        const response = await fetch('https://api.openai.com/v1/engines/davinci/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                prompt: userInput,
                max_tokens: 50
            })
        });

        const data = await response.json();
        return {
            statusCode: 200,
            body: JSON.stringify({ generated_text: data.choices[0].text.trim() })
        };
    } catch (error) {
        console.error('Error fetching data:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Internal server error' })
        };
    }
};
