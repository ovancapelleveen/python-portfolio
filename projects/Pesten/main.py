import tkinter as tk
from tkinter import Button, Label, Frame, Tk
import os

from PIL import Image #, ImageTk
from PIL.ImageTk import PhotoImage
from random import choice, shuffle
from sys import exit


class Card:
    """Represents a single playing card."""
    suits = ['Harten', 'Schoppen', 'Ruiten', 'Klaveren']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Boer', 'Vrouw', 'Heer', 'Aas']
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_folder = os.path.join(BASE_DIR, "Speelkaarten")
    bg_loc = os.path.join(image_folder, 'achterkant.png')
    imagesize = (121,150)

    def __init__(self, suit:str="0", value:str="0", type:str="0"):
        self.suit = suit
        self.value = value
        self.type = type
        if value == "0":
            self.image_loc = Card.bg_loc
        else:
            self.image_loc = f'{Card.image_folder}\\{suit}_{value}.png'
        self.img = Image.open(self.image_loc).resize(Card.imagesize)

    def __repr__(self):
        if self.value == 'Joker':
            return f'{self.value}'
        elif self.value == "0":
            if self.type == 'Boer':
                return f'{self.suit} of een {self.type}'
            else:
                return f'{self.suit}'
        else:      
            return f'{self.suit} {self.value}'

    def check_card(self, topcard, pakken=0):
        if pakken == 0:
            return self.suit == topcard.suit or self.value in (topcard.type, 'Joker')
        else:
            return self.value in (topcard.type, 'Joker') or (self.value == 2 and topcard.type == 'Joker')


class Collection:
    """Represents a deck of cards, which can be a main deck, a hand, or a discard pile."""
    
    def __init__(self, name:str):    
        self.name = name  # Give the deck a name for easier debugging
        if name == 'Main Deck':
            self.pakken = 0
            self.cards = [Card(suit, value, value) for suit in Card.suits for value in Card.values] + [Card(waarde, 'Joker', 'Joker') for waarde in ['0', '1']]
            self.shuffle_deck()
        else:
            self.cards = []  # List of cards in this deck
        self.size = len(self.cards)
        self.selected_card = Card()
        self.selcted_color = None
        self.gestraft = False

    def add_card(self, card:Card):
        """Adds a card to this deck."""
        self.cards.append(card)
        self.size += 1

    def remove_card(self, card:Card):
        """Removes a specific card from this deck."""
        if card in self.cards:
            self.cards.remove(card)
            self.size -= 1
        else:
            raise ValueError(f"The card {card} is not in {self.name}.")

    def draw(self, num_cards:int, target_deck, discard_pile = None):
        """Draws cards from this deck to another deck (like a hand).
           If not enough cards are available, reshuffle from discard pile.
        """
        if num_cards == 0:
            num_cards = 1

        if num_cards > len(self.cards):
            # If not enough cards, reshuffle the discard pile into the main deck
            self.reshuffle_from_discard(discard_pile)
        
        # Check again after reshuffling, raise error if still not enough cards
        if num_cards > len(self.cards):
            raise ValueError(f"Te weinig kaarten in {self.name} om {num_cards} kaarten te trekken.")
        
        for _ in range(num_cards):
            drawn_card = self.cards.pop(0)  # Take the top card (or first card in the list)
            target_deck.add_card(drawn_card)  # Add it to the target deck        

    def reshuffle_from_discard(self, discard_pile):
        """Moves all cards from the discard pile except the top one to this deck and shuffles."""
        if len(discard_pile.cards) > 1:
            # Take all cards from the discard pile except the top two
            reshuffle_cards = discard_pile.cards[:-2]
            self.cards.extend(reshuffle_cards)  # Add them to the main deck
            discard_pile.cards = discard_pile.cards[-2:]  # Leave only the two top cards (voor het geval de bovenste kaart een joker is)
            self.shuffle_deck()

    def shuffle_deck(self):
        """Shuffles the deck."""
        shuffle(self.cards)
    def top_card(self):
        """Returns the top card of the deck (for discard pile)."""
        return self.cards[-1]
    def top_card_color(self):
        """Returns the top card of the deck (for discard pile)."""
        return self.cards[-2]

    def play_card(self, card:Card, discard):
        """Plays a card from the hand to the discard pile, if allowed."""
        if discard.top_card().value == "0":
            discard.remove_card(discard.top_card())
        self.remove_card(card)  # Remove from hand
        discard.add_card(card)  # Add to discard pile
        self.gestraft = False
    
    def sort(self, func):
        self.cards.sort(key=func)

    # def __repr__(self):        
    #     return f'{self.name} with {len(self.cards)} cards: {self.cards}'

