import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize the speech recognition engine
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Load GPT2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Function to speak out the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("I am Jarvis. How can I assist you today?")

# Function to take voice commands
def take_command():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't understand. Can you repeat that?")
        return None

    return query

# Function to generate response using GPT model
def generate_response(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    response_ids = model.generate(input_ids, max_length=100, num_return_sequences=1, no_repeat_ngram_size=2)
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response

# Function to execute commands
def execute_command(query):
    if 'wikipedia' in query.lower():
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif 'open youtube' in query.lower():
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in query.lower():
        webbrowser.open("https://www.google.com")
    elif 'play music' in query.lower():
        music_dir = 'path to your music directory'
        songs = os.listdir(music_dir)
        random_song = os.path.join(music_dir, random.choice(songs))
        os.system(random_song)
    elif 'the time' in query.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {current_time}")
    elif 'exit' in query.lower():
        speak("Goodbye!")
        exit()
    else:
        response = generate_response(query)
        print("Jarvis:", response)
        speak(response)

# Main function
def main():
    greet()
    while True:
        query = take_command()
        if query:
            execute_command(query)

if __name__ == "__main__":
    main()
