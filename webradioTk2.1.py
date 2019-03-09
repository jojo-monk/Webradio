#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from tkinter import *
from tkinter.messagebox import *
import vlc
import time
import threading
import os.path



class Record(threading.Thread):
    """ Enregistrement de la radio dans un fichier dans le dossier ~/webradio-record/'nom de la radio-0'.mp3
        ou sous 'autre-radio-0.mp3' lorsque le nom de la radio n'est pas connue"""
    
    def __init__(self, stream_url, flux):
        threading.Thread.__init__(self)
        self.fluxradio = [ "http://direct.franceinfo.fr/live/franceinfo-midfi.mp3",
       "http://direct.franceinter.fr/live/franceinter-midfi.mp3",
                           'http://direct.fipradio.fr/live/fip-midfi.mp3',
         "http://direct.francemusique.fr/live/francemusique-midfi.mp3",
         "http://cdn.nrjaudio.fm/adwz1/fr/30407/mp3_128.mp3?origine=fluxradios",
        "http://novazz.ice.infomaniak.ch/novazz-128.mp3",
                      "http://direct.franceculture.fr/live/franceculture-midfi.mp3",
                           "http://radiomeuh.ice.infomaniak.ch/radiomeuh-128.mp3",
                           "http://tsfjazz.ice.infomaniak.ch/tsfjazz-high.mp3"]

        self.index = [ "France Info", "France Inter", "FIP",
                  "France Musique", "Rires et Chansons", "Nova",
                       "France Culture", "Radio Meuh", "TSF Jazz" ]
        self.stream_url = stream_url
        self.flux = flux
        f = os.path.expanduser('~') + "/webradio-record"
        if not os.path.exists(f):
            os.makedirs(f)
        
        if self.stream_url < 9:
            self.url = self.fluxradio[self.stream_url]
            self.ad = requests.get(self.url, stream=True)
            i = 0
            self.filepath = f + "/" + self.index[self.stream_url] + "-" + str(i) + ".mp3"
            if os.path.exists(self.filepath):
                i+=1
                self.filepath = f + "/" + self.index[self.stream_url] + "-" + str(i) + ".mp3"
        else:
            self.ad = requests.get(self.flux, stream=True)
            i = 0
            self.filepath = f + "/autre-radio-" + str(i) + ".mp3"
            if os.path.exists(self.filepath):
                i+=1
                self.filepath = f + "/autre-radio-" + str(i) + ".mp3"
        
    def run(self):
        #self.s = s
        print("start")
        try:
            with open(self.filepath, 'wb') as self.f:
                for block in self.ad.iter_content(1024):
                    self.f.write(block)
        except:
            pass
        

    def stop(self):
        print("stop")
        self.f.close()

        
class Webradio:
    """ webradio player via VLC"""
    def __init__(self):
        self.vlc = vlc.Instance()
        self.radio = self.vlc.media_player_new()

        self.fluxradio = [ "http://direct.franceinfo.fr/live/franceinfo-midfi.mp3",
       "http://direct.franceinter.fr/live/franceinter-midfi.mp3",
                           'http://direct.fipradio.fr/live/fip-midfi.mp3',
         "http://direct.francemusique.fr/live/francemusique-midfi.mp3",
         "http://cdn.nrjaudio.fm/adwz1/fr/30407/mp3_128.mp3?origine=fluxradios",
        "http://novazz.ice.infomaniak.ch/novazz-128.mp3",
                      "http://direct.franceculture.fr/live/franceculture-midfi.mp3",
                           "http://radiomeuh.ice.infomaniak.ch/radiomeuh-128.mp3", "http://tsfjazz.ice.infomaniak.ch/tsfjazz-high.mp3"]
        self.index = [ "France Info", "France Inter", "FIP",
                  "France Musique", "Rires et Chansons", "Nova", "France Culture", "Radio Meuh", "TSF Jazz" ]

    def Lecture(self, r=0):
        self.r = r
        self.url = self.fluxradio[self.r]
        print(self.index[self.r])
        w = self.vlc.media_new(self.url)
        self.radio.set_media(w)
        self.radio.play()

    def Url(self, flux=""):
        self.flux = flux
        wr = self.vlc.media_new(self.flux)
        self.radio.set_media(wr)
        self.radio.play()
        
        

    def Mute(self, m=0):
        if m == 0 and self.radio.audio_get_mute():
            print("start")
            self.radio.audio_toggle_mute()
        elif m == 1 and not self.radio.audio_get_mute():
            print("muet")
            self.radio.audio_toggle_mute()

    def Quitter(self, q=0):
        if q == 1:
            print("quitter")
            self.radio.release()

    def Etat(self):
        return self.radio.is_playing()

    def GetVol(self):
        self.radio.audio_get_volume()

    def SetVol(self, vol=60):
        self.vol = vol
        self.radio.audio_set_volume(self.vol)
            

radio = Webradio()

