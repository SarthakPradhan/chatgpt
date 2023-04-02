import speech_recognition as sr
import pyttsx3
import openai
import io
import base64
import time
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

# Set up the speech recognition engine
r = sr.Recognizer()

# Set up the text-to-speech engine
engine = pyttsx3.init()

# Set up the OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = "text-davinci-002"

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speech_function', methods=['POST'])
def speech_function():
    # Start the voice input loop
    listen_duration = 6

    # Use the microphone to listen for input
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.record(source, duration=listen_duration)

    try:
        # Use the speech recognition engine to transcribe the audio
        transcription = r.recognize_google(audio)
        print("You said: ", transcription)

        # Generate a response using the ChatGPT model
        response = generate_response(transcription)
        print("ChatGPT: ", response)

        # Use the transcription-to-speech engine to speak the response
        # engine.say(response)
        # engine.runAndWait()

    except sr.UnknownValueError:
        response = "Could not understand audio"
        print("Could not understand audio")

    except sr.RequestError as e:
        response = "Could not request results: {0}".format(e)
        print("Could not request results: {0}".format(e))

    engine.save_to_file(response, 'output.mp3')
    engine.runAndWait()
    with io.open('output.mp3', 'rb') as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode('ascii')

    return {'text': response, 'audio': audio_base64}

@app.route('/text_function', methods=['POST'])
def text_function():
    # Get the input text from the form
    input_text = request.form.get('input_text')
    print("You typed: ", input_text)

    # Generate a response using the ChatGPT model
    response = generate_response(input_text)
    print("ChatGPT: ", response)

    return {'text': response}

if __name__ == "__main__":
    app.run(debug=True)
