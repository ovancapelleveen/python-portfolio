import tkinter as tk
import os
from PIL import ImageTk, Image
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

    def __init__(self, suit: str, rank: str):
        """Initialisatie van speelkaart met kleur en rang."""
        self.suit = suit
        self.rank = rank
        self.order = Card.values[rank]
        self.player = ''
        self.image_loc = f'{Card.image_folder}\\{suit}_10.png'
        self.img = Image.open(self.image_loc).resize((121,150))

    # def display(self, id):
    #     """Voor het printen van kaarten met een id."""
    #     print('{:<4} {:<8} {:<1}'.format(f'{id}:', self.suit, self.rank))

    def __repr__(self):
        """Voor het printen van kaarten."""
        return f'{self.suit} {self.rank} van {self.player}'
    

class Player:
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
        deck.draw(self, 2)

    def add_inzet(self, num):
        """Inzet verhogen."""
        if num > self.geld:
            self.inzet += self.geld
            self.geld = 0
        else:
            self.inzet += num
            self.geld -= num

    def bevestigen(self):
        """Speler laten bevestigen voor de kaarten worden getoond."""
        window = Window('Bevestigen')

        window.add_frame(window.frame_top, 950,450)
        img_bg = ImageTk.PhotoImage(Image.open(Card.bg_loc).resize((120,150)))
        window.images.append(img_bg)
        # Create a Label Widget to display the text or Image
        lbl_card = tk.Label(master=window.frame_top, image=img_bg)
        lbl_card.grid(row=0, column=0)
        window.add_label(f'\nHet is nu de beurt van {self.name}.\nBevestig dat jij deze speler bent.', window.frame_top, 0, 1, grid=True, font=('calibri',15,'normal'))

        #Start en stopknoppen
        window.add_confirm(window.close, 950, 650)

        window.run()
    
    def __repr__(self):
        """Voor het printen van een speler."""   
        return f'{self.name} met {self.inzet} inzet en {self.geld} geld'
#Einde class Player==============================================================================================


