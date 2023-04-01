import speech_recognition as sr
import pyttsx3
import openai
import time
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()
# Set up the speech recognition engine
r = sr.Recognizer()

# Set up the text-to-speech engine
engine = pyttsx3.init()
app = Flask(__name__)
# Set up the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = "text-davinci-002"


# Define a function to generate a response
def generate_response(prompt):
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()


def main():
    # Start the voice input loop
    listen_duration = 6
    while True:
        # Use the microphone to listen for input
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.record(source, duration=listen_duration)

        try:
            # Use the speech recognition engine to transcribe the audio
            text = r.recognize_google(audio)
            print("You said: ", text)

            # Generate a response using the ChatGPT model
            response = generate_response(text)
            print("ChatGPT: ", response)

            # Use the text-to-speech engine to speak the response
            engine.say(response)
            engine.runAndWait()

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results: {0}".format(e))

        # Pause for a moment to avoid spamming the OpenAI API
        time.sleep(1)


if __name__ == "__main__":
    app.run(debug=True)
