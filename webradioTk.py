#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.messagebox import *
import vlc
import time

class Webradio:
    """ webradio player via VLC"""
    def __init__(self):
        self.vlc = vlc.Instance()
        self.radio = self.vlc.media_player_new()

        self.fluxradio = [ "http://direct.franceinfo.fr/live/franceinfo-midfi.mp3",
       "http://direct.franceinter.fr/live/franceinter-midfi.mp3",
         "http://direct.fipradio.fr/live/fip-webradio4.mp3",
         "http://direct.francemusique.fr/live/francemusique-midfi.mp3",
         "http://cdn.nrjaudio.fm/adwz1/fr/30407/mp3_128.mp3?origine=fluxradios",
        "http://novazz.ice.infomaniak.ch/novazz-128.mp3",
                      "http://direct.fipradio.fr/live/fip-midfi.mp3", "http://direct.franceculture.fr/live/franceculture-midfi.mp3",
                           "http://radiomeuh.ice.infomaniak.ch/radiomeuh-128.mp3", "http://tsfjazz.ice.infomaniak.ch/tsfjazz-high.mp3"]
        self.index = [ "France Info", "France Inter", "FIP Monde",
                  "France Musique", "Rires et Chansons", "Nova", "FIP", "France Culture", "Radio Meuh", "TSF Jazz" ]

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
        self.quitter = Button(self.cadre1, text="Quitter", command=self.Stop, fg="red")
        self.quitter.pack()

        self.m = IntVar()
        self.text = StringVar()
        self.text.set("écoute")
        self.son = Label(self.cadre1, text="son:")
        self.son.pack()
        self.mute = Checkbutton(self.cadre1, textvariable=self.text, variable=self.m, command=self.Muet, anchor="w")        
        self.mute.pack(fill="x")

        self.var_case = IntVar()
        self.case1 = Radiobutton(self.cadre2, text="France Info", variable=self.var_case, value=0, anchor="w", fg=coul, command=self.Finfo)
        self.case2 = Radiobutton(self.cadre2, text="France Inter", variable=self.var_case, value=1, anchor="w", fg=coul,command=self.Finter)
        self.case3 = Radiobutton(self.cadre2, text="Fip", variable=self.var_case, value=2, anchor="w", fg=coul, command=self.Fip)
        self.case4 = Radiobutton(self.cadre2, text="France Musique", variable=self.var_case, value=3, anchor="w",fg=coul, command=self.Fmus)
        self.case5 = Radiobutton(self.cadre2, text="Rire et chansons", variable=self.var_case, value=4, anchor="w", fg=coul, command=self.Retc)
        self.case6 = Radiobutton(self.cadre2, text="Nova", variable=self.var_case, value=5, anchor="w", fg=coul, command=self.Nova)
        self.case7 = Radiobutton(self.cadre2, text="France Culture", variable=self.var_case, value=6, anchor="w", fg=coul,  command=self.Fculture)
        self.case8 = Radiobutton(self.cadre2, text="Radio Meuh", variable=self.var_case, value=7, anchor="w", fg=coul, command=self.Meuh)
        self.case9 = Radiobutton(self.cadre2, text="TSF Jazz", variable=self.var_case, value=8, anchor="w", fg=coul, command=self.Tsf)
        self.case1.pack(fill="x")
        self.case2.pack(fill="x")
        self.case3.pack(fill="x")
        self.case4.pack(fill="x")
        self.case5.pack(fill="x")
        self.case6.pack(fill="x")
        self.case7.pack(fill="x")
        self.case8.pack(fill="x")
        self.case9.pack(fill="x")
        

        self.titre1 = Label(self.cadre2, text="Autre radio:")
        self.titre1.pack()

        self.string = StringVar()
        self.string.set("url webradio")
        self.entree = Entry(self.cadre2, textvariable=self.string, width=20)
        self.entree.pack()
        self.ok = Button(self.cadre2, text="Go", command=self.Autre)
        self.ok.pack(fill="x")
        
        self.resizable(False, False)

        

    def Muet(self):
        if self.m.get() == 1:
            self.text.set("muet")
            radio.Mute(1)
            
        else:
            self.text.set("écoute")
            radio.Mute(0)

    def Finfo(self):
        
        radio.Lecture(0)

    def Finter(self):
        radio.Lecture(1)

    def Fip(self):
        radio.Lecture(6)

    def Fmus(self):
        radio.Lecture(3)

    def Retc(self):
        radio.Lecture(4)

    def Nova(self):
        radio.Lecture(5)

    def Fculture(self):
        radio.Lecture(7)

    def Meuh(self):
        radio.Lecture(8)

    def Tsf(self):
        radio.Lecture(9)

    def Stop(self):
        radio.Quitter(1)
        Interface.destroy(self)

    def Autre(self):
        self.url = self.entree.get()
        radio.Url(self.url)
        time.sleep(2)
        if radio.Etat() == 1:
            print("ok")
        elif radio.Etat() ==0:
            print("erreur")
            showerror("Erreur", "Impossible de se connecter à ce flux")

            


if __name__ == "__main__":
    app = Interface(None)
    app.title("WebRadio")
    app.protocol("WM_DELETE_WINDOW", app.Stop)
    app.withdraw()
    app.deiconify()
    app.mainloop()
