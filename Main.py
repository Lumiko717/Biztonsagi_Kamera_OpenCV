# Készítette Szabó Dóra - G9AJVV

import cv2
import numpy as np

felv = cv2.VideoCapture('vtest.avi')                                # sétáló emberek tesztvideó
# felv = cv2.VideoCapture('vauto.avi')                              # játékautó tesztvideó
# felv = cv2.VideoCapture('http://100.120.35.184:8080/video')       # IP Kamera próba

ret, frame1 = felv.read()                                           # videókép első frame-jének beolvasása
ret, frame2 = felv.read()                                           # videókép második frame-jének beolvasása


while felv.isOpened():
    kulombseg = cv2.absdiff(frame1, frame2)                         # két frame közötti abszolút külömbség
    szurke = cv2.cvtColor(kulombseg, cv2.COLOR_BGR2GRAY)            # szürkeárnyalatos átalakítás
    elmos = cv2.GaussianBlur(szurke, (5, 5), 0)                     # szürkeárnyalatos kép pixeleinek elmosás
    _, kuszob = cv2.threshold(elmos, 20, 255, cv2.THRESH_BINARY)    # kontúrkereséshez küszob beállítása
    kitoltes = cv2.dilate(kuszob, None, iterations=3)               # üres területek kitöltése
    konturak, _ = cv2.findContours(kitoltes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # kontúrák megkeresése

    konturtomb = np.array(konturak)                                 # kontúrák tömbbe gyüjtése
    i = 0

    # cv2.drawContours(frame1, konturak, -1, (0, 255, 0), 2)        # minden kontúra vonnalla való megjelenítése

    for kontura in konturak:                                        # ciklus kontúrákon való végigléptetéshez
        konturtomb[i] = kontura                                     # a legutolső érzékelt kontúra betöltése a tömbbe
        i = i + 1

        if cv2.contourArea(konturtomb[0]) > 800:                    # kontúra méretéve szabályozható szűkítés
            (x, y, w, h) = cv2.boundingRect(konturtomb[0])          # kontúra köré rajzolt kijelölő négyzet sarkai
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)   # kijelölő négyzet kirajzolása

    # cv2.putText(frame1, "Statusz: {}".format('Mozgas Erzekelve'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    # Felső státusz jelzés

    cv2.imshow("Biztonsagi Kamera", frame1)                         # Frame megjelenítés
    frame1 = frame2                                                 # következő frame-re váltás
    ret, frame2 = felv.read()                                       # a következő frame beolvasása a videóképből

    if cv2.waitKey(40) == 27:                                       # kilépés ESC-gombbal
        break

cv2.destroyAllWindows()                                             # ablak/ok bezárása
felv.release()                                                      # videófálj törlése a memóriából