# ==================== SETTINGS ====================

class Window:
    """Representatie van een speelscherm."""
    bg_color = 'pink'
    fg_color = "#000000"
    width = 1900
    height = 1000

    def __init__(self, parent:Tk, naam=None):
        self.window = parent
        self.images = []
        #Root leegmaken bij volgende aanroep
        for widget in parent.winfo_children():
            widget.destroy()

    def on_enter(self, button:Button, relief=tk.SUNKEN, color=None, text=None):
        """Verander relief van een knop als de cursor erover hovered."""
        button['relief'] = relief
        if color:
            button['color'] = color
        if text:
            button['fg'] = Window.fg_color
    def on_leave(self, button:Button, relief=tk.RAISED, color=None, text=None):
        """Verander relief van een knop als de cursor erover hovered."""
        button['relief'] = relief
        if color:
            button['color'] = color
        if text:
            button['fg'] = Window.bg_color

    def add_frame(self, master=None, x_pos=None, y_pos=None, grid:bool=False, anchor_=tk.CENTER, **kwargs):
        """Frame toevoegen aan het scherm."""
        if not master:
            master = self.window
        frame = Frame(master, relief=tk.FLAT, bd=5, bg=Window.bg_color)
        self.place_widget(frame, x_pos, y_pos, grid, anchor_, **kwargs)
        return frame
    
    def add_image(self, frame:Frame|Tk, image_:PhotoImage, col, row, **kwargs):
        """Afbeelding toevoegen aan het frame."""
        image = Label(master=frame, image=image_, bg=Window.bg_color)
        self.place_widget(image, col, row, **kwargs)

    def add_btn_card(self, frame:Frame|Tk, image_:PhotoImage, tekst:str, col, row, functie_tuple:tuple, **kwargs):
        """Knop kaart toevoegen."""
        btn = Button(master=frame,text=tekst, image=image_, bg=Window.bg_color, fg=Window.fg_color, command=lambda var=functie_tuple[1]: functie_tuple[0](var), compound='top')
        self.place_button(btn,col,row, tekst=tekst, enter_relief=tk.FLAT, leave_relief=tk.FLAT,**kwargs)

    def place_widget(self, widget, x_pos=None, y_pos=None, grid=False, anchor_=tk.CENTER, **kwargs):
        """Frame toevoegen aan het scherm."""
        padx = None if 'padx' not in kwargs else kwargs['padx']
        pady = None if 'pady' not in kwargs else kwargs['pady']
        columnspan = None if 'columnspan' not in kwargs else kwargs['columnspan']
        if grid:
            widget.grid(column=x_pos, row=y_pos, sticky="nsew",padx=padx, pady=pady, columnspan=columnspan)
        elif x_pos and y_pos:
            widget.place(x=x_pos, y=y_pos, anchor=anchor_,padx=padx, pady=pady)
        else:
            widget.pack(padx=padx, pady=pady)

    def place_button(self,button:Button, x_pos=None, y_pos=None, grid:bool=False, tekst=None, enter_relief=tk.SUNKEN, leave_relief=tk.RAISED, enter_color=None, leave_color=None):
        button['relief'] = leave_relief
        if tekst:
            button['fg']=Window.bg_color
            button['activebackground']=Window.bg_color
        self.place_widget(button, x_pos, y_pos, grid)
        button.bind("<Enter>", lambda event: self.on_enter(button, enter_relief, enter_color, tekst))
        button.bind("<Leave>", lambda event: self.on_leave(button, leave_relief, leave_color, tekst))

    def add_label(self, text:str, frame=None, x_pos=None, y_pos=None, **kwargs):
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

    def add_discard(self,master:Frame|Tk, discard:Collection, x_pos, y_pos, btn:bool=False, pakken:int=0, functie=None): 
        frame_discard = self.add_frame(master,x_pos,y_pos)
        # Create an object of tkinter ImageTk
        if discard.top_card().value == "0":
            img_dc = PhotoImage(discard.top_card_color().img)
            if btn:
                self.add_label( f'De kleur is {discard.top_card().suit}',x_pos=Window.width/2,y_pos=100)
        else:
            img_dc = PhotoImage(discard.top_card().img)
        self.images.append(img_dc)
        imgbg = PhotoImage(Image.open(Card.bg_loc).resize(Card.imagesize))
        self.images.append(imgbg)

        #Aflegstapeltekst toevoegen
        self.add_label("Aflegstapel:",frame_discard,1, 0,grid=True)
        if btn:
            img_frame = self.add_frame(frame_discard,1,1,grid=True)
            self.add_image(img_frame, img_dc, 0, 0, grid=True)
            #Ontzichtbaar label om alignment te verbeteren
            self.add_label("-",img_frame,0,1,grid=True,fg=Window.bg_color, font=('calibre',6,'bold'))
            #Discardpile knop
            self.add_btn_card(frame_discard, imgbg, f"{f'Trek {pakken} kaarten' if pakken > 1 else 'Trek een kaart'}",0,1,(functie, Card()),grid=True)
        else:
            self.add_image(frame_discard, img_dc, 1, 1, grid=True)
            self.add_image(frame_discard, imgbg, 0, 1, grid=True)


    def add_cards(self, master:Frame|Tk, speler:Collection, label:str, x_pos=None, y_pos=None, functie=None, functie2=None, valid=None, anchor=tk.CENTER, grid:bool=False):
        """Kaarten van een speler toevoegen aan een frame."""
        if speler and speler.cards:
            frame_cards = self.add_frame(master,x_pos, y_pos, anchor_=anchor, grid=grid)
            #Kaarten toevoegen
            self.add_label(label,frame_cards,0,0,grid=True,columnspan=speler.size)
            for id_, kaart in enumerate(speler.cards):
                # Create an object of tkinter ImageTk
                if speler.name == "CPU":
                    img = PhotoImage(Image.open(Card.bg_loc).resize(Card.imagesize))
                    self.images.append(img)
                    self.add_image(frame_cards, img, id_%10, id_//10+1, grid=True)
                else:
                    img = PhotoImage(kaart.img)
                    self.images.append(img)
                    if not valid is None:
                        if kaart in valid:
                            self.add_btn_card(frame_cards, img, f"Speel {kaart}",  id_%10, id_//10+1,(functie,kaart), grid=True)
                        else:
                            self.add_btn_card(frame_cards, img, f"Speel {kaart}", id_%10, id_//10+1, (functie2, kaart), grid=True)
                    else:
                        self.add_image(frame_cards, img, id_%10, id_//10+1, grid=True)

    def add_colors(self, master:Frame|Tk, suits:list, x_pos, y_pos, functie):
        #Kleuropties toevoegen
        frame_color = self.add_frame(master,x_pos,y_pos)
        self.add_label("Kies een kleur:",frame_color,0,0,grid=True,columnspan=4)
        for id_, kleur in enumerate(suits):
            # Create an object of tkinter ImageTk
            btn = Button(master=frame_color, text=f"{kleur}", borderwidth=5, width=10, height=2, command=lambda kleur=kleur: functie(kleur))
            self.place_button(btn, id_, 1, grid=True)

    def add_confirm(self, master:Frame|Tk, functie, var, x_pos=None, y_pos=None):
        """Bevestigknop toevoegen."""
        button = Button(master=master, text=f"Bevestigen", borderwidth=5, width=10, height=2, command=lambda: functie(var))
        self.place_button(button, x_pos, y_pos)
        self.window.bind('<Return>', lambda event: functie(var))


# ==================== FUNCTIONS ====================
def initialize():
    """Represents the game mechanics with the main deck, hand, and discard pile."""
    main_deck = Collection("Main Deck")
    playerHand = Collection("Jij")
    computerHand = Collection("CPU")
    discard_pile = Collection("Discard Pile")

    #Initializeer discard_pile met 1 kaart en spelerhanden met 7
    main_deck.draw(7, playerHand)
    main_deck.draw(7, computerHand)
    main_deck.draw(1, discard_pile)

    return main_deck, playerHand, computerHand, discard_pile

def computerTurn(hand:Collection, opphand:Collection, valid:list, deck:Collection, discard:Collection, root:Tk, callback):
    if not valid:
        deck.draw(deck.pakken, hand, discard)
        if deck.pakken > 1:
            hand.gestraft = True
        else:
            hand.gestraft = False

        bericht = f'CPU trok {deck.pakken} kaarten!' if deck.pakken > 1 else 'CPU trok een kaart!'
        hand.selected_card = Card()
        deck.pakken = 0
    else:
        priority_mapping = {
            'Joker': 1,
            2: 4,
            7: 5,
            8: 5,
            'Heer': 5
            }

        max_priority = 0
        for card in valid:
            card_priority = priority_mapping.get(card.value, 2)
            # Check for specifieke conditie and stop loop als toepasbaar
            if opphand.size <= 3 and card.value == 'Joker':
                hand.selected_card = card
                break
            # Prioriteer kaarten met dezelfde kleur
            if card.suit == discard.top_card().suit:
                card_priority += 1

            if card_priority > max_priority:
                max_priority = card_priority
                hand.selected_card = card

        #Speel de kaart
        hand.play_card(hand.selected_card, discard)
        bericht = f'CPU speelde een {hand.selected_card}'

    comp_play(hand, discard, bericht, root, callback)


def comp_play(hand:Collection, discard:Collection, tekst:str, root:Tk, callback):
     # Create an instance of tkinter window
    window = Window(root, 'comp_play')
    #Actie van de computer weergeven
    window.add_label(tekst, window.window,x_pos=Window.width/2,y_pos=100)
    #Discardpile toevoegen
    window.add_discard(window.window,discard,Window.width/2,300)
    #Handkaarten CPU toevoegen
    window.add_cards(window.window, hand, "Handkaarten CPU:", Window.width/2, 600)
    #Bevestig knop toevoegen
    window.add_confirm(window.window, callback, hand, Window.width/2,800)

def menu(tekst:str, knoptekst:str, root:Tk):
    # Create an instance of tkinter window
    window = Window(root,'Start')
    #Plaatjes toevoegen
    frame_menu = window.add_frame(window.window,Window.width/2,450)
    img_bg = PhotoImage(Image.open(Card.bg_loc).resize(Card.imagesize))
    window.images.append(img_bg)
    # Create a Label Widget to display the text or Image
    window.add_image(frame_menu, img_bg, 0,0,grid=True)
    window.add_label(tekst, frame_menu, 0, 1,grid=True)

    #Start en stopknoppen
    btn_conf = Button(master=window.window, text=knoptekst, borderwidth=5, width=10, height=2, command = lambda: spel_spelen(root))
    btn_inst = Button(master=window.window, text="Instructies", borderwidth=5, width=10, height=2, command = lambda: instructies(root))
    btn_end = Button(master=window.window, text="Sluit spel", borderwidth=5, width=10, height=2, command = exit)
    window.place_button(btn_conf, Window.width/2,600)
    window.place_button(btn_inst, Window.width/2,650)
    window.place_button(btn_end,Window.width/2,700)

def instructies(root:Tk):
    window = Window(root,'Instructies')
    #Tekst om op het scherm te plaatsen
    instructietekst = "Klik op de kaarten om deze te spelen,\nklik op de discardpile om een kaart te trekken"
    #Tekst toevoegen
    window.add_label(instructietekst,window.window,x_pos=Window.width/2,y_pos=400)
    #Knop toevoegen die terug gaat naar het hoofdmenu
    btn_terug = Button(master=window.window, text="Terug", borderwidth=5, width=10, height=2, command = lambda: menu("\nWil je een potje spelen?", "Start", root))
    window.place_button(btn_terug, Window.width/2,650)


def playerTurn(hand:Collection, valid:list, deck:Collection, discard:Collection, root:Tk, callback):
    def vervolg_na_keuze():
        if hand.selected_card.type == "0":
            deck.draw(deck.pakken, hand, discard)
            hand.gestraft = deck.pakken > 1
            hand.selected_card = Card()
            deck.pakken = 0
        else:
            hand.play_card(hand.selected_card, discard)
        callback(hand)
        
    choose_card(hand, discard, valid, deck.pakken, root, vervolg_na_keuze)


def choose_card(hand:Collection, discard:Collection, valid:list, pakken:int, root:Tk, kaart_selectie):
    #Sorteer hand
    def sort_order(input:Card):
        return input.suit, input.value
    hand.sort(sort_order)

    def extract_card(kaart:Card):
        hand.selected_card = kaart
        kaart_selectie()

    def niet_toegestaan(kaart:Card):
        window.add_label(f"Het spelen van {kaart} is niet toegestaan.",window.window,Window.width/2,150)

    # Create an instance of tkinter window
    window = Window(root,'Kies een kaart')
    #Discardpile weergeven
    window.add_discard(window.window, discard,Window.width/2,300,btn=True,pakken=pakken,functie=extract_card)
    #Kaarten plaatsen
    window.add_cards(window.window,hand,"Handkaarten:",Window.width/2,600, functie=extract_card, functie2=niet_toegestaan, valid=valid)


def kleurkiezen(turn:str, hand:Collection, discard:Collection, deck:Collection, waarde, root:Tk, na_kleur):
    def extract_color(kleur):
        nonlocal discard, window
        discard.add_card(Card(kleur, "0", waarde))
        na_kleur()

    if waarde == 'Joker':
        deck.pakken += 5

    suits = ['Harten', 'Schoppen', 'Ruiten', 'Klaveren']
    if turn == 'player':
        suit_counts = {suit: sum(1 for card in hand.cards if card.suit == suit) for suit in suits}
        max_count = max(suit_counts.values())
        kleuren_met_max_count = [suit for suit, count in suit_counts.items() if count == max_count]
        selected_color = choice(kleuren_met_max_count) if max_count > 0 else choice(suits)
        discard.add_card(Card(selected_color, "0", waarde))
        na_kleur()
    
    elif turn == 'CPU':
        # Create an instance of tkinter window
        window = Window(root, 'Kies een kleur')
        window.add_label('Dit is het kleurkiezenscherm',window.window,Window.width/2,150)
        #Discardpile toevoegen
        window.add_discard(window.window,discard, Window.width/2,300)
        #Kaarten toevoegen
        window.add_cards(window.window,hand,"Handkaarten:",Window.width/2,600)
        #Kleuropties toevoegen
        window.add_colors(window.window, suits,Window.width/2,800,extract_color)


def spel_spelen(root:Tk):

    main_deck, playerHand, computerHand, discard_pile = initialize()
    turn = 'player'
    winner = False

    # Zorg dat er geen speciale kaart boven ligt voor de start
    while discard_pile.top_card().value in ['2', '7', '8', 'Heer', 'Joker']:
        main_deck.draw(1, discard_pile)

    def next_turn():
        nonlocal turn, winner
        currentHand, opponentHand = (playerHand, computerHand) if turn == 'player' else (computerHand, playerHand)
        valid_cards = [card for card in currentHand.cards if card.check_card(discard_pile.top_card(), main_deck.pakken)]

        if check_winner(opponentHand):
            end_game(opponentHand, currentHand)
            return
        
        if turn == 'player':
            playerTurn(playerHand, valid_cards, main_deck, discard_pile, root, handle_special_cards)
        else:
            computerTurn(computerHand, playerHand, valid_cards, main_deck, discard_pile, root, handle_special_cards)

    def handle_special_cards(hand:Collection):
        nonlocal turn
        card = hand.selected_card
        if hand.gestraft or card.value in ['7', '8', 'Heer']:
            next_turn()
            return
        if card.value in ['Boer', 'Joker']:
            turn = 'player' if turn == 'CPU' else 'CPU'
            kleurkiezen(turn, hand, discard_pile, main_deck, card.value, root, next_turn)
            return
        if card.value == '2':
            main_deck.pakken += 2
        turn = 'player' if turn == 'CPU' else 'CPU'
        next_turn()

    def check_winner(current:Collection):
        if current.size == 0:
            if current.selected_card.value in ['2', '7', '8', 'Heer', 'Joker']:
                main_deck.draw(2, current, discard_pile)
                return False
            return True
        return False

    def end_game(winner_hand, loser_hand):
        if winner_hand.name == 'CPU':
            bericht = ['\nHelaas, CPU was je te snel af!']
        else:
            bericht = ['\nGefeliciteerd!! Jij bent de winnaar!!']

        aantal = loser_hand.size
        bericht.append(f'{loser_hand.name} had nog {aantal} kaart{"en" if aantal != 1 else ""} over.')
        bericht.append('\nBedankt voor het spelen')
        menu('\n'.join(bericht), "Opnieuw", root)
    # Start eerste beurt
    next_turn()

def main():
    root = Tk()
    root.geometry(f'{Window.width}x{Window.height}+0+0')
    root.configure(background=Window.bg_color)
    root.title('Pesten')
    menu("\nWil je een potje spelen?", "Start", root=root)
    root.mainloop()

if __name__ == '__main__':
    main()
