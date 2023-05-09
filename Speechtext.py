import speech_recognition as sr
# import pyttsx3
 
# Initialize the recognizer
r = sr.Recognizer()
#listens for the user's input
with sr.AudioFile('Female_child.wav') as source:
    audio2 = r.listen(source)
  
# using google speech recognition
    text = r.recognize_google(audio2)
    print('Converting audio transcripts into text ...')
    print(text)