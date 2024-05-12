// openaiRequest.js (Netlify Function)

const fetch = require('node-fetch');

exports.handler = async function(event, context) {
    try {
        const requestBody = JSON.parse(event.body);
        const userInput = requestBody.user_input;

        // Call OpenAI API to generate text based on user input
        const generatedText = await generateText(userInput);

        return {
            statusCode: 200,
            body: JSON.stringify({ generated_text: generatedText })
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};

async function generateText(userInput) {
    const openaiEndpoint = 'https://api.openai.com/v1/chat/completions';
    const openaiApiKey = process.env.OPENAI_API_KEY;

    const requestData = {
        model: "gpt-3.5-turbo",
        messages: [
            {
                role: "user",
                content: userInput
            }
        ],
        temperature: 1,
        max_tokens: 256,
        top_p: 1,
        frequency_penalty: 0,
        presence_penalty: 0
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
