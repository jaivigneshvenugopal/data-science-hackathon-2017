import time
import requests
import cv2
import os
import importlib
from tkinter import *

_url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=age,gender'
_key = '9478277299d942caa0dabbbe8104f1d4'
_maxNumRetries = 10


def processRequest( json, data, headers, params ):
    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429: 

            print( "Message: %s" % ( response.json()['error']['message'] ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )

        break
        
    return result

def getBand(age):
    if(age <= 14):
        return 1
    elif (age > 14 and age <= 24):
        return 2
    elif (age > 24 and age <= 49):
        return 3
    elif (age > 49 and age <= 74):
        return 4
    else:
        return 5

def main(alch, smoke):
    camera = cv2.VideoCapture(0)
    while True:
        return_value,image = camera.read()
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imshow('image',gray)
        if cv2.waitKey(1)& 0xFF == ord('s'):
            cv2.imwrite('test.jpg',image)
            break
    camera.release()
    cv2.destroyAllWindows()

    pathToFileInDisk = r'test.jpg'
    with open( pathToFileInDisk, 'rb' ) as f:
        data = f.read()
       

    params = { 'visualFeatures' : 'Faces'} 

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'

    json = None

    result = processRequest(json, data, headers, params )
    gender = (result[0]['faceAttributes']['gender']).title()
    age = int(result[0]['faceAttributes']['age'])
    ageBand = str(getBand(age))
    #print(gender + " " + str(age))
    ML = importlib.import_module('mltest')
    cancer = ML.getMostCommonCancer(gender,ageBand, alch, smoke)
    #print(cancer)
    os.remove("test.jpg")
    master = Tk()
    message = "Gender: " + gender + "\n" + "Estimated age: " + str(age) + "\n" + "The most common form of cancer among your age group is "+ cancer
    w = Message(master, text="Gender: " + gender + "\n" + "Estimated age: " + str(age) + "\n"
                + "The most common form of cancer among people from your age group is "+ cancer
                + "\n\n" + "Most people survive early stage cancer, get tested now!" , font = 15, width = 500)
    w.pack()

window = Tk()

def close_window():
    window.destroy()
    main(alch.get(), smoke.get())

Label(window, text="Please tick accordingly").grid(row=0, sticky=W)
alch = IntVar()
smoke = IntVar()
Checkbutton(window, text="Do you smoke?", variable=smoke, font = 15).grid(row=1, sticky=W)
Checkbutton(window, text="Do you consume alchohol?", variable=alch,font = 15).grid(row=2, sticky=W)
Button(window, text='Ok', command=close_window).grid(row=3, sticky=W, pady=4)

