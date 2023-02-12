import os
import subprocess
import random
import datetime
import requests 
import pyjokes
import speech_recognition
import gtts
import os
import playsound

def recordCommand():
    sr = speech_recognition 
    r = sr.Recognizer()
     
    with sr.Microphone() as source:  
        print("Listening...")
        r.pause_threshold = 1.2
        audio = r.listen(source)
  
    try:
        print("Recognizing...")   
        intent = r.recognize_google(audio, language ='en-in')
        print(f'What I heard: {intent}\n')
  
    except Exception as e:
        print(e)   
        replyToUser("Sorry, didn't understand that.")
        talk()
        return None
     
    return intent.lower()

def replyToUser(text):
    tts = gtts.gTTS(text,lang='en',slow='True')
    tts.save('talk.mp3')
    
def talk():
    playsound.playsound('talk.mp3')
    
while(True):
    
    intent = recordCommand()
    
    if(intent==None):
        replyToUser('Sorry, could not hear anything')
        talk()
        continue
        
    if 'play music' in intent or 'play a song' in intent:
        music_dir = "path to music directory"
        songs = os.listdir(music_dir)   
        os.system('xdg-open ' + os.path.join(music_dir, songs[random.randint(0,len(songs)-1)]))
        
    if 'google chrome' in intent or 'browser' in intent:
        subprocess.call('google-chrome')

    if 'vs code' in intent or 'write code' in intent:
        subprocess.call('code')

    if 'take a note' in intent:
        replyToUser('What should I write?')
        talk()
        note_text = recordCommand()
        if(note_text!=None):
            f = open('notes.txt','a')
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            f.write(timestamp + '\n')
            note = note_text + '\n\n'
            f.write(note)
            f.close()

    if 'weather' in intent:
        replyToUser('Which city?')
        talk()
        city = recordCommand()
        apiKey = 'your api key'
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}&units=metric')
        x = response.json()
        if x["cod"] != "404":
            y = x['main']
            temperature = x['main']["temp"]
            pressure = x['main']["pressure"]
            humidity = x['main']["humidity"]
            desc = x["weather"][0]["description"]
            weather_detail = f'Current temperature is {temperature}, pressure is {pressure} hPa, humidity is {humidity} %, Weather condition is {desc}'
            replyToUser(weather_detail)
            talk()
        else:
            replyToUser('Sorry, could not find the city')
            talk()

    if 'joke' in intent:
        joke = pyjokes.get_joke()
        replyToUser(joke)
        talk()
    
    if 'shutdown' in intent and 'minutes' in intent:
        for word in st.split():
            if(word.isdigit()==1):
                minutes = word
                break
        os.system(f'shutdown +{minutes}')
    
    if 'stop' in intent:
        replyToUser("Stopping")
        talk()
        break