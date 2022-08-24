# Author: Lissan Koirala
# Date: 2020-05-28

print("-"*119)
print("Getting Things Ready!")
print("-"*119)

import os, shutil # To have acess to the operating system
import speech_recognition as sr # To recognise the thing that we are speaking
import datetime # To get the current time 
import webbrowser # To open the URL provided
import pyttsx3
import time
from googlesearch import search 
import cv2
import face_recognition
import numpy as np

what_can_i_do = """
I am only on when your face has been recognised,
My abilities are as follows:
- I can give you weather informations
- I can set a reminder for you 
- I can read your reminders!
- I can tell you the time
- I can set a timer for you.
- I can set an alram for you, but I guarentee that\nyou will not hear it!
- I can open YouTube with various lists of languages and songs
- I can give you a lastest news headlines
- I can give you coronavirus news
"""

def get_encoded_faces():
    encoded = {}
    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = face_recognition.load_image_file("faces/" + f)
                encoding = face_recognition.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding
    return encoded

def classify_face(faces):
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    img = cv2.imread("captured_face.jpg", 1)
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)
    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"
        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)
        os.remove("captured_face.jpg")
        return face_names[0]

def take_photo(name):
    if ".png" in name or ".jpg" in name:
        file_name = name
    else:
        file_name = "captured_face.jpg"
    if name == "none":
        print("Your Real time Photo is being taken for Identity Purpose, LookUp on the webcam")
        print("-"*119)
    x = 0
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        return "Error"
    cv2.imwrite(file_name, frame)
    if x != "fail":
      return "Sucess"

def speak(what):
      engine = pyttsx3.init()
      voices = engine.getProperty('voices')
      engine.setProperty('rate', 150)
      engine.setProperty('voice', voices[1].id)
      engine.say(what)
      engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)   # This takes the audio and transfers it to the text [User]
        except:
            pass
    print("I heard : ",said)
    return said

try:
	f = open("setup.txt","r")
	f.close()
	setup = True
except:
	setup = False

