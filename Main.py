# Készítette Szabó Dóra - G9AJVV

import cv2
import numpy as np
import tkinter as tk
from tkinter import simpledialog
from tkinter import filedialog

# IP Video cím vagy Video fájl kiválasztáshoz felugró dialógus ablakok

root = tk.Tk()
root.withdraw()
UIP = simpledialog.askstring(title="IP Kamera", prompt="IP Kamera címe:")
if not UIP:
    root.filename = filedialog.askopenfilename(initialdir="/", title= "Valasszon video fajlt", filetypes=(("avi files", "*.*"), ("all files", "*.*")))
    felv = cv2.VideoCapture(root.filename)                         # Video forrás beolvasása fileból
else:
    felv = cv2.VideoCapture(UIP)                                   # IP Video kép beolvasása

#felv = cv2.VideoCapture('vtest.avi')                              # sétáló emberek tesztvideó
#felv = cv2.VideoCapture('vauto.avi')                              # játékautó tesztvideó
#felv = cv2.VideoCapture('http://100.120.35.184:8080/video')       # IP Kamera próba
#felv = cv2.VideoCapture('http://Lumi:Abyss11@192.168.1.102:7778/video')    # Saját mobilról működő IP camera címe


ret, frame1 = felv.read()                                           # videókép első frame-jének beolvasása
ret, frame2 = felv.read()                                           # videókép második frame-jének beolvasása

def empty(a):
    pass

# Videó beállítások nodosításához számozott csúszka

cv2.namedWindow("Parameterek")
cv2.resizeWindow("Parameterek", 900, 150)
cv2.createTrackbar("Kontur", "Parameterek", 20, 255, empty)
cv2.createTrackbar("Kitolt", "Parameterek", 15, 50, empty)


while felv.isOpened():
    KM = cv2.getTrackbarPos("Kontur", "Parameterek")
    KI = cv2.getTrackbarPos("Kitolt", "Parameterek")

    kulombseg = cv2.absdiff(frame1, frame2)                         # két frame közötti abszolút külömbség
    szurke = cv2.cvtColor(kulombseg, cv2.COLOR_BGR2GRAY)            # szürkeárnyalatos átalakítás
    elmos = cv2.GaussianBlur(szurke, (5, 5), 0)                     # szürkeárnyalatos kép pixeleinek elmosás
    _, kuszob = cv2.threshold(elmos, KM, 255, cv2.THRESH_BINARY)    # kontúrkereséshez küszob beállítása
    kitoltes = cv2.dilate(kuszob, None, iterations=KI)              # üres területek kitöltése
    konturak, _ = cv2.findContours(kitoltes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # kontúrák megkeresése


    konturtomb = np.array(konturak)                                 # kontúrák tömbbe gyüjtése
    i = 0

    #cv2.drawContours(frame1, konturak, -1, (0, 255, 0), 2)        # minden kontúra vonnalla való megjelenítése

    for kontura in konturak:                                            # ciklus kontúrákon való végigléptetéshez
        if cv2.contourArea(kontura) > KM:                               # kontúra méretéve szabályozható szűkítés
            konturtomb[i] = kontura                                     # a legutolső érzékelt kontúra betöltése a tömbbe
        i = i + 1

        (x, y, w, h) = cv2.boundingRect(konturtomb[0])                   # kontúra köré rajzolt kijelölő négyzet sarkai
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)    # kijelölő négyzet kirajzolása

    z = i

    cv2.putText(frame1, "Mozgo Alakok erzekelve: {}".format(z), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    # Felső státusz jelzés

    cv2.imshow("Biztonsagi Kamera", frame1)                         # Frame megjelenítés
    cv2.imshow("Szurke arnyalatos elmosott kep", elmos)             # Elmosott szurkearnyalatos kep megjelenitese
    cv2.imshow("Ures resz kitoltes utan", kitoltes)                 # Kitoltesi iteraciok megjelenitese
    frame1 = frame2                                                 # következő frame-re váltás
    ret, frame2 = felv.read()                                       # a következő frame beolvasása a videóképből

    if cv2.waitKey(40) == 27:                                       # kilépés ESC-gombbal
        break

cv2.destroyAllWindows()                                             # ablak/ok bezárása
felv.release()                                                      # videófálj törlése a memóriából

