import tkinter as tk
from tkinter import Button, Label, Frame, Tk

import os
from PIL import Image
from PIL.ImageTk import PhotoImage
from random import shuffle
from itertools import cycle
from sys import exit

class Card:
    """Represents a single playing card."""
    suits = ['Harten', 'Schoppen', 'Ruiten', 'Klaveren']
    ranks = ['7', '8', '9', '10', 'Boer', 'Vrouw', 'Heer', 'Aas']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_folder = os.path.join(BASE_DIR, "Speelkaarten")
    bg_loc = os.path.join(image_folder, 'achterkant.png')
    imagesize = (121,150)

    def __init__(self, suit="0", rank="0"):
        self.suit = suit
        self.rank = rank
        self.player = ''
        self.image_loc = os.path.join(Card.image_folder, f'{suit}_{rank}.png')
        self.img = Image.open(self.image_loc).resize(Card.imagesize)

    def __repr__(self):    
        return f'{self.suit} {self.rank}'

class Player:
    aantal = 3
    players = []
    losers = []
    toeper = ''

    def __init__(self, name, deck = False):
        self.name = name 
        self.score = 0
        self.rondescore = 1
        if deck:
             self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.ranks]
        else:
            self.cards = []
        self.size = 0
        self.selected_card = Card()

    def add_score(self, ronde = 1):
        self.score += self.rondescore
        self.rondescore = ronde

    def add_rondescore(self):
        self.rondescore += 1
    
    def __add__(self, card):
        if isinstance(card, Card):
            self.cards.append(card)
            self.size += 1
        return self

    def __sub__(self, card):
        if isinstance(card, Card):
            if card in self.cards:
                self.cards.remove(card)
                self.size -= 1
            else:
                raise ValueError(f"The card {card} is not in {self.name}.")
        return self

    def draw(self, target_deck):
        """Draws cards from this deck to another deck (like a hand).
           If not enough cards are available, reshuffle from discard pile.
        """
        self.shuffle_deck()
        self.move_cards(target_deck, 4)    

    def move_cards(self, target, num):
        for _ in range(num):
            drawn_card = self.cards.pop(0)  # Take the top card (or first card in the list)
            self.size -= 1 
            target += drawn_card

    def shuffle_deck(self):
        """Shuffles the deck."""
        shuffle(self.cards)

    def top_card(self):
        """Returns the top card of the deck (for discard pile)."""
        if self.cards:
            return self.cards[0]
        return None

    def play_card(self, card, target):
        """Plays a card from the hand to the discard pile, if allowed."""
        self -= card
        target += card
        card.player = self.name

    def setup(self, deck):
        self.cards = []
        self.size = 0
        deck.draw(self)
        self.rondescore = 1

    def wascheck(self):
        plaatje = 0
        zeven = 0
        for card in self.cards:
            if card.rank in ['Aas', 'Heer', 'Vrouw', 'Boer']:
                plaatje += 1
            elif card.rank == '7':
                zeven += 1
        return (plaatje == 4 or (plaatje == 3 and zeven == 1))

    def was(self, deck):
        self.move_cards(deck, self.size)
        deck.draw(self)
    
    def __repr__(self):        
        return f'{self.name} with {len(self.cards)} cards: {self.cards} rondescore: {self.rondescore} en score: {self.score}'
#Einde class Player==============================================================================================

