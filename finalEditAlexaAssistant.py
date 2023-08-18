import requests
import json
from bs4 import BeautifulSoup
import speech_recognition as sr
from num2words import num2words
from subprocess import call
import os
#import pyttsx3
import pywhatkit # import pywhatkit
#import datetime
#import wikipedia # import wikipedia
#import pyjokes #
#from num2words import num2words
#from subprocess import call
import re
import time

twoSeconds = 2
current_time = time.time()


cmd_beg= 'espeak '
cmd_end= ' | aplay /home/least/Documents/alexaAssistant/bashRecord/Text.wav  2>/dev/null' # To play back the stored .wav file and to dump the std errors to /dev/null
cmd_out= '--stdout > /home/least/Documents/alexaAssistant/bashRecord/Text.wav ' # To store the voice file


dataFile = '/home/least/Documents/alexaAssistant/chatGPT-Test/data.json'
headersFile = '/home/least/Documents/alexaAssistant/chatGPT-Test/headers.json'
chatGptResponse = '/home/least/Documents/alexaAssistant/chatGPT-Test/chatGptResponse.json'

listener = sr.Recognizer()

#cmd_beg= 'espeak'

# To play back the stored .wav file and dump the std errors to /dev/null
#cmd_end= ' | aplay /home/least/Documents/alexaAssistant/bashRecord/Text.wav 2>/dev/null'
#cmd_out= '--stdout > /home/least/Documents/alexaAssistant/bashRecord/Text.wav' # To store the voice file

def sleepTwoSeconds():
  time.sleep(2)

def putQuestionInJson(question):
  with open(dataFile, 'r') as f:
    data = json.load(f)
    for item in data['messages']:
      item['content'] = question
    with open(dataFile, 'w') as f:
      json.dump(data, f)

def getData():
  with open(dataFile, 'r') as f:
    data = json.load(f)
  return data


def getHeaders():
  with open(headersFile, 'r') as f:
    headers = json.load(f)
  return headers


def makeOpenAIRequest(question):
  url = 'https://api.openai.com/v1/chat/completions'

  putQuestionInJson(question)
  headers = getHeaders()
  print(headers)
  data = getData()

  response = requests.post(url, headers=headers, json=data)
  if response.status_code == 200:
    response = response.json()
    content = response['choices'][0]['message']['content']
    #print("Content type = ", content)
    print("Content is: ", content)
#    with open(chatGptResponse, 'w') as f:
#      f.write(content)
#      f.close()
    return content
  else:
    print("Error! ")
    print(response.status_code)


def talk(text):
  #text = input("Enter the Text: ")
  print("text is :")
  print(text)

  cleanedString = re.sub(r'[^a-zA-Z\s]', '', text)

  #Replacing ' ' with '_' to identify words in the text entered
  text = cleanedString.replace(' ', '_')
  #text = cleanedString.replace('\n', '_')
  print("cleaned string is: ", cleanedString)
  text = cleanedString.replace(' ', '_')

  #Calls the Espeak TTS Engine to read aloud a Text
  call([cmd_beg+cmd_out+text+cmd_end], shell=True)



# if I need to end the alexa, then it'll return 0
def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
    except Exception as e:
        print("Error! ", e)
        command = " "
        pass
    return command

def separate_words(sentence):
    words = sentence.split()
    return words

def run_alexa():
    command = take_command()
    print("command is: ", command)
    talk(command)
    isPlayingMusic = False
#    command = "what is snow like"
    commandInIndices = separate_words(command)

    if commandInIndices[0] == 'play':
        isPlayingMusic = True
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
        #isPlayingMusic = True
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
    else:
        response = makeOpenAIRequest(command)
        speakWithGpt(response)
    return isPlayingMusic


def speakWithGpt(response):
  hasErrors = False
  wouldLikeMoreInfo = True
  validInput = False
  #talk(response)
  #response = command
  lines = response.splitlines()
  print("****** lines is: ", lines)
  talk(lines[0])

  talk("Would you like more information")


  while validInput != True:
    command = take_command() #taking yes or no
    #
    if command == "no":
      wouldLikeMoreInfo = False
      validInput = True
    elif command == "yes":
      wouldLikeMoreInfo = True
      validInput = True
    else:
      talk("Please say yes or no")
      #command = take_command()


  if wouldLikeMoreInfo == True:
    giveMoreInfo(lines)

  return hasErrors

def giveMoreInfo(lines):
  lineNumber = 0
  for line in lines:
    print("in for line in lines")
    lineNumber = lineNumber + 1
    if lines[1]:
      print("This line: \n", line, "\n was already spoken")
    elif line and (not line.isspace()):
      print("This is a new line ", lineNumber)
      print("line is ", line)
            #if line != None and line and (not line.isspace()):
            #    talk("Next line")
      sentences = line.split(".")
      for sentence in sentences:
        print("sentence is ", sentence)
        talk(sentence)
        sleepTwoSeconds()
        continue
    else:
      print("That's the end of the response!")
            #    talk(line)
#                talk("next line")
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


def main():
  isPlayingMusic = False
  while isPlayingMusic == False:
    print("in main and isPlayingMusic is ", isPlayingMusic)
    isPlayingMusic = run_alexa()
  if isPlayingMusic == True:
    # TODO
    print("isPlayingMusic is ", isPlayingMusic)

main()
