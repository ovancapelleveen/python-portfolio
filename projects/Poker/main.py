import tkinter as tk
from tkinter import Tk, Button
from PIL import Image #, ImageTk
from PIL.ImageTk import PhotoImage
# from PIL import ImageTk, Image
from sys import exit
from collections import Counter
from itertools import cycle
from Poker_classes import Player, Window, Card


def print_function_name(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


def is_flush(kaarten:list):
    """Check of de hand een flush bevat.
    
    :param kaarten: Lijst met kaarten in de hand en op tafel.
    :return Boolean en kleur van de kaarten die de hand vormen.
    """
    suit_counts = Counter(kaart.suit for kaart in kaarten)
    for suit, count in suit_counts.items():
        if count >= 5:
            return True, suit
    return False, ''
def is_straight(kaarten:list):
    """Check of de hand een straight bevat.
    
    :param kaarten: Lijst met kaarten in de hand en op tafel.
    :return Boolean en lijst met de rangen van de kaarten die de hand vormen.
    """
    ranks = [kaart.order for kaart in kaarten]
    ranks = sorted(set(ranks), reverse=True)
    if 14 in ranks:
        ranks.append(1)  # Consider Ace as low for A-2-3-4-5 straight
    for i in range(len(ranks) - 4):
        if int(ranks[i]) - int(ranks[i + 4]) == 4:
            return True, ranks[i:i+5]
    return False, []
def is_straight_flush(kaarten:list):
    """Check of de hand een straight-flush bevat.
    
    :param kaarten: Lijst met kaarten in de hand en op tafel.
    :return Boolean en lijst met de kaarten die de hand vormen.
    """
    suit_groups = {suit: [kaart for kaart in kaarten if kaart.suit == suit] for suit in set(kaart.suit for kaart in kaarten)}
    for _, ranks in suit_groups.items():
        straight, _ = is_straight(ranks)
        if straight:
            return True, ranks
    return False, []


def hand_bepalen(speler, tafel):
        """Bepaal de hand van de speler.
        
        :param speler: Speler-object
        :param tafel: Speler-object van de tafel
        :return 
        """
        def sort_order(input):
            """Sorteer volgorde van de kaarten vaststellen."""
            return input.order
        
        kaarten = speler.cards + tafel.cards
        kaarten.sort(key=sort_order, reverse=True)

        rank_count = Counter([kaart.rank for kaart in kaarten])

        # Check for Straight Flush / Royal Flush
        straight_flush, sf_hand = is_straight_flush(kaarten)
        if straight_flush:
            sf_hand.sort(key=sort_order, reverse=True)
            return (sf_hand, 120 + sf_hand[0].order, 'Royal flush' if sf_hand[1].order == 13  else 'Straight flush')

        # Check for Four of a Kind
        four_kind = [rank for rank, count in rank_count.items() if count == 4]
        if four_kind:
            four_kind = [kaart for kaart in kaarten if kaart.rank in four_kind]
            return (four_kind, 105 + four_kind[0].order + max(speler.cards, key=lambda kaart: kaart.order).order/15, "Vier dezelfde")

        # Check for Full House
        three_kind = [rank for rank, count in rank_count.items() if count == 3]
        pair = [rank for rank, count in rank_count.items() if count == 2]
        if len(three_kind)==2:
            full_house = [kaart for kaart in kaarten if kaart.rank in three_kind]
            full_house.sort(key=sort_order, reverse=True)
            return (full_house[:5],90 + full_house[0].order + full_house[4].order/15, 'Full house')
        elif three_kind and pair:
            full_house = [kaart for kaart in kaarten if kaart.rank in three_kind or kaart.rank == pair[0]]
            full_house.sort(key=sort_order, reverse=True)
            return (full_house, 90 + full_house[0].order + full_house[4].order/15, 'Full house')

        # Check for Flush
        flush, flush_suit = is_flush(kaarten)
        if flush:
            flush_kaarten = [kaart for kaart in kaarten if kaart.suit == flush_suit]
            flush_kaarten.sort(key=sort_order, reverse=True)
            return (flush_kaarten[:5], 75 + flush_kaarten[0].order + flush_kaarten[1].order/15 + flush_kaarten[2].order/(15**2) + flush_kaarten[3].order/(15**3), 'Flush')

        # Check for Straight
        straight, straight_ranks = is_straight(kaarten)
        if straight:
            straight_kaarten = [kaart for kaart in kaarten if kaart.order in straight_ranks or (kaart.order==14 and 1 in straight_ranks)]
            straight_kaarten.sort(key=sort_order, reverse=True)
            gebruikt = set()
            straight_kaarten_ontdubbeld = []
            for kaart in straight_kaarten:
                if kaart.order not in gebruikt:
                    gebruikt.add(kaart.order)
                    straight_kaarten_ontdubbeld.append(kaart)

            return (straight_kaarten_ontdubbeld, 60 + straight_kaarten_ontdubbeld[0].order, 'Straat')

        # Check for Three of a Kind
        if three_kind:
            three_kind = [kaart for kaart in kaarten if kaart.rank in three_kind]
            return (three_kind[:3], 45 + three_kind[0].order + max(speler.cards, key=lambda kaart: kaart.order).order/15 + min(speler.cards, key=lambda kaart: kaart.order).order/(15**2), 'Drie dezelfde')
        
        # Check for Two Pair
        if len(pair) >= 2:
            two_pair = pair[:2]
            two_pair_kaarten = [kaart for kaart in kaarten if kaart.rank in two_pair]
            two_pair_kaarten.sort(key=sort_order, reverse=True)
            return (two_pair_kaarten, 30 + two_pair_kaarten[0].order + two_pair_kaarten[3].order/15 + max(speler.cards, key=lambda kaart: kaart.order).order/(15**2), 'Twee Paren')
        # Check for One Pair
        if pair:
            pair_kaarten = [kaart for kaart in kaarten if kaart.rank in pair]
            return (pair_kaarten, 15 + pair_kaarten[0].order + max(speler.cards, key=lambda kaart: kaart.order).order/15 + min(speler.cards, key=lambda kaart: kaart.order).order/(15**2), 'Paar')
        
        #High card 
        high_card = [max(kaarten, key=lambda kaart: kaart.order)]
        return (high_card, 0 + max(speler.cards, key=lambda kaart: kaart.order).order + min(speler.cards, key=lambda kaart: kaart.order).order/15, 'High card')


# def speleinde(tekst):
#     window = Window('Uitgeschakeld')
#     window.add_text(tekst, x_pos=950, y_pos=450, font=('calibri',15,'bold'))
#     window.add_confirm(window.close, 950, 650) 
#     window.run()


##########################################################################################################################################

#Window
@print_function_name
def kiesmenu_aantal(root, lowerbound=2, upperbound=4):

    def submit_num(var):
        Player.aantal = var.get()
        if lowerbound <= Player.aantal <= upperbound:
            kiesmenu_spelers(root)
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
@print_function_name
def kiesmenu_spelers(root):

    def submit_name(var):
        Player.players = []
        for n in var:
            Player.players.append(Player(n.get()))
        if unique(Player.players):
            spel_spelen(root)
        else:
            window.add_text('Er mogen geen dubbele namen of lege velden zijn!', x_pos=Window.width/2, y_pos=140)
    #Window initieren
    window = Window(root, 'Kiesmenu_spelers')
    # Create frames for top, bottom, and confirm sections
    frame_entries = window.add_frame(x_pos=Window.width/2, y_pos=240)
    #Velden toevoegen
    var = [tk.StringVar() for _ in range(Player.aantal)]
    for i in range(Player.aantal):
        window.add_text(f'Speler {i+1}:', frame_entries, 0, i, grid=True)
        inputfield = tk.Entry(frame_entries, textvariable = var[i], font=('calibre',10,'normal'))
        window.place_widget(inputfield, 1, i, grid=True)
        if i == 0:
            inputfield.focus_force()
    #Bevestig-knop onderaan
    window.add_confirm(lambda var=var: submit_name(var), x_pos=Window.width/2, y_pos=400)

def unique(namen:list) -> bool:
    """Check of de ingevulde namen uniek zijn.
    
    :param namen: Lijst met ingevoerde namen.
    """
    if not namen:
        return False
    unique = []
    for naam in namen:
        if len(naam.name)>10:
            return False
        if naam.name not in unique and naam.name:
            unique.append(naam.name)
    return len(unique) == len(namen)

@print_function_name
def blinds():
    """Blind inzet toevoegen bij startspeler(s).
    
    :param index: Index van de startspeler in de lijst.    
    """
    Player.players[0].add_inzet(50)
    Player.players[0].blind = 'big'
    Player.players[1].add_inzet(25)
    Player.players[1].blind = 'small'

#Window
def bevestigen(root, functie, speler):
    window = Window(root, 'Bevestigen')
    frame_confirm = window.add_frame(x_pos=Window.width/2, y_pos=440)

    img_bg = PhotoImage(Image.open(Card.bg_loc).resize(Card.imagesize))
    window.images.append(img_bg)
    # Create a Label Widget to display the text or Image
    window.add_image(frame_confirm, img_bg, 0, 0)
    window.add_text(f'Het is nu de beurt van {speler.name}.\nBevestig dat jij deze speler bent.', frame_confirm, 0, 1, grid=True)
    #Start en stopknoppen
    window.add_confirm(functie, x_pos=Window.width/2, y_pos=600)


def next_starter(inputlist):
    inputlist = inputlist[1:] + inputlist[:1]
    return inputlist


@print_function_name
def speelronde(root, tafel, deck, callback):
    """Voer de speelronde uit.

    :param spelers: Lijst met alle deelnemende spelers
    :param index: Index van de startspeler in de list 'spelers'
    """
    #Blind inzetten voor startspeler(s)
    blinds()

    # deck.draw(tafel,5)
    #Counter om ervoor te zorgen dat iedere speler aan de beurt is geweest voor de volgende kaart wordt toegevoegd
    counter = 0
    speler_cycle = cycle(Player.players)

    @print_function_name
    def next_turn():
        nonlocal counter
        speler = next(speler_cycle)
        if not speler.fold:
            bevestigen(root, lambda: beurt_scherm(root, speler, tafel, na_beurt), speler)

    def na_beurt(speler):
        nonlocal counter
        speler.blind = ''
        counter +=1
        #Als iedere speler evenveel heeft ingezet en minstens 1 keer aan de beurt is geweest word de volgende kaart toegevoegd
        if gelijke_inzet() and counter >= Player.aantal:
            if tafel.size == 0:
                trek = 3
            elif tafel.size == 5:
                callback(tafel)
                return
            else:
                trek = 1
            deck.draw(tafel, trek)
            counter = 0
        next_turn()

    next_turn()

@print_function_name
def beurt_scherm(root, speler, tafel, callback):
    """Beurt van een speler uitvoeren
    
    :param speler: Speler die aan de beurt is.
    :param spelers: Lijst met alle spelers voor de weergave van de inzet.
    :param tafel: Collectie met kaarten die op tafel liggen
    :param blind: Optionele waarde voor de grote of kleine blind.
    """
    def aanpassen(aantal, max, knop):
        nonlocal inzet_num
        lbl_value["text"] += aantal
        if lbl_value["text"] <= 0:
            lbl_value["text"] = 0
            knop["text"] = "Call"
        if lbl_value["text"] > 0:
            knop["text"] = "Verhogen"
        if lbl_value["text"] >= max:
            lbl_value["text"] = max
            knop["text"] = "All-in"
        inzet_num = lbl_value['text']

    def inzetten(speler):
        nonlocal inzet_num
        max_inzet = max(Player.players, key=lambda speler: speler.inzet).inzet
        inzet_temp = max_inzet - speler.inzet + inzet_num
        speler.add_inzet(inzet_temp)
        callback(speler)
        
    def fold(speler):
        speler.fold = True
        callback(speler)
        
    inzet_num = 0
        #Initialiseer window
    window = Window(root, 'Spelerbeurt')
    #Handkaarten van de speler weergeven
    window.add_cards(speler, 'Handkaarten:', x_pos=950, y_pos=800)
    #Tafel weergeven
    window.add_card_canvas(tafel, x_pos=950, y_pos=350)
    #Inzet-tussenstand weergeven
    window.add_inzet(Player.players)
    if speler.blind:
        window.add_text(f'Je bent de {speler.blind} blind', x_pos=950, y_pos=650, font=('calibri',15,'normal'))

    #Call/Raise knop
    call_button = window.add_button(window.window, "Call", 1650, 900, lambda: inzetten(speler))
    #Fold
    window.add_button(window.window, "Fold", 1750, 900, lambda: fold(speler))
    
    if not speler.blind == 'big':
        #Inzet-knoppen toevoegen
        frame_inzet = window.add_frame(x_pos=1700, y_pos=750, bg="red")
        # frame_inzet["bg"] = "red"

        button_100 = tk.Button(master=frame_inzet, text="+100", fg='green', command= lambda aantal=100, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_100, 0, 0, True)
        button_10 = tk.Button(master=frame_inzet, text="+10", fg='green', command= lambda aantal=10, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_10, 0, 1, True)
        button_1 = tk.Button(master=frame_inzet, text="+1", fg='green', command= lambda aantal=1, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_1, 0, 2, True)
        lbl_value = tk.Label(master=frame_inzet, text=0, font=('calibre', 15, 'bold'), borderwidth=5, relief=tk.RIDGE, width=10, height=2)
        lbl_value.grid(row=3, column=0)
        button_n1 = tk.Button(master=frame_inzet, text="-1", fg='red', command= lambda aantal=-1, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_n1, 0, 4, True)
        button_n10 = tk.Button(master=frame_inzet, text="-10", fg='red', command= lambda aantal=-10, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_n10, 0, 5, True)
        button_n100 = tk.Button(master=frame_inzet, text="-100", fg='red', command= lambda aantal=-100, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_n100, 0, 6, True)

    #Je kan op enter drukken om te callen/verhogen
    window.window.bind('<Return>', lambda event, speler=speler: inzetten(speler))

@print_function_name
def gelijke_inzet() -> bool:
    """Check of elke speler die nog meedoet gelijke inzet heeft.
    """
    max_inzet = max(Player.players, key=lambda speler: speler.inzet).inzet
    for speler in Player.players:
        if speler.inzet != max_inzet and not speler.fold and not speler.geld == 0:
            return False
    return True

@print_function_name
def spel_spelen(root):

    def next_round():
        #Initieer een deck en lege tafel
        tafel = Player('Tafel')
        deck = Player('Deck', True)
        #Maak spelerhanden klaar voor de volgende ronde
        for speler in Player.players:
            speler.setup(deck)

        speelronde(root, tafel, deck, na_speelronde)
        
    def na_speelronde(tafel):
        rondewinnaar(tafel)
        ronde_uitslag(root, tafel, ronde_afhandelen)

    #Check voor winnaar
    def check_winner():
        Player.losers += [speler for speler in Player.players if speler.geld == 0]
        Player.players = [speler for speler in Player.players if speler.geld != 0]
        return len(Player.players) <= 1

    def ronde_afhandelen():
        print('voor', Player.players)
        Player.players = next_starter(Player.players)
        print('na', Player.players)
        if check_winner():
            tussenstand(root, lambda: menu("\nWil je nog een potje spelen?", "Opnieuw", root))
            return
        #Tussenstand weergeven tussen rondes
        tussenstand(root, next_round)

    next_round()


@print_function_name
def rondewinnaar(tafel):
    """
    Bepaal handen van alle spelers, en daarmee de winnaar van de ronde.

    :param spelers: Lijst met spelers.
    :type spelers: list
    :param tafel: Tafelkaarten
    :type tafel: Player()
    """
    for speler in Player.players:
        speler.rondekaarten, speler.rondescore, speler.rondehand = hand_bepalen(speler, tafel)
        print(speler, speler.rondekaarten, speler.rondescore, speler.inzet, speler.geld)
        print("-"*50)

    winnaars = [speler for speler in Player.players if speler.fold == False]
    while winnaars:
        winnaar = max(winnaars, key=lambda speler: speler.rondescore)

        winnaar_inzet = winnaar.inzet
        for speler in Player.players:
            if winnaar_inzet < speler.inzet:
                winst = winnaar_inzet
            else:
                winst = speler.inzet
            winnaar.geld += winst
            winnaar.rondewinst += winst
            speler.inzet -= winnaar_inzet
            if speler.inzet < 0:
                speler.inzet = 0

        #Winnaar uit de lijst verwijderd.
        for index, speler in enumerate(winnaars):
            if speler.name == winnaar.name:
                winnaars.pop(index)
                break

#window
@print_function_name
def tussenstand(root, callback):
    winner = False
    window = Window(root, 'Tussenstand')
    # frame_score = window.add_frame(x_pos=Window.width/2, y_pos=300)
    img_bg = PhotoImage(Image.open(Card.bg_loc).resize(Card.imagesize))
    window.images.append(img_bg)
    # Create a Label Widget to display the text or Image
    window.add_image(window.window, img_bg, x_pos=Window.width/2, y_pos=300, grid=False)

    def sort_order(input):
        """Sorteer volgorde van de kaarten vaststellen."""
        return input.rondescore
    spelers = [speler for speler in Player.players]
    spelers.sort(key=sort_order, reverse=True)

    if len(Player.players) == 1:
        window.add_text(f'Gefeliciteerd {Player.players[0].name}, jij bent winnaartjeman!!\nBedankt voor het spelen!', x_pos=Window.width/2, y_pos=450)
        winner = True
    #Tekst toevoegen
    if Player.players:
        frame_standing = window.add_frame(x_pos=Window.width/2,y_pos=550)
        window.add_text(f"{'Eindstand:' if winner else 'Tussenstand:'}", frame_standing, 0, 0, grid=True, columnspan=2)
        for id_, speler in enumerate(spelers, 1):
            window.add_text(f'{speler.name}', frame_standing, 0, id_, grid=True)
            window.add_text(f'{speler.geld}', frame_standing, 1, id_, grid=True)
    else:
        window.add_text('Helaas, er zijn geen winnaars.\nBedankt voor het spelen!', x_pos=Window.width/2, y_pos=150)

    if Player.losers:
        frame_losers = window.add_frame(x_pos=Window.width/2, y_pos=680)
        window.add_text(f"Helaas, {'jullie zijn' if len(Player.losers) > 1 else 'je bent'} uitgeschakeld", frame_losers, 0, 0, grid=True, columnspan=2)
        for id_, speler in enumerate(Player.losers,1):
            window.add_text(f'{speler.name}', frame_losers, 0, id_, grid=True)
            window.add_text(f'{speler.geld}', frame_losers, 1, id_, grid=True)
    
    #Start en stopknoppen
    window.add_confirm(callback, Window.width/2, 800)


#Window
@print_function_name
def ronde_uitslag(root, tafel, callback):
    """
    Laat de tussenstand zien na het einde van de ronde.

    :param spelers: Lijst met spelers.
    :type spelers: list
    :param tafel: Tafelkaarten
    :type tafel: Player()
    """

    def sort_order(input):
        """Sorteer volgorde van de kaarten vaststellen."""
        return input.rondescore

    #Initialiseer window
    window = Window(root,'Tussenstand')
    frame_top =  window.add_frame(x_pos=350, y_pos=430, bg='black', bd=0)
    # window.add_frame(window.frame_top, 350, 430)
    # window.frame_top["bg"] = "black"
    # window.frame_top["bd"] = 0

    # windows = [window.frame1_t, window.frame2_t, window.frame3_t, window.frame4_t]

    winnaars = [speler for speler in Player.players if speler.fold == False]
    winnaars.sort(key=sort_order, reverse=True)

    #Handkaarten van de spelers weergeven die niet hadden gefold.
    window.add_text('-', frame_top, x_pos=0, y_pos=0, grid=True, font=('calibre',10,'bold'), fg=Window.bg_color)
    window.add_text('Handtype', frame_top, x_pos=1, y_pos=0, grid=True, font=('calibre',10,'bold'), padx=(0,1), width=12)
    window.add_text('Winst', frame_top, x_pos=2, y_pos=0, grid=True, font=('calibre',10,'bold'), padx=(0,1), width=12)
    window.add_text('Huidige\nmonies', frame_top, x_pos=3, y_pos=0, grid=True, font=('calibre',10,'bold'), width=12)
    for i, speler in enumerate(winnaars):
        window.add_cards(speler, f'{speler.name}', frame_top, x_pos=0, y_pos=i+1, grid=True)
        # window.add_cards(speler, windows[i], f'{speler.name}', 0, i+1, grid=True)
        window.add_text(f"{speler.rondehand}", frame_top, x_pos=1, y_pos=i+1, grid=True, font=('calibre',10,'bold'), padx=(0,1), pady=(1,0))
        window.add_text(f"{speler.rondewinst}", frame_top, x_pos=2, y_pos=i+1, grid=True, font=('calibre',10,'bold'), padx=(0,1), pady=(1,0))
        window.add_text(f"{speler.geld}", frame_top, x_pos=3, y_pos=i+1, grid=True, font=('calibre',10,'bold'), pady=(1,0))

    window.add_card_canvas(tafel, 'Tafelkaarten:', 1300, 450)

    #Start en stopknoppen
    window.add_confirm(callback, 950, 900)  



#Window
def menu(tekst:str, knoptekst:str, root:Tk):
    # Create an instance of tkinter window
    window = Window(root,'Start')
    #Plaatjes toevoegen
    frame_menu = window.add_frame(x_pos=Window.width/2, y_pos=450)
    img_bg = PhotoImage(Image.open(Card.bg_loc).resize(Card.imagesize))
    window.images.append(img_bg)
    # Create a Label Widget to display the text or Image
    window.add_image(frame_menu, img_bg, 0,0, grid=True)
    window.add_text(tekst, frame_menu, 0, 1, grid=True)
    #Start en stopknoppen
    window.add_button(window.window, knoptekst, Window.width/2, 600, lambda: kiesmenu_aantal(root))
    window.add_button(window.window, "Instructies", Window.width/2, 650, lambda: instructies(root))
    window.add_button(window.window, "Sluit spel", Window.width/2, 700, exit)

#Window
def instructies(root:Tk):
    window = Window(root,'Instructies')
    #Tekst om op het scherm te plaatsen
    instructietekst = "Klik op de kaarten om deze te spelen,\ntoep als je denkt te kunnen winnen."
    #Tekst toevoegen
    window.add_text(instructietekst, x_pos=Window.width/2, y_pos=400)
    #Knop toevoegen die terug gaat naar het hoofdmenu
    window.add_button(window.window, "Terug", x_pos=Window.width/2, y_pos=650, functie=lambda: menu("\nWil je een potje spelen?", "Start", root))


#Root
def main():
    root = Tk()
    root.title('Toepen')
    root.geometry(f'{Window.width}x{Window.height}+0+0')
    root.resizable(width=False, height=False)
    # root.minsize(Window.width,Window.height)
    # root.maxsize(Window.width,Window.height)    
    root.configure(background=Window.bg_color)

    Player.aantal=3
    Player.players = [Player('oli1'), Player('oli2'), Player('oli3')]
    spel_spelen(root)

    # menu("\nWil je een potje spelen?", "Start", root=root)
    root.mainloop()


if __name__ == '__main__':
    main()
    print('Einde run!')