class Window():
    bg_color = 'pink'
    fg_color = "#660666"
    width = 1900
    height = 1000
    btn_color = "#E2D8E2"

    def __init__(self, parent, naam=None):
        self.window = parent
        self.naam = naam
        self.window.title(naam)
        self.images = []
        #Root leegmaken bij volgende aanroep
        for widget in parent.winfo_children():
            widget.destroy()

        self.window.bind('<Escape>', exit)


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

    def add_frame(self, master=None, x_pos=None, y_pos=None, grid=False, anchor_=tk.CENTER, **kwargs):
        """Frame toevoegen aan het scherm."""
        if not master:
            master = self.window
        frame = Frame(master, relief=tk.FLAT, bd=5, bg=Window.bg_color)
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

    def place_button(self, button, x_pos=None, y_pos=None, grid=False, tekst=None, enter_relief=tk.SUNKEN, leave_relief=tk.RAISED, enter_color=None, leave_color=None, **kwargs):
        button['relief'] = leave_relief
        if tekst:
            button['fg']=Window.bg_color
            button['activebackground']=Window.bg_color
        self.place_widget(button, x_pos, y_pos, grid, **kwargs)
        button.bind("<Enter>", lambda event: self.on_enter(button, enter_relief, enter_color, tekst))
        button.bind("<Leave>", lambda event: self.on_leave(button, leave_relief, leave_color, tekst))

    def add_label(self, text, frame=None, x_pos=None, y_pos=None, **kwargs):
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

    def add_button(self, frame, tekst, x_pos, y_pos, functie, borderwidth=5, width=10, height=2, grid=False):
        """Knop plaatsen."""
        btn = Button(master=frame, text=tekst, borderwidth=borderwidth, width=width, height=height, bg=Window.fg_color, fg=Window.bg_color, command = functie)
        self.place_button(btn, x_pos, y_pos, grid)
  
    def add_btn_card(self, frame, image_, tekst, col, row, functie_tuple, **kwargs):
        """Knop kaart toevoegen."""
        btn = Button(master=frame,text=tekst, image=image_, bg=Window.bg_color, fg=Window.fg_color, command=lambda var=functie_tuple[1]: functie_tuple[0](var), compound='top')
        self.place_button(btn,col,row, tekst=tekst, enter_relief=tk.FLAT, leave_relief=tk.FLAT, **kwargs)

    def add_cards(self, speler, label, x_pos = None, y_pos = None, functie = None, functie2 = None, valid = None, players = False):
        if speler and speler.cards:
            frame_cards = self.add_frame(x_pos=x_pos, y_pos=y_pos)
            self.add_label(label, frame_cards, 0, 0, grid=True, columnspan=speler.size)
            for id_, kaart in enumerate(speler.cards):
                # Create an object of tkinter ImageTk
                img = PhotoImage(kaart.img)
                self.images.append(img)

                if not valid is None:
                    if kaart in valid:
                        self.add_btn_card(frame_cards, img, f"Speel {kaart}",  id_, 1,(functie,kaart), grid=True, padx=5)
                    else:
                        self.add_btn_card(frame_cards, img, f"Speel {kaart}", id_, 1, (functie2, kaart), grid=True, padx=5)
                else:
                    self.add_image(frame_cards, img, id_, 1, padx=5)

                if players:
                    self.add_label(f"Door {kaart.player}", frame_cards, id_, 2, grid=True)

    def add_confirm(self, functie, x_pos=None, y_pos=None):
        """Bevestigknop toevoegen."""
        self.add_button(self.window, "Bevestigen", x_pos, y_pos, functie)
        self.window.bind('<Return>', lambda event: functie())
####################################################

#Window
def kiesmenu_aantal(root, tekst, na_kiesmenu, lowerbound=2, upperbound=4):

    def submit_num(var):
        Player.aantal = var.get()
        if lowerbound <= Player.aantal <= upperbound:
            na_kiesmenu(root)
        else:
            window.add_label('Dat aantal is niet toegestaan!', x_pos=Window.width*0.5, y_pos=Window.height*0.3)


    #Window initieren
    window = Window(root, 'Kiesmenu_aantal')
    # Create frames for top, bottom, and confirm sections
    frame_entries = window.add_frame(x_pos=Window.width*0.5, y_pos=Window.height*0.44)
    #Velden toevoegen
    var=tk.IntVar()
    var.set(upperbound)
    window.add_label(f'Aantal {tekst}:', frame_entries, 0, 0, grid=True)
    inputfield = tk.Entry(frame_entries, textvariable = var, font=('calibre',10,'normal'))
    window.place_widget(inputfield, 1, 0, grid=True)
    inputfield.focus_force()
    #Bevestig-knop onderaan
    window.add_confirm(lambda var=var: submit_num(var), x_pos=Window.width*0.5, y_pos=Window.height*0.6)

