import tkinter as tk
from tkinter import Frame, Button, Label, Canvas
import os
from PIL import ImageTk, Image
from PIL.ImageTk import PhotoImage
from random import shuffle
from sys import exit

class Card:
    """Representatie van een enkele speelkaart."""
    suits = ['Harten', 'Schoppen', 'Ruiten', 'Klaveren']
    values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Boer':11, 'Vrouw':12, 'Heer':13, 'Aas':14}
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_folder = os.path.join(BASE_DIR, "Speelkaarten")
    # image_folder = f'.\\Speelkaarten'
    bg_loc = os.path.join(image_folder, 'achterkant.png')
    # bg_loc = f'{image_folder}\\bg_red.png'
    imagesize = (121,150)

    def __init__(self, suit: str, rank: str):
        """Initialisatie van speelkaart met kleur en rang."""
        self.suit = suit
        self.rank = rank
        self.order = Card.values[rank]
        self.player = ''
        self.image_loc = f'{Card.image_folder}\\{suit}_{rank}.png'
        self.img = Image.open(self.image_loc).resize((121,150))

    # def display(self, id):
    #     """Voor het printen van kaarten met een id."""
    #     print('{:<4} {:<8} {:<1}'.format(f'{id}:', self.suit, self.rank))

    def __repr__(self):
        """Voor het printen van kaarten."""
        return f'{self.suit} {self.rank} van {self.player}'
    
class Player:
    aantal = 0
    players = []
    losers = []

    """Representatie van een collectie van kaarten."""
    def __init__(self, name: str, deck: bool=False):
        """Initialisatie van de speler."""
        self.name = name 
        self.geld = 1000
        self.inzet = 0
        self.fold = False
        self.result = 0
        if deck:
             self.cards = [Card(suit, rank) for suit in Card.suits for rank in Card.values]
        else:
            self.cards = []
        self.size = 0
        self.rondekaarten = []
        self.rondescore = 0.
        self.rondewinst = 0
        self.rondehand = ''
        self.blind = ''

    def add_card(self, card):
        """Specifieke kaart toevoegen aan collectie."""
        self.cards.append(card)
        self.size += 1

    def remove_card(self, card):
        """Specifieke kaart verwijderen uit collectie."""
        if card in self.cards:
            self.cards.remove(card)
            self.size -= 1
        else:
            raise ValueError(f"The card {card} is not in {self.name}.")

    def draw(self,target_deck, num):
        """Trek een aantal willekeurige kaarten naar target_deck."""
        self.shuffle_deck()
        self.move_cards(target_deck, num)

    def move_cards(self, target, num):
        """Beweeg kaarten tussen collecties."""
        for _ in range(num):
            drawn_card = self.cards.pop(0)  # Take the top card (or first card in the list)
            drawn_card.player = target.name
            self.size -= 1 
            target.add_card(drawn_card)

    def shuffle_deck(self):
        """Schud het deck."""
        shuffle(self.cards)

    # def top_card(self):
    #     """Laat de bovenste kaart van de stapel zien."""
    #     if self.cards:
    #         return self.cards[0]
    #     return None

    # def play_card(self, card, target):
    #     """Speel een specifieke kaart naar target."""
    #     self.remove_card(card)  # Remove from hand
    #     target.add_card(card)  # Add to discard pile
    #     card.player = self.name

    def setup(self, deck):
        """Hand vernieuwen voor de start van de volgende ronde."""
        self.cards = []
        self.size = 0
        self.fold = False
        self.rondekaarten = []
        self.rondescore = 0
        self.rondewinst = 0
        self.rondehand = ''
        self.blind = ''
        deck.draw(self, 2)

    def add_inzet(self, num):
        """Inzet verhogen."""
        if num > self.geld:
            self.inzet += self.geld
            self.geld = 0
        else:
            self.inzet += num
            self.geld -= num
    
    def __repr__(self):
        """Voor het printen van een speler."""   
        return f'{self.name} met {self.inzet} inzet en {self.geld} geld'
#Einde class Player==============================================================================================


