import csv
import pathlib
import xml.etree.ElementTree as ET
from hearthstone.deckstrings import Deck


"""
Prepare the data for all the cards in Hearthstone and their later classification in the format
"""
base_path = pathlib.Path(__file__).parent.resolve()
format_path = base_path / "Format.csv"
card_data_path = base_path / "CardDefs.xml"
base_card_data = ET.parse(card_data_path).getroot()
relevant_card_data = {}
for card in base_card_data:
    try:relevant_card_data[card.attrib["ID"]] = card[0][1].text
    except:pass
    
"""
Functions
"""
#Rimescale Siren has no league
def define_format(league):
    format_ = set()
    special_cases = {}
    with open(format_path, "r", newline="") as format_file:
        card_reader = csv.reader(format_file, delimiter=",", quotechar='"')
        for row in card_reader:
            if len(row[1]) == 8:
                if int(row[1][-1]) >= league:
                    format_.add(row[0])
            elif len(row[1]) == 22:
                if int(row[1][7]) >= league:
                    format_.add(row[0])
            else:
                special_cases[row[0]] = row[1]
    return format_, special_cases
#print(special_cases)
            
#for n, deck in enumerate(decks):
def evaluate_deck(deck, league, class_, format_, special_cases):
    deck = Deck.from_deckstring(deck)
    cards_in_deck = set()
    for card in deck.cards:
        card = relevant_card_data[str(card[0])]
        #print(card)
        cards_in_deck.add(card)
    illegal_cards = cards_in_deck.difference(format_)
    accepted_special_cases = set()
    for card in illegal_cards:
        try:
            status = special_cases[card]
            status = status.split(",")
            if status == ["Special"]:
                accepted_special_cases.add(card)
            else:
                for condition in status:
                    if class_ in condition:
                        if int(condition[-1]) >= league:
                            accepted_special_cases.add(card)
                            break
                if card in illegal_cards:
                    for condition in status:
                        if len(condition) == 8 or len(condition) == 9:
                            if int(condition[-1]) >= league:
                                accepted_special_cases.add(card)
                                break
        except:
            pass
    illegal_cards = illegal_cards.difference(accepted_special_cases)
    if len(illegal_cards) == 0:
        print("There are no illegal cards")
    else:
        print("The next cards are illegal:", illegal_cards)
        
"""
Running the Script
"""
league = int(input("Enter the League as a number (1-5): "))
t_format, t_special_cases = define_format(league)
while True:
    class_ = input("Enter the Class (e.g Death Knight): ")
    deck = input("Enter the Deck code (e.g AAEBAfe5AgzP): ")
    evaluate_deck(deck, league, class_, t_format, t_special_cases)
    check_continuation = input("Continue? (y or n): ")
    if check_continuation == "n":
        break
    
    
    

