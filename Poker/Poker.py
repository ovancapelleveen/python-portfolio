import tkinter as tk
from PIL import ImageTk, Image
from sys import exit
from collections import Counter
from itertools import cycle
from Poker_classes import Player, Window


def spelerbeurt(speler, spelers, tafel, blind=None):
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

    def inzetten(speler, spelers):
        nonlocal inzet_num
        max_inzet = max(spelers, key=lambda speler: speler.inzet).inzet
        inzet_temp = max_inzet - speler.inzet + inzet_num
        speler.add_inzet(inzet_temp)
        window.close()
        
    def fold(speler):
        speler.fold = True
        window.close()

    inzet_num = 0
    #Initialiseer window
    window = Window('Spelerbeurt')
    #Handkaarten van de speler weergeven
    window.add_cards(speler, window.frame_bot, 'Handkaarten', 950, 800)
    #Tafel weergeven
    window.add_card_canvas(tafel, 'Tafelkaarten:', 950, 350)
    print(spelers)
    #Inzet-tussenstand weergeven
    window.add_inzet(spelers)
    print(spelers)
    if blind:
        window.add_label(f'Je bent de {blind} blind', x_pos=950, y_pos=650, font=('calibri',15,'normal'))

    #Call/Raise knop
    call_button = tk.Button(master=window.window, text="Call", borderwidth=5, width=10, height=2, command= lambda speler=speler, spelers=spelers: inzetten(speler,spelers))
    window.place_button(call_button, 1650, 900)
    #Fold
    fold_button = tk.Button(master=window.window, text="Fold", borderwidth=5, width=10, height=2, command= lambda speler=speler: fold(speler))
    window.place_button(fold_button, 1750, 900)
    
    if not blind == 'big':
        #Inzet-knoppen toevoegen
        window.add_frame(window.frame_inzet, 1700, 750)
        window.frame_inzet["bg"] = "red"

        button_100 = tk.Button(master=window.frame_inzet, text="+100", fg='green', command= lambda aantal=100, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_100, 0, 0, True)
        button_10 = tk.Button(master=window.frame_inzet, text="+10", fg='green', command= lambda aantal=10, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_10, 0, 1, True)
        button_1 = tk.Button(master=window.frame_inzet, text="+1", fg='green', command= lambda aantal=1, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_1, 0, 2, True)
        lbl_value = tk.Label(master=window.frame_inzet, text=0, font=('calibre', 15, 'bold'), borderwidth=5, relief=tk.RIDGE, width=10, height=2)
        lbl_value.grid(row=3, column=0)
        button_n1 = tk.Button(master=window.frame_inzet, text="-1", fg='red', command= lambda aantal=-1, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_n1, 0, 4, True)
        button_n10 = tk.Button(master=window.frame_inzet, text="-10", fg='red', command= lambda aantal=-10, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_n10, 0, 5, True)
        button_n100 = tk.Button(master=window.frame_inzet, text="-100", fg='red', command= lambda aantal=-100, max=speler.geld, knop=call_button: aanpassen(aantal, max, knop))
        window.place_button(button_n100, 0, 6, True)

    #Je kan op enter drukken om te callen/verhogen
    window.window.bind('<Return>', lambda event, speler=speler, spelers=spelers: inzetten(speler,spelers))
    #Open window
    window.run() 

#Kiesmenu voor het aantal spelers en de spelernamen
def kiesmenu(tekst: str='', aantal: int=None, bericht: str=None,) -> int | list:
    """Laat window zien om het aantal spelers te bepalen, of de namen in te vullen.

    :param tekst: Toelichting met mogelijk aantal spelers.
    :param aantal: Aantal deelnemende spelers.
    :param bericht: Foutmelding als de spelernamen niet uniek zijn.
    :return output: Aantal spelers (2-4), of een lijst met Spelers.
    """
    output = None

    def submit(var):
        """Geef output terug."""
        nonlocal output
        if type(var) == list:
            output = []
            for n in var:
                output.append(Player(n.get()))
            window.close()
        else:
            output = var.get()
            if output in [2,3,4]:
                window.close()

    #Window initieren
    window = Window('Kiesmenu')
    #Errormelding toevoegen als deze er is
    window.add_label(bericht, x_pos=960, y_pos=400, font=('calibri',15,'bold'))
    #Frame klaarzetten voor de input-velden
    window.add_frame(window.frame_top, 950, 500)
    #Velden toevoegen
    if not aantal:
        #Int veld voor aantal spelers
        var=tk.IntVar()
        var.set('')
        input = tk.Entry(window.frame_top, textvariable=var, font=('calibre', 10,'normal'))
        input.grid(row=0,column=1)
        input.focus_force()
        window.add_label(f'Aantal {tekst}:', window.frame_top, 0, 0, grid=True, font=('calibre', 10, 'bold'))
    else:
        #Str-velden voor de spelernamen
        tk.Label(window.frame_top, text=f'Vul de namen in (maximaal 10 tekens):', font=('calibre', 10, 'bold'), bg=Window.bg_color, fg=Window.fg_color).grid(row=0,column=0,columnspan=2)
        var = [tk.StringVar() for _ in range(aantal)]
        for i in range(aantal):
            input = tk.Entry(window.frame_top, textvariable=var[i], font=('calibre',10,'normal'))
            input.grid(row=i+1,column=1)
            if i == 0:
                input.focus_force()
            window.add_label(f'Speler {i+1}:', window.frame_top, 0, i+1, grid=True, font=('calibre',10, 'bold'))

    #Bevestig-knop onderaan
    window.add_confirm(lambda var=var: submit(var), x_pos=950, y_pos=650)

    window.run()
    return output