class Window():
    """Representatie van een speelscherm."""
    bg_color = 'pink'
    fg_color = 'black'

    def __init__(self, naam=None):
        """Initialisatie van het scherm."""
        self.window = tk.Tk()
        self.naam = naam
        self.window.title("Poker")
        self.window.geometry('1900x1000+0+0')
        self.window.minsize(1900,1000)
        self.window.maxsize(1900,1000)
        self.window.configure(background=Window.bg_color)
        self.frame_top, self.frame_bot, self.frame_text, self.frame_confirm, self.frame_inzet, self.frame_extra = [tk.Frame(self.window, relief=tk.FLAT, bd=5, bg=Window.bg_color) for _ in range(6)]
        self.frame1_t, self.frame2_t, self.frame3_t, self.frame4_t, = [tk.Frame(self.frame_top, relief=tk.FLAT, bd=5, bg=Window.bg_color) for _ in range(4)]
        self.frame1, self.frame2, self.frame3, self.frame4, = [tk.Frame(self.window, relief=tk.FLAT, bd=5, bg=Window.bg_color) for _ in range(4)]
        if naam != 'Start':
            #Sluit knop altijd toevoegen als het niet het startscherm is.
            button = tk.Button(master=self.window, text=f"Sluit spel", borderwidth=5, command=exit)
            self.place_button(button, 1850, 40)
        #Bewaar plaatjes van kaarten om te laten zien
        self.images = []
        self.window.focus_force()
    
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

    def add_frame(self, frame, x_pos= None, y_pos=None, grid=False, anchor_=tk.CENTER, **kwargs):
        """Frame toevoegen aan het scherm."""
        padx = None if 'padx' not in kwargs else kwargs['padx']
        pady = None if 'pady' not in kwargs else kwargs['pady']
        if grid:
            frame.grid(column=x_pos, row=y_pos, sticky="nsew",padx=padx, pady=pady)
        elif x_pos and y_pos:
            frame.place(x=x_pos, y=y_pos, anchor=anchor_,padx=padx, pady=pady)
        else:
            frame.pack(padx=padx, pady=pady)

    def add_label(self, text, frame=None, x_pos=None, y_pos=None, **kwargs):
        """Label toevoegen aan een frame."""
        if text:
            if not frame:
                frame = self.window
            label = tk.Label(master=frame, text=text, bg=Window.bg_color, fg=Window.fg_color)
            for key, value in kwargs.items():
                try:
                    label[key] = value
                except Exception:
                    pass
            self.add_frame(label, x_pos, y_pos, **kwargs)

    def add_image(self, frame, image_, num):
        """Afbeelding toevoegen aan het frame."""
        return tk.Label(master=frame, image=image_, bg=Window.bg_color).grid(row=0, column=num)
    def add_cards(self, speler, frame, label, x_pos=None, y_pos=None, anchor=tk.CENTER, grid=False):
        """Kaarten van een speler toevoegen aan een frame."""
        if speler and speler.cards:
            self.add_frame(frame, x_pos, y_pos, anchor_=anchor, grid=grid)
            frame["bg"]=Window.bg_color
            tk.Label(master=frame, text=label, bg=Window.bg_color, fg=Window.fg_color,font=('calibre',10,'bold')).grid(row=1, column=0, columnspan=speler.size)
            for id_, kaart in enumerate(speler.cards):
                # Create an object of tkinter ImageTk
                img = ImageTk.PhotoImage(kaart.img)
                self.images.append(img)
                self.add_image(frame, img, id_)

    def add_card_canvas(self,speler, label, x_pos=None, y_pos=None):
            #Tafel weergeven
        canvas = tk.Canvas(self.window,bg=Window.bg_color,highlightthickness=0,height=450, width=1000)
        self.add_frame(canvas, x_pos, y_pos)

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
                img = ImageTk.PhotoImage(kaart.img)
                self.images.append(img)
                image = tk.Label(master=canvas, image=img, bg="brown")
                canvas.create_window(id_*150+200, 230, window=image)

    def add_inzet(self, spelers):
        """Inzet-frame toevoegen aan window."""

        def sort_order(input):
            """Sorteer volgorde van de kaarten vaststellen."""
            return input.geld
    
        self.add_frame(self.frame_extra, 200, 200)
        self.frame_extra["bg"] = "black"
        # self.frame_extra["bd"] = 0

        #Maak een kopie zodat de volgorde niet wijzigd.
        spelers = spelers.copy()
        spelers.sort(key=sort_order, reverse=True)

        self.add_label('-', self.frame_extra, x_pos=0, y_pos=0, grid=True, font=('calibre',10,'bold'), fg=Window.bg_color, width=12)
        self.add_label('Inzet', self.frame_extra, x_pos=1, y_pos=0, grid=True, font=('calibre',10,'bold'), padx=(0,1), width=12)
        self.add_label('Huidige\nmonies', self.frame_extra, x_pos=2, y_pos=0, grid=True, font=('calibre',10,'bold'), width=12)
        for i, speler in enumerate(spelers,1):
            self.add_label(f"{speler.name}", self.frame_extra, x_pos=0, y_pos=i, grid=True, font=('calibre',10,'bold'), padx=(0,1), pady=(1,0), height=3)
            self.add_label(f"{speler.inzet}", self.frame_extra, x_pos=1, y_pos=i, grid=True, font=('calibre',10,'bold'), padx=(0,1), pady=(1,0))
            self.add_label(f"{speler.geld}", self.frame_extra, x_pos=2, y_pos=i, grid=True, font=('calibre',10,'bold'), pady=(1,0))

    def add_confirm(self, functie, x_pos, y_pos):
        """Bevestigknop toevoegen."""
        button = tk.Button(master=self.window, text=f"Bevestigen", borderwidth=5, width=10, height=2, command=functie)
        self.place_button(button, x_pos, y_pos)
        self.window.bind('<Return>', lambda event: functie())

    def place_button(self,button, x_pos, y_pos, grid=False, enter_relief=tk.SUNKEN, leave_relief=tk.RAISED, enter_color=None, leave_color=None):
        button['relief'] = leave_relief
        self.add_frame(button, x_pos, y_pos, grid)
        # button.place(x=x_pos,y=y_pos,anchor=tk.CENTER)
        button.bind("<Enter>", lambda event, button=button, relief=enter_relief, color=enter_color: self.on_enter(button, relief, color))
        button.bind("<Leave>", lambda event, button=button, relief=leave_relief, color=leave_color: self.on_leave(button, relief, color))

    def close(self):
        """Sluit window."""
        self.window.destroy()

    def run(self):
        """Draai window."""
        self.window.mainloop()
####################################################


if __name__ == '__main__':
    print('Dit is het verkeerde bestand!')