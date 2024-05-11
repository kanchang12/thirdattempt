// functions/openaiRequest.js
const axios = require('axios');

exports.handler = async function(event, context) {
    try {
        const { user_input } = JSON.parse(event.body);

        // Retrieve OpenAI API key from environment variable
        const openaiApiKey = process.env.apiKey;

        // Example: Make request to OpenAI API
        const response = await axios.post('https://api.openai.com/v1/engines/davinci/completions', {
            prompt: user_input,
            max_tokens: 50
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${openaiApiKey}`
            }
        });

        // Extract generated text from OpenAI response
        const generated_text = response.data.choices[0].text.trim();

        // Return response to frontend
        return {
            statusCode: 200,
            body: JSON.stringify({ generated_text })
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
