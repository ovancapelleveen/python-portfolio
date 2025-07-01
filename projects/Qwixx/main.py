import re
import tkinter as tk
from tkinter import Button, Label, Frame, Tk

import os
from PIL import Image #, ImageTk
from PIL.ImageTk import PhotoImage
from random import randint, shuffle
from itertools import cycle
from sys import exit


class Window():
    #Logo van het spel
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_folder = os.path.join(BASE_DIR, "Qwixx_dice")
    # image_folder = f'.\\Qwixx_dice'
    bg_loc = os.path.join(image_folder, 'menu.jpg')
    # bg_loc = f'{image_folder}\\menu.jpg'
    bg_color = 'lightblue'
    fg_color = 'black'
    width = 1000
    height = 500
    imagesize = (120,150)

    #Initialiseer window
    def __init__(self, parent, naam):

        self.window = parent
        self.name = naam
        parent.title(naam)
        self.images = []
        #Root leegmaken bij volgende aanroep
        for widget in parent.winfo_children():
            widget.destroy()        

    def add_frame(self, master=None, x_pos=None, y_pos=None, grid=False, anchor_=tk.CENTER, relief=tk.FLAT, **kwargs):
        """Frame toevoegen aan het scherm."""
        if not master:
            master = self.window
        frame = Frame(master, relief=relief, bd=1, bg=Window.bg_color) # type: ignore
        self.place_widget(frame, x_pos, y_pos, grid, anchor_, **kwargs)
        return frame
    
    def place_widget(self, frame, x_pos=None, y_pos=None, grid=False, anchor_=tk.CENTER, **kwargs):
        """Frame toevoegen aan het scherm."""
        padx = None if 'padx' not in kwargs else kwargs['padx']
        pady = None if 'pady' not in kwargs else kwargs['pady']
        columnspan = None if 'columnspan' not in kwargs else kwargs['columnspan']
        if grid:
            frame.grid(column=x_pos, row=y_pos, sticky="nsew",padx=padx, pady=pady, columnspan=columnspan)
        elif x_pos and y_pos:
            frame.place(x=x_pos, y=y_pos, anchor=anchor_,padx=padx, pady=pady)
        else:
            frame.pack(padx=padx, pady=pady)
    
    def place_button(self, button, x_pos=None, y_pos=None, grid=False, tekst=None, enter_relief=tk.SUNKEN, leave_relief=tk.RAISED, enter_color=None, leave_color=None):
        button['relief'] = leave_relief
        if tekst:
            button['fg']=Window.bg_color
            button['activebackground']=Window.bg_color
        self.place_widget(button, x_pos, y_pos, grid)

        button.bind("<Enter>", lambda event: self.on_enter(button, enter_relief, enter_color, tekst))
        button.bind("<Leave>", lambda event: self.on_leave(button, leave_relief, leave_color, tekst))
        
    def on_enter(self, button, relief=tk.SUNKEN, color=None, text=None,):
        """Verander relief van een knop als de cursor erover hovered."""
        button['relief'] = relief
        if color:
            button['color'] = color
        if text:
            button['fg'] = Window.fg_color
    def on_leave(self, button, relief=tk.RAISED, color=None, text=None):
        """Verander relief van een knop als de cursor erover hovered."""
        button['relief'] = relief
        if color:
            button['color'] = color
        if text:
            button['fg'] = Window.bg_color

    #Vakjes op kaart aanbrengen
    def add_box(self, frame, value, color, x_pos, y_pos):
        Button(master = frame, text = value, fg = 'white', bg = color, borderwidth=1,relief="raised", width=4, height=1, font = ('calibri', 25)).grid(column=x_pos, row=y_pos, padx=2, pady=2)
    #Toegestane vakjes op kaart aanbrengen
    def add_button_box(self, frame, value, color, functie, x_pos, y_pos):
        Button(master = frame, text = value, fg = 'white', bg = color, borderwidth=1, relief="raised", width=4, height=1, font = ('calibri', 25), command=functie).grid(column=x_pos, row=y_pos, padx=2, pady=2)
    #Gemarkeerde vakjes op kaart aanbrenge
    def add_mark(self, frame, value, color, x_pos, y_pos):
        Button(master = frame, text = value, bg = color, borderwidth=2, relief="solid", width=4, height=1, font = ('calibri', 25, 'overstrike')).grid(column=x_pos, row=y_pos, padx=2, pady=2)
    #Dobbelstenen (plaatjes) toevoegen
    def add_die_img(self, frame, die, x_pos):
        img = PhotoImage(die.img)
        self.images.append(img)
        if die.color == 'White':
            bg='white'
        else:
            bg=Window.bg_color
        Label(master = frame, image = img, bg=bg).grid(column=x_pos, row=1, padx=3, pady=2)

    #Tekst-bericht toevoegen
    def add_text(self, text, frame=None, x_pos=None, y_pos=None, **kwargs):
        """Label toevoegen aan een frame."""
        if text:
            if not frame:
                frame = self.window
            label = Label(master=frame, text=text, bg=Window.bg_color, fg=Window.fg_color, font=('calibre',10,'bold'))
            for key, value in kwargs.items():
                try:
                    label[key] = value
                except Exception:
                    pass
            self.place_widget(label, x_pos, y_pos, **kwargs)

    def add_image(self, frame, image_, x_pos, y_pos, grid=True, **kwargs):
        """Afbeelding toevoegen aan het frame."""
        image = Label(master=frame, image=image_, bg=Window.bg_color)
        self.place_widget(image, x_pos, y_pos, grid, **kwargs)

    def add_button(self, frame, tekst, x_pos, y_pos, functie, width=13, height=2, grid=False):
        """Knop plaatsen."""
        btn = Button(master=frame, text=tekst, width=width, height=height, bg=Window.fg_color, fg=Window.bg_color, command = functie)
        self.place_button(btn, x_pos, y_pos, grid)
    
    #Bevestig knop toevoegen, ook 'Pas'-knop
    def add_confirm(self, functie, tekst="Bevestigen", x_pos=None, y_pos=None, width=13):
        """Bevestigknop toevoegen."""
        self.add_button(self.window, tekst=tekst, x_pos=x_pos, y_pos=y_pos, functie=functie, width=width)
        self.window.bind('<Return>', lambda event: functie())

    #Mislukte worpen toevoegen
    def add_failed(self, kaart, x_pos = None, y_pos = None):
        frame_failed = self.add_frame(x_pos=x_pos, y_pos=y_pos)
        self.add_text('Mislukte worpen:', frame_failed, x_pos=0, y_pos=0, grid=True, columnspan=4)
        for i in range(4):
            Label(master = frame_failed, text = f'{kaart.failed[i]}', bg = 'white', borderwidth=1, relief="solid", width=2, height=1, font = ('calibri', 25)).grid(row = 1, column=i)
