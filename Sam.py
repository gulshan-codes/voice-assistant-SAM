import speech_recognition as sr
import webbrowser
import pyttsx3
import musicliberary
import requests
import os
from gtts import gTTS
import pygame
from openai import OpenAI

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "<Your Key Here>"


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    client = OpenAI(
    api_key="<Your Key Here>"
)  # Pass key explicitly

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Sam skilled in general tasks like Alexa and Google Cloud."},
            {"role": "user", "content": "What is coding?"}
        ]
    )

    print(completion.choices[0].message["content"])

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    os.remove('temp.mp3')




def processCommand(c):
    if "open google" in c.lower():
        webbrowser.get("/usr/bin/brave-browser %s").open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.get("/usr/bin/brave-browser %s").open("https://youtube.com")    
    elif "open facebook" in c.lower():
        webbrowser.get("/usr/bin/brave-browser %s").open("https://facebook.com")    
    elif "open perplexity" in c.lower():
        webbrowser.get("/usr/bin/brave-browser %s").open("https://perplexity.com")    
    elif "open chatgpt" in c.lower():
        webbrowser.get("/usr/bin/brave-browser %s").open("https://chatgpt.com")    

    elif c.lower().startswith("play"):
        song = " ".join(c.lower().split(' ')[1:]) 
        if song in musicliberary.music:
            link = musicliberary.music[song]
            webbrowser.get("/usr/bin/brave-browser %s").open(link) 
            speak(f"Playing {song} song.....")

        else:
            speak(f"Sorry sir, i couldnt find {song} in your library.")       

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])

            if not articles:
                speak("Sorry sir, no news articles found.")
            else:
                for i, article in enumerate(articles[:5], start=1):  # Limit to 5
                    headline = article.get("title", "No title available")
                    print(f"{i}. {headline}")
                    speak(headline)
        else:
            speak(f"Error fetching news. Status code {r.status_code}")
            print(r.text)

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)


    


if __name__ == "__main__":
    speak("Initializing Sam........")
    while True:
        # Listen for the wake word "Sam"
        # obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing...")    
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            command = r.recognize_google(audio)
            print(f"You said: {command}")
            if "hello sam" in command.lower():
                speak("Yes sir.")
                # Listen for command
                with sr.Microphone() as source:
                    print("Sam is Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        
        except Exception as e:
            print("Error; {0}".format(e))