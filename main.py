from ipaddress import ip_address
import cohere

import pyttsx3
import  speech_recognition as sr
import keyboard
import os
import subprocess as sp
import random
import requests
from PIL import Image
from io import BytesIO
#from handgesture import hand_gesture_control,stop_gesture_control


from datetime import datetime

from decouple import config
from random import choice
from conv import random_text
from online import find_my_ip,search_on_google,search_on_wikipedia,youtube
from weather import get_weather
import mydatabase
from base64 import b64decode

from mydatabase import save_command_to_db

COHERE_API_KEY = "Your-API-Key"
cohere_client = cohere.Client(COHERE_API_KEY)

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.0)  # Volume range: 0.0 to 1.0
engine.setProperty('rate', 175)    # Adjust speaking rate
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Use the first voice available

# User and Bot details from environment variables
USER = config('USER', default='User')
HOSTNAME = config('BOT', default='Assistant')

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def greet_me():
    """Greets the user based on the time of day."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good morning, {USER}!")
    elif 12 <= hour < 16:
        speak(f"Good afternoon, {USER}!")
    elif 16 <= hour < 19:
        speak(f"Good evening, {USER}!")
    speak(f"I am {HOSTNAME}. How may I assist you?{USER}")


listening=True
def start_listening():
    global listening
    listening=True
    print("started listening")

def pause_listening():
    global listening
    listening=False
    print("stopped listening")




keyboard.add_hotkey('ctrl+alt+k',start_listening)
keyboard.add_hotkey('ctrl+alt+p',pause_listening)


def take_command():
    """Listens to the user's voice and converts it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')  # Changed to recognize_google for simplicity
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError:
            speak("It seems there is an issue with the speech recognition service.")
            return None
        except Exception as e:
            speak("do you want to use another serice,sir?.")
            print(f"Error: {e}")
            return None





def generate_response(prompt):
    """Generates a response using Cohere AI."""
    try:
        response = cohere_client.generate(
            model="command-xlarge",  # Correct model name
            prompt=prompt,
            max_tokens=300,
            temperature=0.7,
            stop_sequences=["\n"]
        )
        if response and response.generations:
            return response.generations[0].text.strip()
        else:
            return "I'm sorry, I couldn't generate a response."
    except Exception as e:
        print(f"Error with Cohere API: {e}")
        return "Sorry, I encountered an error while generating a response."

def play_music():
    """Plays music from a predefined directory."""

    music_dir = "C:\\notjustmusic"

    try:
        songs = os.listdir(music_dir)  # List all files in the music directory
        if not songs:
            speak("Your music folder is empty. Please add some songs and try again.")
            return

        # Ask if the user wants a specific song or a random one
        speak("Do you want to play a specific song or a random one?")
        choice = take_command()
        if choice is None:
            speak("I didn't catch your choice. Playing a random song.")
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))
            speak(f"Playing {song} for you.")
            return

        if "specific" in choice:
            speak("Please tell me the name of the song.")
            song_name = take_command()
            if song_name:
                for song in songs:
                    if song_name.lower() in song.lower():
                        os.startfile(os.path.join(music_dir, song))
                        speak(f"Playing {song_name} for you.")
                        return
                speak(f"I couldn't find the song {song_name} in your music folder.")
            else:
                speak("Sorry, I didn't catch the name of the song. Playing a random song.")
                song = random.choice(songs)
                os.startfile(os.path.join(music_dir, song))
                speak(f"Playing {song} for you.")
        elif "random" in choice:
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))
            speak(f"Playing {song} for you.")
        else:
            speak("I didn't understand your choice. Playing a random song.")
            song = random.choice(songs)
            os.startfile(os.path.join(music_dir, song))

    except Exception as e:
        speak("An error occurred while trying to play music.")
        print(f"Error: {e}")


if __name__ == '__main__':
    greet_me()

    while True:
        if listening:
            query = take_command()
            if query:
                save_command_to_db(query)
                if "how are you" in query:
                    speak("I am absolutely fine, sir. What about you?")

                elif"who is your owner" in query:
                    speak("my owner is, rohan gaikwad")

                #elif "control mouse" in query:
                    #speak("Starting hand gesture control for the mouse.")
                    #hand_gesture_control()

                #elif "stop control" in query:
                    #speak("Stopping hand gesture control.")
                    #stop_gesture_control()


                elif"open command prompt" in query:
                    speak("opening command prompt")
                    os.system('start cmd')

                elif"open camera" in query:
                    speak("opening camera sir")
                    sp.run('start microsoft.windows.camera:',shell=True)

                elif"open notepad " in query:
                    speak("opening notepad for you sir")
                    notepad_path="C:\\Windows\\notepad.exe"
                    os.startfile(notepad_path)

                elif"ip address" in query:
                    ip_address=find_my_ip()
                    speak(f"your ip address is{ip_address}")
                    print(f"your ip address is{ip_address}")
                    
                elif"open youtube" in query:
                    speak("what do you want to play on youtube,sir?")
                    video=take_command().lower()
                    youtube(video)
                    
                    
                elif"open google" in query:
                    speak(f"what do you want yo search on google,{USER}")
                    query=take_command().lower()
                    search_on_google(query)
                    
                    
                elif"open wikipedia" in query:
                    speak("What do you want to search on Wikipedia, sir?")
                    search = take_command()
                    if search:  # Check if search is not None
                        search = search.lower()
                        results = search_on_wikipedia(search)
                        if results:
                            speak(f"According to Wikipedia, {results}")
                            speak("I am printing it on the terminal.")
                            print(results)
                        else:
                            speak("Sorry, I couldn't find anything on Wikipedia.")


                elif"play music" in query or"play song" in query:
                    play_music()


                elif "climate" in query:
                    speak("Please tell me the name of the city.")
                    city = take_command()
                    if city:
                        weather_report = get_weather(city)
                        speak(weather_report)
                        print(weather_report)
                    else:
                        speak("I didn't catch the city name. Please try again.")
                elif "stop" in query or "exit" in query:
                    hour = datetime.now().hour
                    if 21 <= hour or hour < 6:
                        speak("Good night, sir. Take care!")
                    else:
                        speak("Have a good day!")
                    break
                else:
                    speak("Let me think...")
                    response = generate_response(query)

                    if response:
                        # Split response into sentences by full stop
                        sentences = response.split(".")
                        for sentence in sentences:
                            sentence = sentence.strip()  # Remove any leading/trailing spaces
                            if sentence:  # Avoid empty lines
                                print(sentence)
                                speak(sentence)
                    else:
                        speak("Sorry, I couldn't generate a response.")