####################################################

class Dice():
    #Locatie voor dobbelsteen-plaatjes
    colors = ['Red', 'Blue', 'Green', 'Yellow', 'White1', 'White2']
    imagesize = (70, 70)

    def __init__(self, name):
        self.value = randint(1,6)
        self.name = name
        self.color = re.findall('[A-z]+', self.name)[0]
        self.image_loc = os.path.join(Window.image_folder, f'White_{self.value}.png')
        # self.image_loc = f'{Window.image_folder}\\White_{self.value}.png'
        self.img = Image.open(self.image_loc).resize(Dice.imagesize)

    def roll(self):
        self.value = randint(1,6)
        self.image_loc = os.path.join(Window.image_folder, f'{self.color}_{self.value}.png')
        # self.image_loc = f'{Window.image_folder}\\{self.color}_{self.value}.png'
        self.img = Image.open(self.image_loc).resize(Dice.imagesize)

    def __repr__(self):
        return f'{self.name} {self.value}'
    
#Waardes van de gegooide dobbelstenen bepalen
class Values():

    colors = ['Red', 'Blue', 'Green', 'Yellow', 'White']

    def __init__(self, color, dice):
        self.color = color
        self.value1 = 0
        self.value2 = 0
        if color == 'White':
            for die in dice:
                if die.color == 'White':
                    self.value1 += die.value
                    self.value2 += die.value
        else:
            for die in dice:
                if die.name in [color, 'White1']:
                    self.value1 += die.value
                if die.name in [color, 'White2']:
                    self.value2 += die.value

    def __repr__(self):
        return f'{self.color}: {self.value1} en {self.value2}'

