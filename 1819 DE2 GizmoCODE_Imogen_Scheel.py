# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:39:32 2019

@author: Imogen Scheel
"""
#IMPORTS

from gpiozero import Button, Motor
from time import sleep
from PIL import Image
import pyttsx3
import speech_recognition as sr
import webbrowser
import urllib.request
import urllib.parse
import re
import wikipedia
import time
import os
import pygame      
import pytesseract 


#Setting up the motor to GPIO pins 20 and 21

motor = Motor(20, 21)

#Setting up Buttons

b1 = Button(2,17) #Each button is assigned two pins, the pins are shared with other buttons to conserve
b2 = Button(3,17) # the number of pins on the board, the method is known as Multiplexing.
b3 = Button(4,17) # n^k = number of buttons where 2n is the number of pins used hence significantly 
                  # reducing the number of pins used. Likewise: h*w = no. buttons, h+w = no. pins
b4 = Button(2,22)
b5 = Button(3,22)
b6 = Button(4,22)

b7 = Button(2,27)
b8 = Button(3,27)
b9 = Button(4,27)





def destination_search():
    
    Rows = [2,3,4]
    Cols = [17,22,27]
    
    Pins = [
                [b1, b2, b3],
                [b4, b5, b6],
                [b7, b8, b9]
    
             ]
    
    Countries = [  
                        ['London ', 'Paris ', 'Beijing '],
                        ['Sydney ', 'Tokyo ', 'Moscow '],
                        ['Berlin ', 'Dubai ', 'Madrid ']
                        ]
                        
    
    
    pin_list = b1 or b2 or b3 or b4 or b5 or b6                                 #While no button is pressed, no for loop is conducted
    button_list = [b1,b2,b3,b4,b5,b6]    
    if pin_list == 1:  
        s = None
        for i in range(0,3):                                                    #There are two pins with a logic of 1 as a button is pressed, which one is it?            
            for j in range(0,3):
                if Pins[i[0]] and Pins[i[1]] == i.is_pressed():
                    s = Countries[i][j]                                         #The code searches through an adjaceny matrix to find which pin is_active/ which button is_pressed and uses the location in this matrix to loaction the name of the place in another matrix of equivelent size.
                    
                   
    else:
        s = None                                                                #No pins are HIGH, you are unable to ask the globe any commands as it has not arrived at a place
        destination_search()
    engine.say(s);                                                              #Prepares engine for what it is to say
    engine.runAndWait() ;                                                       #Tells person which place they have landed at
    
    
    return s
               




def command(destination_country, motor):
    engine.say('Would you like to know about the history, culture, people, climate, or geography?')
    engine.runAndWait()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)                                                 #waiting to pic up response to question from user
        try:
            pass                                                                 #Preventing the programme from hearing wrong input
        except sr.UnknownValueError:
            engine.say('I didnt get that. I will try again')
            engine.runAndWait()
            command(destination_country)
            
    if r.recognize_google(audio) in voice_command:
        engine.say('How long do you want the spoken passage to be? Short, standard or long?')
        engine.runAndWait()
        with sr.Microphone() as source:
            response = r.listen(source)
            try:
                pass
            except sr.UnknownValueError:
                engine.say('I didnt get that. I will try again')
                engine.runAndWait()
                command(destination_country)
                
        if r.recognize_google(response) == 'short':
            n = 3
        elif r.recognize_google(response) == 'standard':
            n = 10
        elif r.recognize_google(response) == 'long':
            n=30
        try:
            motor.forward()                                                                          #Motor turns to open up the aperture, revealing the screen at the base of the globe
            sleep(0.8)                                                                               #The amount of time need to complete a rotation angle of 75 degrees with the specific motor used
            motor.stop()
            w = wikipedia.summary(destination_country + r.recognize_google(audio), sentences = n)
        except wikipedia.PageError:                                                                  #if there is no corrosponding category the script will present this error
            engine.say('Unfortunately there is no article for this category \
                       for this place, try another category.')
            engine.runAndWait()
            command(destination_country)
        new_w = w.replace("==", "")                                                                   #Headings in some articles contain == the space prevents the engine from saying 'equals equals'
        
        try:
            engine.say(new_w)
            engine.runAndWait()
        except:
            sr.UnknownValueError
            pass
        speech = r.recognize_google(audio)
        engine.say(new_w);
        engine.runAndWait() ;
       
        
        return speech
    
    
    
       
        

def youtube_search(destination_country, search_category):
    #new = 2
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'                     #chrome must be used for the following tasks
    query_string = urllib.parse.urlencode({"search_query" : destination_country + search_category})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())            #turns the search query into a string of numbers and letters which provides the correct end to the URL string
    url = "http://www.youtube.com/embed/" + search_results[0] + "?mute=1;autoplay=1"                   #plays the first search result from youtube, embed allows the screen to be maximised, mute stops the audio so the article can be heard
    webbrowser.get(chrome_path).open(url)
    #Motor would open apeture (forward)
    
    
    
 
    
    
def Flights(destination_country, departure_country, ShortCodes):                    #This function tells the user the cheapest flight from the place the just moved from and to the place they just moved to
    engine.say('Would you like to select another category? Yes or no?') 
    engine.runAndWait()
    with sr.Microphone() as source:
        answer = r.listen(source)
        try:
            pass
        except sr.UnknownValueError:
            engine.say('I didnt get that. I will try again')
            engine.runAndWait()
            command(destination_country)
            
    if r.recognize_google(answer) == 'yes':
        search_category = command(s)
        youtube_search(s, search_category)
    else:
        pass
    
    engine.say('Are you now inspired to fly to {}? Yes or no?' .format(destination_country))
    engine.runAndWait()
    with sr.Microphone() as source:
        answer = r.listen(source)
        try:
            pass
        except sr.UnknownValueError:
            engine.say('I didnt get that. I will try again')
            engine.runAndWait()
             
    if departure_country == None:
        engine.say('Please travel to a new place first ')
        engine.runAndWait()
        return
    if departure_country == destination_country:
        engine.say('Please move the counter to a new airport')
        engine.runAndWait()
        print('Please move the counter to a new airport')
        return
    if r.recognize_google(answer) == 'yes':
        motor.backward()                                                           # The aperture closes as the video is no longer relevant
        sleep(0.8)
        motor.stop()
        
        os.system("taskkill /im chrome.exe /f")                                    #Closes chrome to stop the video from playing
        
        engine.say('When do you want to fly? Give the date in numbers as follows: dd, mm, yy')
        engine.runAndWait()
        with sr.Microphone() as source:
            response = r.listen(source)
            try:
                pass
            except sr.UnknownValueError:
                engine.say('I didnt get that. I will try again')
                engine.runAndWait()
        date = r.recognize_google(response) 
        date_code = date[6] + date[7] + date[3] + date[4] + date[0] + date[1]       #the date is written as yymmdd in skyscanner's URL
        
        departure_SCode = ShortCodes[departure_country]                             #calling the cities short code from the dictionary of short codes to use in the URL
        destination_SCode = ShortCodes[destination_country]
        chrome_path = '/home/pi/directory/opt/chromium.exe'
        skyscanner_url = "https://www.skyscanner.net/transport/flights \            #red highlighted sections are to be ignored
        /{0}/{1}/{2}/?adults=1&children=&adultsv2=1&childrenv2=0&infants \
        =1&cabinclass=economy&rtn=0&preferdirects=false&outboundaltsenabled= \
        false&inboundaltsenabled=false&ref=home#results" \
        .format(departure_SCode, destination_SCode, date_code)                      #concatinating the skyscanner URL
        
        webbrowser.get(chrome_path).open(skyscanner_url)                            #skyscanner opens up to the page with flight prices to the place the user just moved to from the place they just moved from
        time.sleep(5)                                                               # gives time for the page to load
        
        size = width, height = 1536, 864                                            # 1536 x 864 is the resolution of screen used in the Globe
        screen = pygame.display.set.mode(size)
        pygame.image.save(screen, "/home/pi/directory/flight_prices.png")           #saves image to the directory
        os.system("taskkill /im chrome.exe /f")                                     #closes chrome as skyscanner is no longer needed
        
        imageObject = Image.open("/home/pi/directory/flight_prices.png")            #opens screenshotted page
        cropped = imageObject.crop((432, 685, 20, 15))                              #page is cropped around the cheapest price on the screen which always opens in the same position on the screen
        os.remove('/home/pi/directory/flight_prices.png')                           #whole screenshot of webpage is removed to free up the file path
        pygame.image.save(cropped, "/home/pi/directory/flight_prices.png")          #cropped image is saved in the same file path so only one image is saved at a time, freeing up memory for pi
        
        value=Image.open("/home/pi/directory/flight_prices.png")                    #cropped image is opened 
        price=pytesseract.image_to_string(value)                                    #pytesseract is used for Optical Character Recognition, it turns the image of the price into a string
        engine.say('The cheapest flight from {} to {} cost {}' \
                   .format(departure_country, destination_country, price)); #The engine tells the user the price of the cheapest flight
        engine.runAndWait() ;
        os.remove('/home/pi/directory/flight_prices.png') #removes the file so it can be written again for future flight searches, freeing up the memory
 
        pass
    else:
        pass
   





#MAIN SCRIPT
        
def Main():
       
    a = None
       
    while True:
        
        #Setting up python voice 
    
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        volume = engine.getProperty('volume')
        engine.setProperty('volume', 10.0)
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 25)
        
        #The list of different categories which can be given to the globe as voice inputs
        #in order to find out different facts above the place they have travelled to
    
        voice_command = ['history', 'culture', 'people', 'climate', 'geography']
        
        #The following dictionary holds the shortened codes used for different countries
        #required by the skysnners URL to complete a search for flights
        
        ShortCodes = {
                        'London ' : 'lond',
                        'Paris ' : 'pari',
                        'Beijing ': 'bjsa',
                        'Sydney ' : 'syda',
                        'Tokyo ' : 'tyoa',
                        'Moscow ' : 'mosc',
                        'Berlin ' : 'berl',
                        'Dubai ' : 'dxba'
                        }
        
        #The following calls the above functions consecutively
        
        s = destination_search() 
        search_category = command(s)
        youtube_search(s, search_category)
        Flights(s,a, ShortCodes)
        
        #The functions are called again, however recursively so that
        #the destination country becomes the departure country
        
        a = destination_search()
        search_category = command(a)
        youtube_search(a, search_category)
        Flights(a,s, ShortCodes)
        
        return
    

Main()


'''
REFERENCES:
    
Matrix keypad  -> https://www.raspberrypi.org/forums/viewtopic.php?t=211657  
Multiplexing   -> https://www.instructables.com/id/RaspberryPi-Multiple-Buttons-On-One-Digital-Pin/
Text to speech -> https://pypi.org/project/pyttsx3/    
Speech to text -> https://www.dexterindustries.com/howto/make-your-raspberry-pi-speak/
                  https://www.codementor.io/edwardzionsaji/simple-voice-enabled-chat-bot-in-python-kt2qi5oke
Youtube URL's  -> https://www.codeproject.com/Articles/873060/Python-Search-Youtube-for-Video
Cropping Images-> https://pythontic.com/image-processing/pillow/crop
Images to text -> https://blog.anirudhmergu.com/code/ocr-python-tesseract-ocr/
Multiprocessing-> https://stackoverflow.com/questions/25733934/python-run-two-commands-at-the-same-time
