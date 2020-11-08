import requests
import json
import pyttsx3
import speech_recognition as sr
import re
import subprocess
import datetime
from PyDictionary import PyDictionary
import math
import webbrowser 
import schedule 
import time 
import random



API_KEY = "t9v5r1iZegtK"
PROJECT_TOKEN = "tVFVS0P1xu8G"
RUN_TOKEN = "tBTJEMCYgkzM"



class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key


        }
        self.get_data()


    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data', params={"api_key": API_KEY})
        self.data = json.loads(response.text)

    
    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']



    def get_total_deaths(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Deaths:":
                return content['value']

    def get_country_data(self, country):
        data = self.data["country"]

        

        for content in data:
            if content['name'].lower() == country.lower ():
                return content 
        

    def get_list_of_countries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())

        return countries

data = Data(API_KEY, PROJECT_TOKEN)


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""


        try:
            said = r.recognize_google(audio)

        except Exception as e: 
            print("Exception:", str(e))

    return said.lower() 






def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt" 
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def dictionary():
    speak("dictionary")
    text = get_audio()
    SearchWord = text
    try:
        myDict = PyDictionary(SearchWord)
        speak(myDict.getMeanings())
    except:
        print('Not Found')



def take_a_break():
    speak("take a break. Go grab a healthy snack!")


def calculator (text):
        speak("calculator")
        text = get_audio()
        if "add" in text:
            speak("say first number")
        
            speak("say second number")
            text = get_audio()
            input = text 
            result = y
        
        

            return x + y

def make_flash_cards():
    speak("what is the word you want to add")
    word = get_audio()
    speak("what is the definition for this word")
    definition = get_audio()

    f= open("flash_cards.txt","a")

    f.write(word + ":" + definition)

    f.close()

def read_flash_cards():
    f= open("flash_cards.txt","r")
    count_line = 0
    for line in f:
        if line != "\n":
            count_line += 1

    for i in range (count_line):
        line = open("flash_cards.txt").read().splitlines()
        test = random.choice(line)

        end_of_word = 0

        for i in range(len(test)):
            if test[i] == ":":
                end_of_word = i

        word = test[:end_of_word]
        definition = test[end_of_word+1:]
       
        speak("the definition is: " + definition + "what is the word?")
        user_response = get_audio()
        print(test)
        if user_response == word:
            speak("corect!")
        else:
            speak("incorrect")


def stopwatch(start: int, end:int):
    f= open("tracker.txt","a")

    p = str("start time: " + str(start) + " end time: " + str(end))
    f.write(p)
    f.close()










def main():
    print("started program")
    data = Data(API_KEY, PROJECT_TOKEN)
    END_PHRASE = "stop"
    country_list = (data.get_list_of_countries())


    TOTAL_PATTERNS = {
                    re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
                    re.compile("[\w\s]+ total cases"): data.get_total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"):data.get_total_deaths,
                    re.compile("[\w\s]+ total deaths"): data.get_total_cases,
                  }

    COUNTRY_PATTERNS = {

                    			re.compile("[\w\s]+ cases [\w\s]+"): lambda country: data.get_country_data(country)['total_cases'],
                    re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],

                    }





    WAKE = "harvey"
    while True:
        print("listening...")
        text = get_audio()
        if text.count(WAKE) > 0:
            speak("i am ready")
            text = get_audio()
        print(text)
        result = None 

        for pattern, func in COUNTRY_PATTERNS.items():
            if pattern.match(text):
                words = set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break 




        for pattern, func in TOTAL_PATTERNS.items():
            if pattern.match(text):
                result = func()
                break 

        if result:
            speak(result)
        
        if text.find(END_PHRASE) != -1:
            print("Exit")
            break 
    
        NOTE_STRS = ["make a note", "write this down", "remember this"]
        for phrase in NOTE_STRS:
            if phrase in text.lower():
                speak("what would you like me to write down")
                
                note_text = get_audio().lower()
                note(note_text)
                speak("i've made a note of that")

        if "dictionary" in text:
            dictionary()

        if "make flash card" in text:
            make_flash_cards()

        if "read flashcards" in text:
            read_flash_cards()

        if "start study timer":
            start_time = datetime.datetime.now()
        if "end study timer":
            end_time = datetime.datetime.now()
            stopwatch(start_time, end_time)
            
            
main()