class Window():
    """Representatie van een speelscherm."""
    bg_color = 'pink'
    fg_color = 'black'
    width = 0
    height = 0

    def __init__(self, parent, naam=None):
        self.window = parent
        self.naam = naam
        self.window.title(naam)
        self.images = []
        #Root leegmaken bij volgende aanroep
        for widget in parent.winfo_children():
            widget.destroy()

        self.window.bind('<Escape>', exit)

    def on_enter(self, button, relief=tk.SUNKEN, color=None):
        """Verander relief van een knop als de cursor erover hovered."""
        button['relief'] = relief
        if color:
            button['color'] = color
    def on_leave(self, button, relief=tk.RAISED, color=None):
        """Verander relief van een knop als de cursor erover hovered."""
        button['relief'] = relief
        if color:
            button['color'] = color

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

    #Tekst-bericht toevoegen
    def add_text(self, text, frame=None, x_pos=None, y_pos=None, **kwargs):
        """Label toevoegen aan een frame."""
        if text:
            if not frame:
                frame = self.window
            label = Label(master=frame, text=text, bg=Window.bg_color, fg=Window.fg_color, font=('calibre',10,'normal'))
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

    def add_cards(self, speler, label, master=None, x_pos=None, y_pos=None, anchor=tk.CENTER, grid=False):
        """Kaarten van een speler toevoegen aan een frame."""
        if speler and speler.cards:
            frame_cards = self.add_frame(master=master, x_pos=x_pos, y_pos=y_pos, anchor_=anchor, grid=grid)
            self.add_text(label, frame_cards, 0, 1, grid=True, columnspan=speler.size)
            for id_, kaart in enumerate(speler.cards):
                # Create an object of tkinter ImageTk
                img = PhotoImage(kaart.img)
                self.images.append(img)
                self.add_image(frame_cards, img, id_, 0, padx=5)

    def add_card_canvas(self, speler, label='', x_pos=None, y_pos=None):
            #Tafel weergeven
        canvas = Canvas(self.window,bg=Window.bg_color,highlightthickness=0,height=450, width=1000)
        self.place_widget(canvas, x_pos, y_pos)

        #Tafel weergeven
        canvas.create_oval(0, 0, 450,450,fill="brown")
        canvas.create_oval(550, 0, 1000,450,fill="brown")
        canvas.create_polygon(225,0,775,0,775,450,225,450, fill="brown")
    
        #Kaarten op tafel weergeven.
        if speler and speler.cards:
            # label = tk.Label(master=canvas, text=label, bg="brown", fg=Window.fg_color)
            # canvas.create_window(500,130, window=label)
            for id_, kaart in enumerate(speler.cards):
                # Create an object of tkinter ImageTk
                img = PhotoImage(kaart.img)
                self.images.append(img)
                image = Label(master=canvas, image=img, bg="brown")
                canvas.create_window(id_*150+200, 230, window=image)

    def add_inzet(self, spelers):
        """Inzet-frame toevoegen aan window."""

        def sort_order(input):
            """Sorteer volgorde van de kaarten vaststellen."""
            return input.geld
        frame_stand = self.add_frame(x_pos=200, y_pos=200)
        frame_stand["bg"] = "black"
        # frame_stand["bd"] = 0

        #Maak een kopie zodat de volgorde niet wijzigd.
        spelers = spelers.copy()
        spelers.sort(key=sort_order, reverse=True)

        self.add_text('-', frame_stand, x_pos=0, y_pos=0, grid=True, font=('calibre',10,'bold'), fg=Window.bg_color, width=12)
        self.add_text('Inzet', frame_stand, x_pos=1, y_pos=0, grid=True, font=('calibre',10,'bold'), padx=(0,1), width=12)
        self.add_text('Huidige\nmonies', frame_stand, x_pos=2, y_pos=0, grid=True, font=('calibre',10,'bold'), width=12)
        for i, speler in enumerate(spelers,1):
            self.add_text(f"{speler.name}", frame_stand, x_pos=0, y_pos=i, grid=True, font=('calibre',10,'bold'), padx=(0,1), pady=(1,0), height=3)
            self.add_text(f"{speler.inzet}", frame_stand, x_pos=1, y_pos=i, grid=True, font=('calibre',10,'bold'), padx=(0,1), pady=(1,0))
            self.add_text(f"{speler.geld}", frame_stand, x_pos=2, y_pos=i, grid=True, font=('calibre',10,'bold'), pady=(1,0))

    def add_confirm(self, functie, x_pos, y_pos):
        """Bevestigknop toevoegen."""
        button = tk.Button(master=self.window, text=f"Bevestigen", borderwidth=5, width=10, height=2, command=functie)
        self.place_button(button, x_pos, y_pos)
        self.window.bind('<Return>', lambda event: functie())

    def add_button(self, frame, tekst, x_pos, y_pos, functie, borderwidth=5, width=10, height=2, grid=False):
        """Knop plaatsen."""
        btn = Button(master=frame, text=tekst, borderwidth=borderwidth, width=width, height=height, bg=Window.fg_color, fg=Window.bg_color, command = functie)
        self.place_button(btn, x_pos, y_pos, grid)
        return btn

    def place_button(self, button, x_pos=None, y_pos=None, grid=False, enter_relief=tk.SUNKEN, leave_relief=tk.RAISED, enter_color=None, leave_color=None, **kwargs):
        button['relief'] = leave_relief
        self.place_widget(button, x_pos, y_pos, grid, **kwargs)
        button.bind("<Enter>", lambda event: self.on_enter(button, enter_relief, enter_color))
        button.bind("<Leave>", lambda event: self.on_leave(button, leave_relief, leave_color))


    def close(self):
        """Sluit window."""
        self.window.destroy()

    def run(self):
        """Draai window."""
        self.window.mainloop()
####################################################


if __name__ == '__main__':
    print('Dit is het verkeerde bestand!')