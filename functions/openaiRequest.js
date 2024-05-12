const fetch = require('node-fetch');

async function generateTextWithMessages() {
    const openaiEndpoint = 'https://api.openai.com/v1/engines/gpt-3.5-turbo/completions';
    const openaiApiKey = process.env.OPENAI_API_KEY;

    const requestData = {
        model: "gpt-3.5-turbo",
        messages: [
            {
                role: "user",
                content: "Can you summarize the plot of the book?"
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

// Example usage:
generateTextWithMessages()
    .then(generatedText => {
        console.log("Generated Text:", generatedText);
    })
    .catch(error => {
        console.error("Error:", error);
    });
