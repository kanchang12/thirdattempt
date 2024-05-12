// openaiRequest.js (Netlify Function)

const fetch = require('node-fetch');

exports.handler = async function(event, context) {
    try {
        const requestBody = JSON.parse(event.body);
        const userInput = requestBody.user_input;
        console.log('Received user input:', userInput);

        // Call OpenAI API to generate text based on user input
        const generatedText = await generateText(userInput);
        console.log('Generated text from OpenAI:', generatedText);

        return {
            statusCode: 200,
            body: JSON.stringify({ generated_text: generatedText })
        };
    } catch (error) {
        console.error('Error in Netlify Function:', error);
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
    console.log('Request data for OpenAI:', requestData);

    const response = await fetch(openaiEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${openaiApiKey}`
        },
        body: JSON.stringify(requestData)
    });
    console.log('OpenAI API request sent');

    if (!response.ok) {
        throw new Error(`OpenAI request failed with status ${response.status}`);
    }

    const responseData = await response.json();
    console.log('Response data from OpenAI:', responseData);

    const generatedText = responseData.choices[0].text.trim();
    console.log('Generated text:', generatedText);

    return generatedText;
}