#Scorekaart is een verzameling van rijen per speler
class Scorekaart():

    base_list = list(range(2,13))
    red_list = base_list.copy()
    yel_list = base_list.copy()
    blu_list = base_list.copy()
    gre_list = base_list.copy()
    shuffle(red_list)
    shuffle(yel_list)
    shuffle(blu_list)
    shuffle(gre_list)

    aantal = 0
    players = []

    def __init__(self, player, random=False):
        self.player = player
        self.rows = [Row(color, random) for color in Row.colors]
        self.failed = ['','','','']
        self.score = 0
        self.gebruikt1 = False
        self.gebruikt2 = False

    #Markeer een vakje in een speficieke rij
    def mark(self, color, number):
        for row in self.rows:
            if row.color == color:
                row.mark(number)
    #Mislukte worp toevoegen
    def failed_throw(self):
        for i, entry in enumerate(self.failed):
            if entry == '':
                self.failed[i]='X'
                break

    #Punten optellen
    def add_score(self, aantal):
        self.score += int(aantal)

    def __repr__(self):
        return f'Scorekaart van {self.player}'

#Rijen met een kleur en een verzameling van vakjes
class Row():
    colors = ['Red', 'Yellow', 'Green', 'Blue']

    def __init__(self, color, random=False):
        self.color = color
        self.boxes = [Box(color, num, random) for num in Box.numbers]

    #Markeer een specifiek vakje in de rij
    def mark(self, num):
        for box in self.boxes:
            if box.number == num:
                box.mark()

#Class van vakjes
class Box():
    
    numbers = list(range(2,13))
    #Elk vakje heeft een zichtbare en onzichtbare waade (voor de volgorde)
    def __init__(self, color, number, random=False):
        if random:
            if color == 'Red':
                self.number = Scorekaart.red_list[number-2]
            elif color == 'Yellow':
                self.number = Scorekaart.yel_list[number-2]
            elif color == 'Blue':
                self.number = Scorekaart.blu_list[number-2]
            else:
                self.number = Scorekaart.gre_list[number-2]
        else:
            if color in ['Red', 'Yellow']:
                self.number = number
            else:
                self.number = 14 - number    

        self.marked = False        
        self.order = number - 1
            
    #Markeer een vakje
    def mark(self):
        self.marked = True
#######################################


#Window
def kiesmenu_aantal(root, random = False, lowerbound=2, upperbound=4):

    def submit_num(var):
        Scorekaart.aantal = var.get()
        if lowerbound <= Scorekaart.aantal <= upperbound:
            kiesmenu_spelers(root, random)
        else:
            window.add_text('Dat aantal is niet toegestaan!', x_pos=Window.width/2, y_pos=140)

    #Window initieren
    window = Window(root, 'Kiesmenu_aantal')
    # Create frames for top, bottom, and confirm sections
    frame_entries = window.add_frame(x_pos=Window.width/2, y_pos=240)
    #Velden toevoegen
    var=tk.IntVar()
    var.set(lowerbound)
    window.add_text(f'Aantal spelers (2-4): ', frame_entries, 0, 0, grid=True)
    inputfield = tk.Entry(frame_entries, textvariable = var, font=('calibre',10,'normal'))
    window.place_widget(inputfield, 1, 0, grid=True)
    inputfield.focus_force()
    #Bevestig-knop onderaan
    window.add_confirm(lambda: submit_num(var), x_pos=Window.width/2, y_pos=400)