def startmenu():
    """Laat scherm zien met het startmenu."""
    window = Window('Start')
    window.add_frame(window.frame_text, 950, 450)
    window.add_frame(window.frame_confirm, 950, 700)
    #Afbeelding toevoegen
    img_bg = ImageTk.PhotoImage(Image.open(Window.bg_loc).resize((120,150)))
    # Create a Label Widget to display the text or Image
    tk.Label(master=window.frame_text, image=img_bg, bg=Window.bg_color).pack()
    window.add_label("\nWil je een potje spelen?", window.frame_text, font=('calibri',15,'normal'))
    #Start en stopknoppen
    startbutton=tk.Button(master=window.frame_confirm, text=f"Start", borderwidth=5, width=10, height=2, command=window.close)
    window.place_button(startbutton, 0, 0, True)
    exitbutton=tk.Button(master=window.frame_confirm, text=f"Sluit spel", borderwidth=5, width=10, height=2,command=exit)
    window.place_button(exitbutton, 1, 0, True)

    window.window.bind('<Return>', lambda event: window.close())
    window.run()


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

def blinds(spelers:list, index:int):
    """Blind inzet toevoegen bij startspeler(s).
    
    :param spelers: Lijst met de spelers.
    :param index: Index van de startspeler in de lijst.    
    """
    spelers[index].add_inzet(50)
    spelers[(index+1)%len(spelers)].add_inzet(25)

def gelijke_inzet(spelers: list) -> bool:
    """Check of elke speler die nog meedoet gelijke inzet heeft.

    :param spelers: Lijst met alle spelers.
    """
    max_inzet = max(spelers, key=lambda speler: speler.inzet).inzet
    for speler in spelers:
        if speler.inzet != max_inzet and not speler.fold and not speler.geld == 0:
            return False
    return True

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


def wincheck(spelers:list, tafel):
    """
    Bepaal handen van alle spelers, en daarmee de winnaar van de ronde.

    :param spelers: Lijst met spelers.
    :type spelers: list
    :param tafel: Tafelkaarten
    :type tafel: Player()
    """
    for speler in spelers:
        speler.rondekaarten, speler.rondescore, speler.rondehand = hand_bepalen(speler, tafel)
        print(speler, speler.rondekaarten, speler.rondescore, speler.inzet, speler.geld)
        print("-"*50)

    winnaars = [speler for speler in spelers if speler.fold == False]
    while winnaars:
        winnaar = max(winnaars, key=lambda speler: speler.rondescore)

        winnaar_inzet = winnaar.inzet
        for speler in spelers:
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