#Window
def kiesmenu_spelers(root):

    def submit_name(var):
        Player.players = []
        Player.losers = []
        for n in var:
            Player.players.append(Player(n.get()))
        if unique(Player.players):
            kiesmenu_aantal(root, 'punten', spel_spelen, 1, 15)
        else:
            window.add_label('Er mogen geen dubbele namen of lege velden zijn!', x_pos=Window.width*0.5, y_pos=Window.height*0.3)
   
   #Window initieren
    window = Window(root, 'Kiesmenu_aantal')
    # Create frames for top, bottom, and confirm sections
    frame_entries = window.add_frame(x_pos=Window.width*0.5, y_pos=Window.height*0.44)
    #Velden toevoegen
    var = [tk.StringVar() for _ in range(Player.aantal)]
    for i in range(Player.aantal):
        window.add_label(f'Speler {i+1}:', frame_entries, 0, i, grid=True)
        inputfield = tk.Entry(frame_entries, textvariable = var[i], font=('calibre',10,'normal'))
        window.place_widget(inputfield, 1, i, grid=True)
        if i == 0:
            inputfield.focus_force()
    #Bevestig-knop onderaan
    window.add_confirm(lambda var=var: submit_name(var), Window.width*0.5, Window.height*0.6)

def unique(namen):
    if not namen:
        return False
    unique = []
    for naam in namen:
        if len(naam.name)>10:
            return False
        if naam.name not in unique and naam.name:
            unique.append(naam.name)
    return len(unique) == len(namen)

#Initialiseer spelerhanden vanuit deck
def create_hands():
    #Genereer kaarten
    deck = Player('Deck', True)
    #Genereer spelerhanden vanuit deck
    for speler in Player.players:
        #Genereer handen
        speler.setup(deck)
    return deck

#Window
def bevestigen(root, functie, speler):
    window = Window(root, 'Bevestigen')
    frame_confirm = window.add_frame(x_pos=Window.width*0.5, y_pos=Window.height*0.44)

    img_bg = PhotoImage(Image.open(Card.bg_loc).resize(Card.imagesize))
    window.images.append(img_bg)
    # Create a Label Widget to display the text or Image
    window.add_image(frame_confirm, img_bg, 0, 0)
    window.add_label(f'Het is nu de beurt van {speler.name}.\nBevestig dat jij deze speler bent.', frame_confirm, 0, 1, grid=True)
    #Start en stopknoppen
    window.add_confirm(functie, x_pos=Window.width*0.5, y_pos=Window.height*0.6)

#Begin met wassen
def was_ronde(root, deck, na_was):
    counter = -1
    spelers = cycle(Player.players)
    def next_player():
        nonlocal counter
        counter += 1
        speler = next(spelers)
        if counter >= len(Player.players):
            na_was()
            return
        bevestigen(root, lambda: wil_wassen(speler), speler)

    def wil_wassen(speler, bericht='', nieuw_deck=None):
        nonlocal deck
        if nieuw_deck:
            deck=nieuw_deck
        if bericht == 'gelukt':
            bericht = 'Niemand controleerd de was, je trekt een nieuwe hand.'
            speler.was(deck)
        #Nee = next_player() werkt!
        ja_nee_vraag(root, speler, "Wil je wassen?", bericht, 'wassen', next_player, wil_wassen, deck)
        #Ja = Player.windex = id -> checkronde(root, wil_wassen)
    next_player()

def check_ronde(root, deck, wil_wassen):
    speler_cycle = cycle(Player.players)
    speler = next(speler_cycle)
    def next_player():
        speler = next(speler_cycle)
        if speler == Player.players[0]:
            bevestigen(root, lambda: wil_wassen(speler, 'gelukt'), speler)
            return
        bevestigen(root, lambda var=deck: wil_checken(var), speler)

    def wil_checken(deck):
        #Nee = next_player()
        bericht=f'{Player.players[0].name} wil wassen.'
        ja_nee_vraag(root, speler, "Wil je checken?", bericht, 'checken', next_player, wil_wassen, deck)
        #Ja = wascontrole(root, id, na_check) 
    next_player()