#Window
def kiesmenu_spelers(root, random = False):

    def submit_name(var):
        Scorekaart.players = []
        for n in var:
            Scorekaart.players.append(Scorekaart(n.get(), random))
        if unique(Scorekaart.players):
            spel_spelen(root)
        else:
            window.add_text('Er mogen geen dubbele namen of lege velden zijn!', x_pos=Window.width/2, y_pos=140)
    #Window initieren
    window = Window(root, 'Kiesmenu_spelers')
    # Create frames for top, bottom, and confirm sections
    frame_entries = window.add_frame(x_pos=Window.width/2, y_pos=240)
    #Velden toevoegen
    var = [tk.StringVar() for _ in range(Scorekaart.aantal)]
    for i in range(Scorekaart.aantal):
        window.add_text(f'Speler {i+1}:', frame_entries, 0, i, grid=True)
        inputfield = tk.Entry(frame_entries, textvariable = var[i], font=('calibre',10,'normal'))
        window.place_widget(inputfield, 1, i, grid=True)
        if i == 0:
            inputfield.focus_force()
    #Bevestig-knop onderaan
    window.add_confirm(lambda var=var: submit_name(var), x_pos=Window.width/2, y_pos=400)


def unique(namen):
    if not namen:
        return False
    unique = []
    for naam in namen:
        if naam.player not in unique and naam.player:
            unique.append(naam.player)
    return len(unique) == len(namen)

def next_starter(inputlist):
    inputlist = inputlist[1:] + inputlist[:1]
    return inputlist

#Start van de beurt weergeven
def start_beurt(root, dice, vervolg_beurt):

    def dobbelen():
        # nonlocal dice
        for die in dice:
            die.roll()
        vervolg_beurt()

    window = Window(root, 'Beurt')
    frame_text = window.add_frame(x_pos=Window.width/2, y_pos=150)
    #Afbeelding plaatsen
    img_bg = PhotoImage(Image.open(Window.bg_loc).resize(Window.imagesize))
    window.images.append(img_bg)
    window.add_image(frame_text, img_bg, 0, 0)
    window.add_text(f"Het is nu de beurt aan {Scorekaart.players[0].player}", frame_text, 0, 1, grid=True)
    #Bevestig knop
    window.add_confirm(functie=dobbelen, tekst="Gooi dobbelstenen!", x_pos=Window.width/2, y_pos=350, width=15)


def spel_spelen(root):
    #Dobbelstenen initiëren
    dice = [Dice(color) for color in Dice.colors]

    def next_turn():
        nonlocal dice
        Scorekaart.players[0].gebruikt1 = False
        Scorekaart.players[0].gebruikt2 = False
        start_beurt(root, dice, lambda: spelerbeurt_wit(root, dice, na_wit))

    def na_wit():
        nonlocal dice
        einde, dice, reden = einde_controle(dice)
        if einde:
            #Spel is voorbij. Eindstand weergeven
            scoreberekening()
            eindstand(root, reden)
            return
        else:
            kiezen(root, Scorekaart.players[0], dice, einde_beurt, white=False)

    def einde_beurt():
        nonlocal dice
        if not Scorekaart.players[0].gebruikt1 and not Scorekaart.players[0].gebruikt2:
            Scorekaart.players[0].failed_throw()
        einde, dice, reden = einde_controle(dice)
        if einde:
            #Spel is voorbij. Eindstand weergeven
            scoreberekening()
            eindstand(root, reden)
            return
        else:
            Scorekaart.players = next_starter(Scorekaart.players)
            next_turn()
        
    next_turn()


#Score berekening
def scoreberekening():
    for kaart in Scorekaart.players:
        for row in kaart.rows:
            aantal = 0
            for box in row.boxes:
                if box.marked:
                    aantal +=1
                if box.marked and box.order == 11:
                    aantal +=1
            kaart.add_score(aantal*(aantal+1)/2)

        num_failed = kaart.failed.count('X')
        kaart.add_score(-5 * num_failed)


