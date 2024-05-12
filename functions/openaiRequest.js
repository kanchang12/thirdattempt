// functions/openaiRequest.js
const fetch = require('node-fetch');

exports.handler = async function(event, context) {
    try {
        // Parse the request body
        const { user_input } = JSON.parse(event.body);

        // Call the OpenAI API to generate text
        const generatedText = await generateText(user_input);

        // Return a successful response
        return {
            statusCode: 200,
            body: JSON.stringify({ generated_text: generatedText })
        };
    } catch (error) {
        // Return an error response
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};

async function generateText(userInput) {
    const openaiEndpoint = 'https://api.openai.com/v1/engines/davinci/completions';
    const openaiApiKey = process.env.OPENAI_API_KEY; // Retrieve API key from environment variables

    const requestData = {
        prompt: userInput,
        max_tokens: 50
    };

    const response = await fetch(openaiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${openaiApiKey}`
        },
        body: JSON.stringify(requestData)
    });

    if (!response.ok) {
        throw new Error(`OpenAI request failed with status ${response.status}`);
    }

    const responseData = await response.json();
    const generatedText = responseData.choices[0].text.trim();

    return generatedText;
}
