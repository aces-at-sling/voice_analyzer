import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt
# import seaborn
# seaborn.set(style='ticks')
# from IPython.display import Audio
import numpy as np
import scipy
import mir_eval
import joblib
import librosa
# import IPython.display

# use sox to record audio

clffg = joblib.load('cfl_gender.pkl')
clffa = joblib.load('cfl_age.pkl') 
clffd = joblib.load('cfl_dialect.pkl')
y, sr = librosa.load("Female_adult.wav", sr=24000)
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
pred = clffg.predict(features)
print("Gender Prediction: ", pred)
pred = clffa.predict(features)
print("Age Prediction: ", pred)
pred = clffd.predict(features)
print("Dialect Prediction: ", pred)