#Eindstand weergeven
def eindstand(root, reden):
    window = Window(root, 'Eindstand')
    window.add_text( f'Het spel is voorbij vanwege {reden}.', x_pos=500, y_pos=150)
    frame_kaart = window.add_frame(x_pos=500, y_pos=250)
    window.add_text('De eindstand is als volgt:', frame_kaart, x_pos=0, y_pos=0, grid=True, columnspan=2) 
    for i, kaart in enumerate(Scorekaart.players,1):
        window.add_text(kaart.player, frame_kaart, x_pos=0, y_pos=i, grid=True)
        window.add_text(kaart.score, frame_kaart, x_pos=1, y_pos=i, grid=True)

    window.add_text('Bedankt voor het spelen.', frame_kaart, x_pos=0, y_pos=5, grid=True, columnspan=2)
    window.add_confirm(lambda: menu("\nWil je nog een potje spelen?", "Opnieuw", root), x_pos = 500, y_pos = 400)


#Kijk of het spel voorbij is, 2 gesloten rijen, of een speler met 4 mislukte worpen
def einde_controle(dice):
    mislukt = False
    einde = False
    reden = ''

    for kaart in Scorekaart.players:
        #Kijk naar 4 mislukte worpen op elke kaart
        if kaart.failed.count('X') == 4:
            mislukt = True
            naam = kaart.player
        #Kijk naar rijen die gesloten zijn, verwijder vervolgens die dobbelsteen
        for row in kaart.rows:
            for box in row.boxes:
                if box.order == 11 and box.marked:
                    for i,die in enumerate(dice):
                        if die.color == row.color:
                            del dice[i]
    #Kijk of er 2 rijen zijn gesloten of iemand 4 mislukte worpen heeft
    if len(dice) == 4:
        einde = True
        reden = 'twee gesloten rijen'
    elif mislukt:
        einde = True
        reden = f'4 mislukte worpen van {naam}'
    return einde, dice, reden

#Deel 1 van de beurt, loopt ook door andere spelers voor de witte dobbelstenen
def spelerbeurt_wit(root, dice, callback):
    speler_counter = -1
    speler_cycle = cycle(Scorekaart.players)

    
    def next_player():
        nonlocal speler_counter
        speler = next(speler_cycle)
        speler_counter += 1
        if speler_counter == Scorekaart.aantal:
            callback()
            return
        else:
            kiezen(root, speler, dice, next_player)

    next_player()

#Vakje kiezen om te markeren
def kiezen(root, speler, dice, callback, white=True):
    #Markeer veld op kaart
    def mark_value(color, num):
        if speler==Scorekaart.players[0]:
            if white:
                speler.gebruikt1 = True
            else:
                speler.gebruikt2 = True
        speler.mark(color, num)
        callback()

    #Initieer window
    window = Window(root, 'Kiezen')
    #Kaart toevoegen
    frame_kaart = window.add_frame(x_pos=480, y_pos=180)
    frame_kaart['highlightbackground']="black"
    frame_kaart['highlightthickness']=1
    #Spelernaam en tekst toevoegen boven de kaart
    window.add_text(speler.player, frame_kaart, 0, 0, grid=True, columnspan=2, font=('Calibri', 20, 'bold'))
    beschrijving = f"Wil je de {'witte' if white else 'gekleurde'} dobbelstenen {f'van {Scorekaart.players[0].player} ' if speler != Scorekaart.players[0] else ''}gebruiken?"
    window.add_text(beschrijving, frame_kaart, x_pos=3, y_pos=0, grid=True, columnspan=8, font=('Calibri', 15, 'bold'))
    for i, row in enumerate(speler.rows, 1):
        for j,box in enumerate(row.boxes):
            values = Values('White' if white else row.color, dice)
            #Verschillende type knoppen toevoegen
            if box.marked:
                window.add_mark(frame_kaart, box.number, row.color, j,i)
            elif toegestaan(box, row, values, dice):
                window.add_button_box(frame_kaart, box.number, row.color, lambda color = row.color, num = box.number: mark_value(color, num), j,i)
            else:
                window.add_box(frame_kaart, box.number, row.color, j,i)

    #Dobbelstenen toevoegen
    frame_dice = window.add_frame(x_pos=300, y_pos=410, relief=tk.RAISED)
    window.add_text('Dobbelstenen', frame_dice, x_pos=0, y_pos=0, grid=True, columnspan=len(dice))
    for i, die in enumerate(dice):
        window.add_die_img(frame_dice, die, i)
    #Pas-knop toevoegen
    window.add_confirm(callback, f"{'Pas' if speler.gebruikt1 or white else 'Mislukte worp'}",610, 410)
    #Mislukte worpen toevoegen
    window.add_failed(speler, 780, 410)