class Interface(Tk):
    
    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""
    
    def __init__(self, fenetre):
        Tk.__init__(self, fenetre)
        self.fenetre = fenetre
        self.initialize()

    def initialize(self):
        self.cadre1 = Frame(self, self.fenetre, width=768, height=100, relief=GROOVE)
        self.cadre2 = Frame(self, self.fenetre, width=768, height=100, relief=GROOVE)
        self.cadre1.pack(side=TOP, padx=10, pady=10)
        self.cadre2.pack(side=BOTTOM, padx=10, pady=10)
        self.titre = Label(self.cadre1, text="WebRadio Player")
        self.titre.pack()
        coul = "blue"
        # Création de nos widgets
        self.quitter = Button(self.cadre1, text="Quitter", command=self.Stop, fg="black", bg="gray25")
        self.quitter.pack(fill="x")

        self.m = IntVar()
        self.v = IntVar()
        self.text = StringVar()
        self.text.set("écoute")
        self.son = Label(self.cadre1, text="son:")
        self.son.pack()
        self.mute = Checkbutton(self.cadre1, textvariable=self.text, variable=self.m, command=self.Muet, anchor="w")        
        self.mute.pack(side=LEFT, fill="x")
        self.volume = Scale(self.cadre1, orient="vertical", from_=100, to=0, resolution=1, length=60, label="Volume", variable=self.v, takefocus=1, command=self.Amp)
        self.volume.set(80)
        self.volume.pack(side=RIGHT, padx=5, pady=5)

        

        self.var_case = IntVar()
        self.case1 = Radiobutton(self.cadre2, text="France Info", variable=self.var_case, value=0, anchor="w", fg=coul, command=self.Rad)
        self.case2 = Radiobutton(self.cadre2, text="France Inter", variable=self.var_case, value=1, anchor="w", fg=coul,command=self.Rad)
        self.case3 = Radiobutton(self.cadre2, text="Fip", variable=self.var_case, value=2, anchor="w", fg=coul, command=self.Rad)
        self.case4 = Radiobutton(self.cadre2, text="France Musique", variable=self.var_case, value=3, anchor="w",fg=coul, command=self.Rad)
        self.case5 = Radiobutton(self.cadre2, text="Rire et chansons", variable=self.var_case, value=4, anchor="w", fg=coul, command=self.Rad)
        self.case6 = Radiobutton(self.cadre2, text="Nova", variable=self.var_case, value=5, anchor="w", fg=coul, command=self.Rad)
        self.case7 = Radiobutton(self.cadre2, text="France Culture", variable=self.var_case, value=6, anchor="w", fg=coul,  command=self.Rad)
        self.case8 = Radiobutton(self.cadre2, text="Radio Meuh", variable=self.var_case, value=7, anchor="w", fg=coul, command=self.Rad)
        self.case9 = Radiobutton(self.cadre2, text="TSF Jazz", variable=self.var_case, value=8, anchor="w", fg=coul, command=self.Rad)
        self.case10 = Radiobutton(self.cadre2, text="Autre radio : ", variable=self.var_case, value=9, anchor="w", fg=coul, command=self.Autre1)
        self.case1.pack(fill="x")
        self.case2.pack(fill="x")
        self.case3.pack(fill="x")
        self.case4.pack(fill="x")
        self.case5.pack(fill="x")
        self.case6.pack(fill="x")
        self.case7.pack(fill="x")
        self.case8.pack(fill="x")
        self.case9.pack(fill="x")
        self.case10.pack(fill="x")

        self.string = StringVar()
        self.string.set("url webradio")
        self.entree = Entry(self.cadre2, textvariable=self.string, width=20)
        self.entree.pack()
        self.entree.config(state='disabled')
        
        self.ok = Button(self.cadre2, text="Go", command=self.Autre)
        self.ok.pack(fill="x")
        self.ok.config(state='disabled')

        self.rec = Button(self.cadre2, text="Record", fg='red', command=self.Enreg)
        self.rec.pack(side=LEFT)

        self.arret = Button(self.cadre2, text="Stop", command=self.Arret)
        self.arret.pack(side=RIGHT)
        self.arret.config(state='disabled')
        
        
        self.resizable(False, False)
        

    def Muet(self):
        if self.m.get() == 1:
            self.text.set("muet")
            radio.Mute(1)
            
        else:
            self.text.set("écoute")
            radio.Mute(0)

    def Rad(self):
        self.r = self.var_case.get()
        # désactive l'entrée autre radio et le bouton go, si une radio prédéfinie est choisie
        self.entree.config(state='disabled')
        self.ok.config(state='disabled')
        radio.Lecture(self.r)
            

    def Stop(self):
        radio.Quitter(1)
        Interface.destroy(self)

    def Autre1(self):
        # active le champ autre radio et le bouton go
        self.entree.config(state='normal')
        self.ok.config(state='normal')

    def Autre(self):
        self.url = self.entree.get()
        radio.Url(self.url)
        time.sleep(1)
        if radio.Etat() == 1:
            print("ok")
        elif radio.Etat() == 0:
            print("erreur")
            showerror("Erreur", "Impossible de se connecter à ce flux", icon="error")

    def Amp(self, v):
        self.v = self.volume.get()
        radio.SetVol(self.v)

    def Enreg(self):
        
        self.rec.config(state='disabled')
        self.arret.config(state='normal')
        self.a = self.var_case.get()
        if self.a < 9:
            print(self.a)
            self.e = Record(self.a, 0)
            self.e.start()
        else:
            self.url = self.entree.get()
            self.e = Record(10, self.url)
            self.e.start()
            

    def Arret(self):
        self.arret.config(state='disabled')
        self.e.stop()
        self.rec.config(state='normal')
        


if __name__ == "__main__":
    
    app = Interface(None)
    app.title("WebRadio")
    app.protocol("WM_DELETE_WINDOW", app.Stop)
    app.withdraw()
    app.deiconify()
    app.mainloop()
    
