import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import random

# Initialize the speech recognition engine
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

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
        speak("A very good afternoon!")
    else:
        speak("A very good evening!")

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
        # Handle custom commands here
        speak("Sorry, I don't understand that command. Would you like me to search the web for you?")
        response = take_command()
        if response:
            webbrowser.open(f"https://www.google.com/search?q={response}")

# Main function
def main():
    greet()
    while True:
        query = take_command()
        if query:
            execute_command(query)

if __name__ == "__main__":
    main()