#Window
def was_controle(root, checker, deck, na_check):
    #1 knop naar na_check
    window = Window(root, 'was_controle')
    #Kaarten toevoegen van beide spelers
    window.add_cards(Player.players[0], f"Handkaarten {Player.players[0].name}:", x_pos=Window.width*0.5, y_pos=Window.height*0.3)
    window.add_cards(checker, "Jouw handkaarten:", Window.width*0.5, Window.height*0.6)

    if Player.players[0].wascheck():
        resultaat = 'Het was een correcte was, je krijgt daarvoor een strafpunt.'
        bericht = f"Het was een correcte was en werd gecontroleerd, {checker.name} kreeg daarvoor een strafpunt. Je ontvangt een nieuwe hand."
        checker.add_score()
        Player.players[0].was(deck)
    else:
        resultaat = f"Het was een foute was. {Player.players[0].name} krijgt een strafpunt."
        bericht = f"Het was een foute was en werd gecontroleerd door {checker.name}, je kreeg daarvoor een strafpunt."
        Player.players[0].add_score()
    #Tekst toevoegen
    window.add_label(resultaat, x_pos=Window.width*0.5, y_pos=Window.height*0.17)
    #Bevestigknop toevoegen
    window.add_confirm(lambda: bevestigen(root, lambda: na_check(Player.players[0], bericht, deck), Player.players[0]), Window.width*0.5, 750)

def next_starter(inputlist, start):
    if start in inputlist:
        while inputlist[0] != start:
            inputlist = inputlist[1:] + inputlist[:1]
    else: 
        raise ValueError("Start zit niet in de inputlijst")
    return inputlist


#Window
def ja_nee_vraag(root, speler, vraag, bericht, vraagtype, functie_nee, callback, deck=None, pile = None):

    def confirm(var):
        if var=='wassen':
            Player.players = next_starter(Player.players, speler)
            check_ronde(root, deck, callback)
        elif var=='checken':
            was_controle(root, speler, deck, callback)
        elif var=='toepen':
            speler.add_rondescore()
            callback()

    def deny(var):
        if var=='wassen' or var=='checken':
            functie_nee()
        elif var=='toepen':
            speler.add_score(0)
            functie_nee()

    # Create an instance of tkinter window
    window = Window(root, 'Ja_nee_vraag')

    #Tekst toevoegen indien nodig
    window.add_label(bericht, x_pos=Window.width*0.5, y_pos=Window.height*0.17)
    #Gespeelde kaarten toevoegen
    window.add_cards(pile, 'Gespeelde kaarten:', Window.width*0.5, Window.height*0.3, players = True)
    #Kaarten toevoegen
    window.add_cards(speler, "Handkaarten:", Window.width*0.5, Window.height*0.6)

    frame_confirm = window.add_frame(x_pos=Window.width*0.5, y_pos=Window.height*0.75)
    window.add_label(vraag, frame_confirm, 0, 0, grid=True, columnspan=2)
    #Knoppen toevoegen
    window.add_button(frame_confirm, "Ja", 0, 1, lambda: confirm(vraagtype), grid=True)
    window.add_button(frame_confirm, "Nee", 1, 1, lambda: deny(vraagtype), grid=True)

def bekennen(speler, pile):
    beken = False
    if not pile.cards:
        suit = ''
        bericht = 'Speel de eerste kaart, bepaal daarmee de kleur die moet worden bekend.'
    else:
        suit = pile.top_card().suit
        bericht = f'De gespeelde kleur is {suit}.'

        for card in speler.cards:
            if card.suit == suit:
                beken = True
                break
        if beken:
            bericht = '\n'.join([bericht, 'Je moet kleur bekennen.'])  
        else:
            suit = ''
            bericht = '\n'.join([bericht,'Je kan geen kleur bekennen'])
    return suit, bericht

#Window
def choose_card(root, speler, pile, valid, bericht, na_selectie):
    # print('choose_card()')

    def extract_card(kaart:Card):
        # print(f'extract_card({kaart=})')
        speler.selected_card = kaart
        na_selectie()

    def niet_toegestaan(kaart:Card):
        window.add_label(f"Het spelen van {kaart} is niet toegestaan.", x_pos=Window.width*0.5, y_pos=Window.height*0.71)

    def niet_toepen():
        if Player.toeper == 'automatisch':
            bericht = "Er wordt al automatisch getoept."
        elif speler.name == Player.toeper:
            bericht = "Je kan jezelf niet overtoepen."
        bericht = f"Je mag nu niet toepen. {bericht}"
        window.add_label(bericht, x_pos=Window.width*0.5, y_pos=Window.height*0.8)

    # Create an instance of tkinter window
    window = Window(root,'Kies een kaart')
    window.add_label(bericht, x_pos=Window.width*0.5, y_pos=Window.height*0.17)
    #Discardpile weergeven
    window.add_cards(pile,"Gespeelde kaarten", Window.width*0.5, Window.height*0.3, players=True)
    #Kaarten plaatsen
    window.add_cards(speler,"Handkaarten:", Window.width*0.5, Window.height*0.6, functie=extract_card, functie2=niet_toegestaan, valid=valid)

    if speler.name != Player.toeper and Player.toeper != 'automatisch':
        toep_functie = lambda: extract_card(Card())
    else:
        toep_functie = niet_toepen

    window.add_button(window.window, "Toep!", Window.width*0.5, Window.height*0.755, toep_functie)


