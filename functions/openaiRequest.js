import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.apiKey, // Ensure OPENAI_API_KEY is set in Netlify environment variables
});

exports.handler = async function(event, context) {
  try {
    // Prepare the chat completion request payload
    const completion = await openai.chat.completions.create({
      messages: [{ role: "user", content: "Hi" }], // Hard-coded message "Hi"
      model: "gpt-3.5-turbo",
    });

    // Extract the generated text from the response
    const generatedText = completion.choices[0].message.content;

    return {
      statusCode: 200,
      body: JSON.stringify({ generated_text: generatedText }),
    };
  } catch (error) {
    console.error('Error in Netlify Function:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};