def speelronde(spelers, index):
    """Voer de speelronde uit.

    :param spelers: Lijst met alle deelnemende spelers
    :param index: Index van de startspeler in de list 'spelers'
    """
    #Initieer een deck en lege tafel
    tafel = Player('Tafel')
    deck = Player('Deck', True)
    #Maak spelerhanden klaar voor de volgende ronde
    for speler in spelers:
        speler.setup(deck)

    # deck.draw(tafel, 5)

    #Blind inzetten voor startspeler(s)
    blinds(spelers, index)
    aantal = len(spelers)
    
    #Big blind
    spelers[index].bevestigen()
    spelerbeurt(spelers[index], spelers, tafel, 'big')
    index = (index+1)%aantal
    #Small blind
    spelers[index].bevestigen()
    spelerbeurt(spelers[index], spelers, tafel, 'small')
    index = (index+1)%aantal

    #Counter om ervoor te zorgen dat iedere speler aan de beurt is geweest voor de volgende kaart wordt toegevoegd
    counter = 1
    speler_cycle  = cycle(spelers)
    for i, speler in enumerate(speler_cycle):
        if i < index:
            continue
        
        #Break als nog maar 1 actieve speler
        if sum(1 for speler in spelers if not speler.fold) == 1:
            break

        #Spelerbeurt als deze niet gefold heeft
        if not speler.fold:
            speler.bevestigen()
            spelerbeurt(speler, spelers, tafel)
        counter +=1
        #Als iedere speler evenveel heeft ingezet en minstens 1 keer aan de beurt is geweest word de volgende kaart toegevoegd
        if gelijke_inzet(spelers) and counter >= aantal:
            if tafel.size == 0:
                trek = 3
            elif tafel.size == 5:
                break
            else:
                trek = 1
            deck.draw(tafel, trek)
            counter = 0

    wincheck(spelers, tafel)
    tussenstand(spelers, tafel)


def tussenstand(spelers:list, tafel):
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
    window = Window('Tussenstand')
    window.add_frame(window.frame_top, 350, 430)
    window.frame_top["bg"] = "black"
    window.frame_top["bd"] = 0

    windows = [window.frame1_t, window.frame2_t, window.frame3_t, window.frame4_t]

    winnaars = [speler for speler in spelers if speler.fold == False]
    winnaars.sort(key=sort_order, reverse=True)
    #Handkaarten van de spelers weergeven die niet hadden gefold.
    window.add_label('-', window.frame_top, x_pos=0, y_pos=0, grid=True, font=('calibre',10,'bold'), fg=Window.bg_color)
    window.add_label('Handtype', window.frame_top, x_pos=1, y_pos=0, grid=True, font=('calibre',10,'bold'), padx=(0,1), width=12)
    window.add_label('Winst', window.frame_top, x_pos=2, y_pos=0, grid=True, font=('calibre',10,'bold'), padx=(0,1), width=12)
    window.add_label('Huidige\nmonies', window.frame_top, x_pos=3, y_pos=0, grid=True, font=('calibre',10,'bold'), width=12)
    for i, speler in enumerate(winnaars):
        window.add_cards(speler, windows[i], f'{speler.name}', 0, i+1, grid=True)
        window.add_label(f"{speler.rondehand}", window.frame_top, x_pos=1, y_pos=i+1, grid=True, font=('calibre',10,'bold'), padx=(0,1), pady=(1,0))
        window.add_label(f"{speler.rondewinst}", window.frame_top, x_pos=2, y_pos=i+1, grid=True, font=('calibre',10,'bold'), padx=(0,1), pady=(1,0))
        window.add_label(f"{speler.geld}", window.frame_top, x_pos=3, y_pos=i+1, grid=True, font=('calibre',10,'bold'), pady=(1,0))

    window.add_card_canvas(tafel, 'Tafelkaarten:', 1300, 450)

    #Start en stopknoppen
    window.add_confirm(window.close, 950, 900)  
    window.run()


def speleinde(tekst):
    window = Window('Uitgeschakeld')
    window.add_label(tekst, x_pos=950, y_pos=450, font=('calibri',15,'bold'))
    window.add_confirm(window.close, 950, 650) 
    window.run()



def main(): 
    """Mainfunctie die het script draait."""

    startmenu()

    #Bepaal aantal spelers
    num_players = kiesmenu(tekst='spelers (2-4)')
    #Input voor spelernamen
    spelers = []
    error_msg = ''
    while not unique(spelers):
        spelers = kiesmenu(aantal=num_players, bericht=error_msg)
        error_msg = 'Er mogen geen dubbele namen of lege velden zijn.'

    indices = cycle(range(num_players))
    #Testgegevens
    # spelers = [Player('oli1'), Player('oli2'), Player('oli3')]
    for start_index in indices:

        speelronde(spelers, start_index)

        #Check voor de winnaar en of uitschakeling.
        spelers_temp = []
        for speler in spelers:
            if speler.geld != 0:
                spelers_temp.append(speler)
            else:
                speleinde(f"Helaas {speler.name}, je monies zijn op.\n\nJe kan nu niet meer mee spelen!")
        spelers = spelers_temp
        if len(spelers) == 1:
            speleinde(f'Gefeliciteerd {spelers[0].name}, jij bent winnaartjeman!!')
            break


if __name__ == '__main__':
    main()
    print('Einde run!')