def speel_slag(root, na_slag):
    # print('uitvoeren: speel_slag()')
    pile = Player('Pile')
    turncounter = -1
    spelers = cycle(Player.players)

    def next_turn():
        # print('speel_slag: next_turn()')
        nonlocal turncounter
        turncounter += 1
        # print(f'{turncounter=}')
        #Spelers die nog meedoen bepalen na automatische toep, en stoppen als dit niemand is.
        actief = [speler for speler in Player.players if speler.rondescore != 0]
        actief_naam = [speler.name for speler in actief]
        if len(actief) == 1 or turncounter == len(Player.players):
            na_slag(root, pile, actief_naam)
            return

        speler = next(spelers)
        if speler.name in actief_naam:
            bevestigen(root, lambda: playerTurn(speler), speler)
        else:
            next_turn()

    def playerTurn(speler, getoept=False):
        # print(f'speel_slag: playerTurn({getoept})')
        #Bepaal of er kleur moet worden bekend
        suit, bericht = bekennen(speler, pile)
        valid_cards = [card for card in speler.cards if card.suit == suit or suit == '']

        if getoept:
            actief = [speler for speler in Player.players if speler.rondescore != 0]
            if len(actief) == 1:
                actief_naam = [speler.name for speler in actief]
                na_slag(root, pile, actief_naam)
                return
            else:
                speler.add_rondescore()

        # print(Player.players[id_])
        def vervolg_na_keuze():
            # print('vervolg_na_keuze')
            # print(f'{Player.players[id_].selected_card=}')
            if speler.selected_card.suit == "0":
                Player.toeper = speler.name
                toep_ronde(root, speler, lambda: bevestigen(root, lambda: playerTurn(speler, True), speler))
                return
            else:
                speler.play_card(speler.selected_card, pile)
                next_turn()
    
        choose_card(root, speler, pile, valid_cards, bericht, vervolg_na_keuze)

    #Eerste beurt van de slag instantieren
    next_turn()


def toep_ronde(root, toeper, na_toepronde, auto=False, toepers=[]):
    # print(f'uitvoeren: toep_ronde({toeper_id=})')

    toep_spelers = cycle(next_starter(Player.players, toeper))
    next(toep_spelers)

    def next_player():
        # print('toep_ronde: next_player()')
        speler = next(toep_spelers)
        print(speler, toeper)
        if speler == toeper:
            na_toepronde()
            return
        if speler.name in toepers or speler.rondescore == 0:
            next_player()
            return
        bevestigen(root, lambda: wil_mee(speler), speler)

    def wil_mee(speler):
        # print('toep_ronde: wil_mee()')
        if not auto:
            toep_bericht = f"{Player.toeper} heeft getoept."
        else:
            toep_bericht = f"{' en '.join(toepers)} {'toept' if len(toepers) == 1 else 'toepen'} automatisch."  
        ja_nee_vraag(root, speler, "Ga je mee?", toep_bericht, 'toepen', next_player, next_player)

    next_player()


