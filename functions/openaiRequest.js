// functions/openaiRequest.js

exports.handler = async function(event, context) {
    try {
        const { user_input } = JSON.parse(event.body);
        // Process user_input (example: echo back the input)
        const response = { generated_text: `You entered: ${user_input}` };
        return {
            statusCode: 200,
            body: JSON.stringify(response)
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
