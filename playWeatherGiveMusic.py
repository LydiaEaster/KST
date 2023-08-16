from bs4 import BeautifulSoup
import speech_recognition as sr
from num2words import num2words
from subprocess import call
import os
import requests
#import pyttsx3
import pywhatkit # import pywhatkit
#import datetime
#import wikipedia # import wikipedia
#import pyjokes #
#from ChatGPT_lite.ChatGPT import Chatbot

listener = sr.Recognizer()

cmd_beg= 'espeak '
# To play back the stored .wav file and dump the std errors to /dev/null
cmd_end= ' | aplay /home/least/Documents/alexaAssistant/bashRecord/Text.wav 2>/dev/null'
cmd_out= '--stdout > /home/least/Documents/alexaAssistant/bashRecord/Text.wav ' # To store the voice file

def talk(text):
  #Replacing ' ' with '_' to identify words in the text entered
  text = text.replace(' ', '_')

  #Calls the Espeak TTS Engine to read aloud a Text
  call([cmd_beg+cmd_out+text+cmd_end], shell=True)

#def talk(text):
#    engine.say(text)
#    engine.runAndWait()

# if I need to end the alexa, then it'll return 0
def take_command():
    try:
        print("in try")
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
    except Exception as e:
        print("Error! ", e)
        pass
    return command


def run_alexa():
    command = take_command()
    talk(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'what is the weather in ' in command:
        cityName = command.replace('what is the weather in ', '')
        weatherUrl = "https://www.google.com/search?q=" + "weather" + cityName
        html = requests.get(weatherUrl).content
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

        print("temp is ", temp)
        data = str.split('\n')
        sky = data[1]
        print("Sky Description: ", sky)

        weatherReport = "The temperature in " + cityName + " is " + temp + " and the sky is " + sky
        talk(weatherReport)
#    elif 'who is' in command:
#        person = command.replace('who is', '')
#        info = wikipedia.summary(person, 1)
#        print(info)
#        talk(info)
#    elif 'are you single' in command:
#        talk('I am in a relationship with wifi')
#    elif 'joke' in command:
#        talk(pyjokes.get_joke())
#    else:
#        talk('Please say the command again.')



run_alexa()