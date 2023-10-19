import pyttsx3
import datetime
import sys
import speech_recognition as sr
import re

import pyrebase


config = {}  # credentials to your realtime database

firebase = pyrebase.initialize_app(config)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voices', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish(datetime):
    hr = int(datetime.datetime.now().hour)
    if hr >= 0 and hr < 12:
        speak('good morning')
    elif hr >= 12 and hr < 18:
        speak('good afternoon')
    else:
        speak('good evening')


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listtenning')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('recognising!!')
        query = r.recognize_google(audio, language='en-in')
        print('user said-', query)
    except Exception as e:
        print(e)
        return 'none'
    return query


if __name__ == '__main__':
    wish(datetime)

    while 1:

        speak('say add to add items, query for query an item, remove to remove items, stop to turn off')
        query = takecommand().lower()
        print(query)

        if 'add' in query:
            while (1):
                speak('say the item to add or exit to return')
                inp = takecommand().lower()
                if inp == 'exit':
                    break
                try:
                    print(inp)
                    patterns = re.findall(
                        pattern="([a-zA-Z]*) ([\d]*)", string=inp)
                    print(patterns)
                    speak(
                        f"fruit added is {patterns[0][0]} and number of itmes is {patterns[0][1]} and date {str(datetime.datetime.now())[:10]}")
                    to_add = patterns[0]
                    try:
                        item = {'Name': to_add[0], 'Count': to_add[1], 'DOA': str(
                            datetime.datetime.now())[:10]}
                        print(item)

                        db = firebase.database()
                        db.child('record').push(item)
                        speak("Item added successfully")
                    except:
                        speak('Failed to add')

                except:
                    speak('invalid input')

        elif 'query' in query:

            speak('how can I help you say exit to return')
            user_query = takecommand().lower()  # say the item name

            if user_query == 'exit':
                break

            flag = 0

            db = firebase.database()
            user_ref = db.child('record').get()

            for key, doc in user_ref.val().items():
                if user_query == doc["Name"]:
                    speak(
                        f'A total of {doc["Count"]} of {doc["Name"]} was present which was added on {doc["DOA"]}')
                    flag = 1
                    break

            if flag == 0:
                speak("Element not found")

        if 'remove' in query:
            while (1):
                speak('say the item to remove or exit to return')
                inp = takecommand().lower()
                if inp == 'exit':
                    break
                try:
                    print(inp)
                    patterns = re.findall(
                        pattern="([a-zA-Z]*) ([\d]*)", string=inp)
                    print(patterns)
                    speak(
                        f"fruit being removed is {patterns[0][0]} and number of itmes is {patterns[0][1]} ")
                    to_add = patterns[0]
                    try:
                        db = firebase.database()
                        user_rec = db.child('record').get()
                        for key, value in user_ref.val().items():
                            if value['Name'] == to_add[0]:
                                db.child('record').child(key).update(
                                    {'Count': value["Count"] - to_add[1]})
                        speak("Item added successfully")
                    except:
                        speak('Failed to add')

                except:
                    speak('invalid input')

        if 'stop' in query:
            speak('good night!')
            break

    sys.exit()
