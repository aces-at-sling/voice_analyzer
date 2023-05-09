import requests

url = 'http://192.168.56.1:8000'
myfiles = {'file': open('Female_adult.wav' ,'rb')}

x = requests.post(url, files = myfiles)

#print the response text (the content of the requested file):

print(x)