def speel_ronde(root, eindscore, na_speelronde):
    # print('uitvoeren: speel_ronde()')

    def next_slag(boerenfinish=False):
        # print('speel_ronde: next_slag()')
        actief = [speler for speler in Player.players if speler.rondescore != 0]
        if len(actief) == 1 or len(actief[0].cards) == 0:
            for index, speler in enumerate(Player.players):
                if index != 0:
                    speler.add_score()
                elif boerenfinish:
                    speler.score -= 1
            ronde_uitslag(root, boerenfinish, na_speelronde)
            return
        
        speel_slag(root, slag_afhandelen)

    def slag_afhandelen(root, pile, actieve_spelers):
        # print('speel_ronde: slag_afhandelen()')
        #winaar bepalen en tonen
        if len(actieve_spelers) > 1:
            suit = pile.top_card().suit
            card_order = {'Boer': 1, 'Vrouw': 2, 'Heer': 3, 'Aas': 4, '7': 5, '8': 6, '9': 7, '10': 8}
            try:
                winnende_kaart = max((card for card in pile.cards if card.suit == suit and card.player in actieve_spelers),
                            key=lambda x: card_order[x.rank])
            except ValueError:
                winnende_kaart = max((card for card in pile.cards if card.player in actieve_spelers),
                            key=lambda x: card_order[x.rank])

            winnaar = winnende_kaart.player
            boerenfinish = winnende_kaart.rank == 'Boer'
        else:
            winnaar = actieve_spelers[0]
            boerenfinish = False
            winnende_kaart = None

        #windex aanpassen naar de winnaar van de slag
        Player.players = next_starter(Player.players, next(speler for speler in Player.players if speler.name == winnaar))
        slag_uitslag(root, lambda: next_slag(boerenfinish), pile, winnende_kaart)

    Player.toeper = ''
    toepers = []
    for speler in Player.players:
        if speler.score == eindscore-1:
            toepers.append(speler.name)
            Player.players = next_starter(Player.players, speler)
    # print(f'{toepers=}')
    #Als er mensen automatisch toepen wordt dit uitgevoerd.
    if toepers:
        Player.toeper = 'automatisch'
        toep_ronde(root, Player.players[0], next_slag, auto=True, toepers=toepers)
        return
    #Eerste slag van de ronde instantieren
    next_slag()

#Window
def slag_uitslag(root, functie, pile, winnende_kaart=None):
    # print('slag_uitslag')
    window = Window(root, 'Slag uitslag')
    window.add_cards(pile, "Gespeelde kaarten:", Window.width*0.5, Window.height*0.4, players=True)
    if winnende_kaart:
        window.add_label(f'\nDe slag is gewonnen door {winnende_kaart.player} met een {winnende_kaart}.', x_pos=Window.width*0.5, y_pos=600)
    else:
        window.add_label(f'\nDe slag is gewonnen door {Player.players[0].name}, er zijn geen andere spelers over.', x_pos=Window.width*0.5, y_pos=600)
    #Start en stopknoppen
    window.add_confirm(functie, Window.width*0.5, Window.height*0.8)

#Window
def ronde_uitslag(root, boerenfinish, functie):
    window = Window(root, 'Ronde uitslag')
    frame_score = window.add_frame(x_pos=Window.width*0.5, y_pos=Window.height*0.4)
    img_bg = PhotoImage(Image.open(Card.bg_loc).resize(Card.imagesize))
    window.images.append(img_bg)
    # Create a Label Widget to display the text or Image
    window.add_image(frame_score, img_bg, 0, 0)
    window.add_label(f"\nDe ronde is gewonnen door {Player.players[0].name}. \n{'Met een boerenfinish!' if boerenfinish else ''}", frame_score, 0, 1, grid=True)
    #Start en stopknoppen
    window.add_confirm(functie, Window.width*0.5, Window.height*0.8)

