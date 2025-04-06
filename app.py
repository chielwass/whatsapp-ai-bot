from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# Haal OpenAI API-sleutel op uit environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Je bent een AI-assistent gespecialiseerd in vastgoedbeheer. Antwoord professioneel, vriendelijk en kort."},
                    {"role": "user", "content": incoming_msg}
                ]
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = "Er is een fout opgetreden bij het verwerken van uw verzoek."

        msg.body(answer)
    else:
        msg.body('Ik heb geen bericht ontvangen. Kunt u uw vraag herhalen?')

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
