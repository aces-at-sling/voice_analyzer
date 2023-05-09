from http.server import HTTPServer, BaseHTTPRequestHandler

import pandas as pd
import numpy as np
import scipy
import mir_eval
import joblib
import librosa

import speech_recognition as sr

clffg = joblib.load('cfl_gender.pkl')
clffa = joblib.load('cfl_age.pkl') 
clffd = joblib.load('cfl_dialect.pkl')

# Initialize the recognizer
# rec = sr.Recognizer()

class predictor():
    def pre_age_gend(self,sourcefile):
        y, sr = librosa.load(sourcefile, sr=24000)
        spectrogram = np.abs(librosa.stft(y))
        melspec = librosa.feature.melspectrogram(y=y, sr=sr)
        stft = np.abs(librosa.stft(y))
        mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
        mel = np.mean(librosa.feature.melspectrogram(y, sr=sr).T, axis=0)
        contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sr).T, axis=0)
        tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr).T, axis=0)
        chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sr).T,axis=0)
        features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
        features = features.reshape(1, -1)
        predgen = clffg.predict(features)
        # print("Gender Prediction: ", predgen)
        predage = clffa.predict(features)
        # print("Age Prediction: ", predage)
        # pred = clffd.predict(features)
        # print("Dialect Prediction: ", pred)
        return predgen, predage


class speechtotext():
    def s2t(self, sourcefile):
        rec = sr.Recognizer()
        #listens for the user's input
        with sr.AudioFile(sourcefile) as source:
            audio = rec.listen(source)
        
            # using google speech recognition
            text = rec.recognize_google(audio)
            return text
            


class helloHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        print('GET Method')
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        
        wavfile = self.rfile.read(content_length) # <--- Gets the data itself

        with open("samples/sample.wav", "wb") as binary_file:
            # Write bytes to file
            binary_file.write(wavfile)

        resultprediction = predictor()
        resulttext = speechtotext()

        gender, age = resultprediction.pre_age_gend('samples/sample.wav')

        text = resulttext.s2t('samples/sample.wav')

        print(gender[0])
        print(age[0])
        print(text)

        if(age[0]!="Youth"):
            print(text)
            self.wfile.write(text.encode("utf-8"))
        elif(age[0]=="Youth"):
            text =text + " Kids"
            self.wfile.write(text.encode("utf-8"))
            print(text)
        # self.wfile.write("Female_voice".encode("utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        print('POST Method')
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        print(content_length)
       
        # self.wfile.write("Female_voice")
#        print(post_data)
    
def main():
    IP = '192.168.56.1'
    PORT = 8000
    server =HTTPServer((IP,PORT),helloHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()


