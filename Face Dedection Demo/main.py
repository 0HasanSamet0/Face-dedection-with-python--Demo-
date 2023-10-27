from tkinter import Button, Entry, Label, Tk, messagebox
import cv2
import math
import webbrowser
import os
import requests
from selenium import webdriver
import tkinter as tk
import serial


#port=serial.Serial("COM6",9600) #arduino iletişim yolu
def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn=frame.copy()
    frameHeight=frameOpencvDnn.shape[0]
    frameWidth=frameOpencvDnn.shape[1]
    blob=cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (250, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections=net.forward()
    faceBoxes=[]
    for i in range(detections.shape[2]):
        confidence=detections[0,0,i,2]
        if confidence>conf_threshold:
            x1=int(detections[0,0,i,3]*frameWidth)
            y1=int(detections[0,0,i,4]*frameHeight)
            x2=int(detections[0,0,i,5]*frameWidth)
            y2=int(detections[0,0,i,6]*frameHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn,faceBoxes
url = "https://cdnarabic1.img.sputniknews.com/images/103707/40/1037074074.jpg"
img = cv2.imread(url)
faceProto="C:\\Users\\men\\Documents\\opencv\\Demo\\opencv_face_detector.pbtxt"
faceModel="C:\\Users\\men\\Documents\\opencv\\Demo\\opencv_face_detector_uint8.pb"
ageProto="C:\\Users\\men\\Documents\\opencv\Demo\\age_deploy.prototxt"
ageModel="C:\\Users\\men\\Documents\\opencv\Demo\\age_net.caffemodel"
genderProto="C:\\Users\\men\\Documents\\opencv\\Demo\\gender_deploy.prototxt"
genderModel="C:\\Users\\men\\Documents\\opencv\\Demo\\gender_net.caffemodel"

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
ageList=['(00-02)', '(04-06)', '(08-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList=['Male','Female']

faceNet=cv2.dnn.readNet(faceModel,faceProto)
ageNet=cv2.dnn.readNet(ageModel,ageProto)
genderNet=cv2.dnn.readNet(genderModel,genderProto)
video=cv2.VideoCapture(0)
padding=20
print("Yüz algılanmadı")
print(cv2.waitKey(1))
while -1<0:
    hasFrame,frame=video.read()
    if not hasFrame:
        cv2.waitKey()
        break

    resultImg,faceBoxes=highlightFace(faceNet,frame)
    if not faceBoxes:
       # port.write(b"0")
        print("yüz yok")
       

    for faceBox in faceBoxes:
        face=frame[max(0,faceBox[1]-padding):
                   min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
                   :min(faceBox[2]+padding, frame.shape[1]-1)]

        cerceve=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(cerceve)
        genderPreds=genderNet.forward()
        gender=genderList[genderPreds[0].argmax()]
        print(f'Gender: {gender}')

        ageNet.setInput(cerceve)
        agePreds=ageNet.forward()
        age=ageList[agePreds[0].argmax()]
        print(age[4:6])
        cv2.putText(resultImg, f'{age}', (faceBox[0], faceBox[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2, cv2.LINE_AA)
        cv2.imshow("Detecting age and gender", resultImg)
       # port.write(b"1")
    if cv2.waitKey(3) & 0XFF==ord('q'):
        break

   

if(int(age[4:6])<7):
        messagebox.showinfo("Yaş Kontrolü", "7 yaşindan küçük olduğunuz için ebeveyn kontrolsuz giris yapılamaz!")
       
def get_input():
    name = name_entry.get()  # 
    if(int(age[4:6])<50):
        with open("C:\\Users\\men\\Documents\\opencv\\Demo\\yasaklisiteler.txt", "r") as dosya:
            yasakli_siteler = dosya.read().splitlines()
            if name in yasakli_siteler:
                messagebox.showwarning("Site Erişimi","Site Erişimi İçin Yaşınız Uygun Değildir.")
            else:
                name = "https://www." + name.strip().lower() + ".com"
                webbrowser.open(name)
    else:
        name = "https://www." + name.strip().lower() + ".com"
        webbrowser.open(name)

window = Tk()
window.focus()


name_label = Label(window, text="Site İsmi:")
name_label.pack()

name_entry = Entry(window)
name_entry.pack()

submit_button = Button(window, text="Onayla", command=get_input)
submit_button.pack()
# 
window.mainloop()

video.release()
cv2.destroyAllWindows()