if setup == True:
	alram = "no"
	while True:
	      take_photo("none")
	      faces = get_encoded_faces()
	      name = classify_face(faces)
	      f = open("setup.txt","r")
	      n = f.read()
	      f.close()
	      user = n[26:]
	      if name == None:
	      	name = "none"         

	      if user in name: # Only starts the program if it is called, if not stands by until called.
	            speak("I am on sir, How can I help you?")
	            while True: # This continues until the user says exit
	                  print("Assistant is Active still!")
	                  print("-"*119)
	                  text = get_audio() # Then it gets the audio from the user
	                  if "read" in text or "reminders" in text:
	                        speak("Hmm... Just a second, let me have a look!")
	                        f = open("reminders.txt",'r')  # Here it reads out the reminders.
	                        reminders = f.read()
	                        f.close()
	                        speak(reminders)
	                  
	                  elif "note" in text or "remind" in text:
	                        index_text = text[0]
	                        if index_text == "n":
	                              note_text = text[5:]
	                        else:
	                              note_text = text[10:]

	                        f = open("reminders.txt",'r')   # This makes a note and saves it in the reminder file
	                        previous_reminders = f.read()
	                        f.close()
	                        time = datetime.datetime.now()
	                        time = time.strftime("%H:%M")
	                        write_text = previous_reminders + "\nYour told me to remind you " + note_text + " at " + time + ","
	                        f = open("reminders.txt",'w')
	                        f.write(write_text)
	                        f.close()
	                        speak("you reminder has been set!")
	                  
	                  elif "time" in text and "what" in text:
	                        texts = datetime.datetime.now()
	                        text_time = "The time is " + texts.strftime("%H:%M")  # This tells the actual time
	                        speak(text_time)

	                  elif "set" in text and "timer" in text:
	                        z = "yes"
	                        speak("For how long you want the timer to run sir?")
	                        seconds = get_audio()             # This sets an timer for the time which is said
	                        try:
	                              index = seconds.index(" ")
	                        except:
	                              index = seconds.index("-")
	                        what = seconds[index:]
	                        times = seconds[:index]
	                        if "sec" in what:
	                              pass
	                        elif "min" in what:
	                              times = int(times) * 60
	                        elif "hour" in what:
	                              speak("Would you like to set an alarm instead?")
	                              conf = get_audio()
	                              if "yes" or "ok" or "that's great" in conf:
	                                    alram = "yes"
	                                    
	                              else:
	                                    times = int(times) * 60 * 60
	                        else:
	                              speak("Oops, seems you provided incorrect units, the possible units are: seconds, minutes, hours.")
	                              z = "no"
	                        if z != "no":
	                              time.sleep(int(times))
	                              speak("alram.mp3")
	                              
	                  elif "alarm" in text and "set" in text or alram == "yes":
	                        speak("when_alram.mp3")
	                        t = get_audio()
	                        try:
	                              f = open("alram.txt",'r')
	                              previous_alram = f.read()
	                              f.close()
	                        except:
	                              previous_alram = ""
	                              f = open("alarm.txt","w")
	                              f.write(" ")
	                              f.close()
	                        t = previous_alram + t
	                        f = open("alarm.txt","w")
	                        f.write(t)
	                        f.close()
	                        speak("Your alarm has been set sir!")
	                                   
	                  elif "YouTube" in text:
	                        speak("which_song.mp3")
	                        conformation = get_audio()
	                        if "english" in conformation:
	                              webbrowser.open("https://www.youtube.com/watch?v=XwxLwG2_Sxk&list=PLDIoUOhQQPlXzhp-83rECoLaV6BwFtNC4") # This opens the youtube and plays the music in the language allocated
	                        elif "nepali" in conformation:
	                              webbrowser.open("https://www.youtube.com/watch?v=mdvJJMAjZlc&list=PLm_3vnTS-pvnc4wnMI7UYko1uiSX73ahd")
	                        else:
	                              webbrowser.open("https://www.youtube.com/watch?v=5Yu_wePKsRE")

	                  elif "news" in text or "headlines" in text:
	                        speak("Which language news would you like to hear sir? You know many languages!")
	                        conformation = get_audio()
	                        if "english" in conformation or "English" in conformation or "language" in conformation:
	                              speak("Which channel would you like sir?")
	                              channel = get_audio()      # This plays the news in the language allocated
	                              if channel == "BBC":
	                                    print("Opening BBC news")
	                                    webbrowser.open("https://www.bbc.co.uk/")
	                                    
	                              elif channel == "Sky":
	                                    print("Opening Sky news")
	                                    webbrowser.open("https://www.youtube.com/watch?v=9Auq9mYxFEE")
	                                    
	                              elif channel == "CNN":
	                                    print("Opening CNN news")
	                                    webbrowser.open("https://edition.cnn.com/")
	                                    
	                              else:
	                                    speak("Sorry, I didn't get that!")
	                        else:
	                              webbrowser.open("https://www.bbc.com/nepali/multimedia/radio_programmes")

	                  elif "virus" in text: ## Get the inforamtion from the coronavirus website and then uptade me and then talk 
	                        webbrowser.open("https://www.worldometers.info/coronavirus/#countries")
	                        
	                  elif "weather" in text:
	                        try:
	                              f = open("city.txt",'r')
	                              city_name = f.read()
	                              f.close()
	                              ask = "no"
	                              speak("Just a second...!")
	                        except:
	                              speak("Oops, I haven't got any information on where you live! Could you please provide me with the city name please?")
	                              city_name = get_audio()
	                              ask = "yes"
	                        try:
	                              f = open("alternative_cities.txt",'r')
	                              alternative_cities = f.read()
	                              f.close()
	                              ask_alt = "no"
	                        except:
	                              ask_alt = "yes"

	                        import requests, json
	                        appid = "" # Get this from openweathermap
	                        complete_url = f"http://api.openweathermap.org/data/2.5/weather?appid={appid}&q={city_name}" 
	                        response = requests.get(complete_url) 
	                        x = response.json() 
	                        if x["cod"] != "404":
	                              y = x["main"] 
	                              current_temperature = y["temp"] 
	                              z = x["weather"] 
	                              weather_description = z[0]["description"] 
	                              total = city_name + ". Temperature : " + str(int(current_temperature - 273.15)) + "°C." + "\nDescription : " + str(weather_description)
	                              speak(total)
	                              if ask == "yes":
	                                    speak("Is this the city you live sir?")
	                                    conf = get_audio()
	                                    if "yes" in conf:
	                                          f = open("city.txt",'w')
	                                          f.write(city_name)
	                                          f.close()
	                                    else:
	                                          speak("Task Aborted")
	                                    if ask_alt == "yes":
	                                          speak("Would you like to hear any other cities information by default sir?")
	                                          con = get_audio()
	                                          if "yes" in con or "ofcourse" in con:
	                                                speak(" Okay, could you please write them down by seperating them with commas, a file will open for you shortly!")
	                                                f = open("alternative_cities.txt",'w')
	                                                f.close()
	                                                os.system("alternative_cities.txt")
	                                                speak("That's great thanks alot sir!")
	                        if ask_alt == "no":
	                              speak("Now these are the alternative cities weather information. Hmm, bare with me for a moment please!")
	                              cities = alternative_cities.split(",")
	                              number = 0
	                              for i in cities:
	                                    city_name = cities[number]
	                                    number += 1
	                                    complete_url = "http://api.openweathermap.org/data/2.5/weather?appid=1c7741dee5e386d8fbe4f00222888d2d&q=" + city_name 
	                                    response = requests.get(complete_url) 
	                                    x = response.json() 
	                                    if x["cod"] != "404":
	                                          y = x["main"] 
	                                          current_temperature = y["temp"] 
	                                          z = x["weather"] 
	                                          weather_description = z[0]["description"] 
	                                          total = city_name + ". Temperature : " + str(int(current_temperature - 273.15)) + "°C." + "\nDescription : " + str(weather_description)
	                                          speak(total)
	                                    else:
	                                          speak("Sorry, I couldn't find the weather inforamtion on the city named " + city_name + ".")

	                              speak("You can always change your account default settings. just say, 'Change my Account default settings!'")
	                        else: 
	                              speak("Oops, look that the city name provided was incorrect!")

	                  elif "account" in text and "change" in text:
	                        speak("Which default setting you want to change? Hmm... is it about weather default cities?")
	                        conf = get_audio()
	                        if "yes" in conf or "yeah" in conf:
	                              speak(" Okay, could you please write them down by seperating them with commas, a file will open for you shortly!")
	                              os.system("alternative_cities.txt")
	                              speak("That's great thanks alot sir!")

	                  elif "what can" in text:
	                  		speak("Here are the things I can do. A file will open up for you!")
	                  		f = open("abilities.txt","w")
	                  		f.write(what_can_i_do)
	                  		f.close()
	                  		os.system("abilities.txt")
	                  		os.remove("abilities.txt")
	                  		speak("Did you get what can I do. Now try those things out! I am listening........hmm, looks you already started talking. I am not listening to you now. Haha")
	                  		speak("Go on now, that was just for fun. Sorry if you were hurted by that! oops, haha")

	                  else:
	                        speak("Sorry, I didn't get that!")  # If it cannot reply then say's I can't reply to this
	                        speak("Would you like me to google that for you?")
	                        conf = get_audio()
	                        if "yes" in conf or "yeah" in conf:
	                              url = "https://www.google.com.tr/search?q={}".format(text)    
	                              webbrowser.open(url)
	                        else:
	                              speak("Ok, that's fine. These are the relevant links for your query, hope that helps!")
	                              for search_engine in search(text, tld="co.in", num=10, stop=10, pause=2): 
	                                    print(search_engine)
	      else:
	            print("Sorry, your face was not recognisied!, Only "+user+" can use this Voice Assistant\nTrying Again...")
	            print("-"*119)

else:
	try:
		os.mkdir("faces")
	except:
		pass
	print("Welcome to the Voice Assistant Setup!")
	print("-"*119)
	name = input("By what name you want me to Identify you? : ")
	print("-"*119)
	print("Ok, your real time photo is being taken, LookUp on the Webcam!")
	print("-"*119)
	take_photo(name+".jpg")
	print("Done, the photo has been taken!\nNow I can Recognise you by the name : " + name)
	print("-"*119)
	f = open("setup.txt","w")
	f.write("Setup has been done for : " + name)
	f.close()
	os.system("attrib +h setup.txt")
	shutil.move(name+".jpg", 'faces')
	print("You may now close this file as setup has been completed!\nOr just hit Enter")
	print("-"*119)
	time.sleep(5)