#Controleer of waarde is toegestaan
def toegestaan(box, row, values, dice):
    mark_num = 0
    max_mark = 0
    colors = []
    for die in dice:
        colors.append(die.color)

    #Waarde is niet gegooid, waarde is al aangekruisd, of rij is al gesloten (dus dobbelsteen is niet meer aanwezig)
    if box.number not in [values.value1, values.value2] or box.marked or row.color not in colors:
        return False
    #Controle van gemarkeerde vakjes
    for box_ in row.boxes:
        if box_.marked:
            mark_num += 1
            max_mark = box_.order
    #Als een vakje verderop al gemarkeerd is
    if box.order <= max_mark:
        return False
    #Laatste vakje als er minder dan 5 andere gemarkeerd zijn
    if box.order == 11 and mark_num < 5:
        return False
    #Anders is het toegestaan
    return True

#Window
def menu(tekst:str, knoptekst:str, root:Tk):
    # Create an instance of tkinter window
    window = Window(root,'Start')
    #Plaatjes toevoegen
    frame_menu = window.add_frame(x_pos=Window.width/2, y_pos=150)
    img_bg = PhotoImage(Image.open(Window.bg_loc).resize(Window.imagesize))
    window.images.append(img_bg)
    # Create a Label Widget to display the text or Image
    window.add_image(frame_menu, img_bg, 0,0, grid=True)
    window.add_text(tekst, frame_menu, 0, 1, grid=True)
    #Start en stopknoppen
    window.add_button(window.window, knoptekst, Window.width/2, 300, lambda: kiesmenu_aantal(root))
    window.add_button(window.window, "Variant", Window.width/2, 350, lambda: kiesmenu_aantal(root, True))
    window.add_button(window.window, "Instructies", Window.width/2, 400, lambda: instructies(root))
    window.add_button(window.window, "Sluit spel", Window.width/2, 450, exit)

#Window
def instructies(root:Tk):
    window = Window(root,'Instructies')
    #Tekst om op het scherm te plaatsen
    instructietekst = "Klik op de kaarten om deze te spelen,\ntoep als je denkt te kunnen winnen."
    #Tekst toevoegen
    window.add_text(instructietekst, x_pos=Window.width/2, y_pos=250)
    #Knop toevoegen die terug gaat naar het hoofdmenu
    window.add_button(window.window, "Terug", x_pos=Window.width/2, y_pos=400, functie=lambda: menu("\nWil je een potje spelen?", "Start", root))

#Root
def main():
    root = Tk()
    root.title('Toepen')
    root.geometry(f'{Window.width}x{Window.height}+300+250')
    root.resizable(width=False, height=False)
    # root.minsize(Window.width,Window.height)
    # root.maxsize(Window.width,Window.height)    
    root.configure(background=Window.bg_color)
    menu("\nWil je een potje spelen?", "Start", root=root)
    root.mainloop()

if __name__ == '__main__':
    main()
    