#Window
def tussenstand(root, callback):
    winner = False
    window = Window(root, 'Tussenstand')
    # frame_score = window.add_frame(x_pos=Window.width*0.5, y_pos=300)
    img_bg = PhotoImage(Image.open(Card.bg_loc).resize(Card.imagesize))
    window.images.append(img_bg)
    # Create a Label Widget to display the text or Image
    window.add_image(window.window, img_bg, x_pos=Window.width*0.5, y_pos=Window.height*0.3, grid=False)

    if len(Player.players) == 1:
        window.add_label(f'Gefeliciteerd {Player.players[0].name}, je bent de winnaar!\nBedankt voor het spelen!', x_pos=Window.width*0.5, y_pos=450)
        winner = True
    #Tekst toevoegen
    if Player.players:
        frame_standing = window.add_frame(x_pos=Window.width*0.5,y_pos=Window.height*0.55)
        window.add_label(f"{'Eindstand' if winner else 'Tussenstand'}", frame_standing, 0, 0, grid=True, columnspan=2)
        for id_, speler in enumerate(Player.players,1):
            window.add_label(f'{speler.name}', frame_standing, 0, id_, grid=True)
            window.add_label(f'{speler.score}', frame_standing, 1, id_, grid=True)
    else:
        window.add_label('Helaas, er zijn geen winnaars.\nBedankt voor het spelen!', x_pos=Window.width*0.5, y_pos=Window.height*0.15)

    if Player.losers:
        frame_losers = window.add_frame(x_pos=Window.width*0.5, y_pos=Window.height*0.68)
        window.add_label(f"Helaas, {'jullie zijn' if len(Player.losers) > 1 else 'je bent'} uitgeschakeld", frame_losers, 0, 0, grid=True, columnspan=2)
        for id_, speler in enumerate(Player.losers,1):
            window.add_label(f'{speler.name}', frame_losers, 0, id_, grid=True)
            window.add_label(f'{speler.score}', frame_losers, 1, id_, grid=True)
    
    #Start en stopknoppen
    window.add_confirm(callback, Window.width*0.5, Window.height*0.8)


def spel_spelen(root):
    eindscore = Player.aantal

    def next_round():
        deck = create_hands()
        was_ronde(root, deck, speelronde)
  
    #Check voor winnaar
    def check_winner():
        Player.losers += [speler for speler in Player.players if speler.score >= eindscore]
        Player.players = [speler for speler in Player.players if speler.score < eindscore]
        return len(Player.players) <= 1
    
    def speelronde():
        if check_winner():
            tussenstand(root, lambda: menu("\nWil je nog een potje spelen?", "Opnieuw", root))
            return
        #Ronde spelen
        speel_ronde(root, eindscore, ronde_afhandelen)

    def ronde_afhandelen():
        if check_winner():
            tussenstand(root, lambda: menu("\nWil je nog een potje spelen?", "Opnieuw", root))
            return
        #Tussenstand weergeven tussen rondes
        tussenstand(root, next_round)

    #Start eerste beurt
    next_round()

#Window
def menu(tekst:str, knoptekst:str, root:Tk):
    # Create an instance of tkinter window
    window = Window(root,'Start')
    #Plaatjes toevoegen
    frame_menu = window.add_frame(x_pos=Window.width*0.5, y_pos=Window.height*0.45)
    img_bg = PhotoImage(Image.open(Card.bg_loc).resize(Card.imagesize))
    window.images.append(img_bg)
    # Create a Label Widget to display the text or Image
    window.add_image(frame_menu, img_bg, 0,0, grid=True)
    window.add_label(tekst, frame_menu, 0, 1, grid=True)
    #Start en stopknoppen
    window.add_button(window.window, knoptekst, Window.width*0.5, Window.height*0.6, lambda: kiesmenu_aantal(root, 'spelers (2-4)', kiesmenu_spelers))
    window.add_button(window.window, "Instructies", Window.width*0.5, Window.height*0.65, lambda: instructies(root))
    window.add_button(window.window, "Sluit spel", Window.width*0.5, Window.height*0.7, exit)

#Window
def instructies(root:Tk):
    window = Window(root,'Instructies')
    #Tekst om op het scherm te plaatsen
    instructietekst = "Klik op de kaarten om deze te spelen,\ntoep als je denkt te kunnen winnen."
    #Tekst toevoegen
    window.add_label(instructietekst, x_pos=Window.width*0.5, y_pos=Window.height*0.4)
    #Knop toevoegen die terug gaat naar het hoofdmenu
    window.add_button(window.window, "Terug", x_pos=Window.width*0.5, y_pos=Window.height*0.65, functie=lambda: menu("\nWil je een potje spelen?", "Start", root))


#Root
def main():
    root = Tk()
    # root.title('Toepen')
    Window.width = root.winfo_screenwidth()
    Window.height = root.winfo_screenheight()
    root.attributes('-fullscreen', True)
    # root.geometry(f'{Window.width}x{Window.height}+0+0')
    # root.resizable(width=False, height=False)
    # root.minsize(Window.width,Window.height)
    # root.maxsize(Window.width,Window.height)    
    root.configure(background=Window.bg_color)
    menu("\nWil je een potje spelen?", "Start", root=root)
    root.mainloop()

if __name__ == '__main__':
    main()




