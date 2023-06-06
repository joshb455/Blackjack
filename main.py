import tkinter
import requests
from io import BytesIO
from PIL import ImageTk, Image

screen = tkinter.Tk()

screen.geometry("1000x1000")

screen.title("Blackjack")
class Game:
    def __init__(self):
        self.game_message = tkinter.Label(screen, font='Helvetica 22 bold')
class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.value_total = 0
        #self.card_image = tkinter.PhotoImage(file=r"C:\Users\Josh\PycharmProjects\Blackjack\card_pictures\PNG-cards-1.3\ace_of_hearts.png")

class Money:
    def __init__(self):
        self.money = 10
        self.bet = 1


player_money = Money()

deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6")

deck_id = deck.json()["deck_id"]


'''
draw 2 cards for dealer
draw 2 cards for player
display the hands
ask player to hit or stand

'''


'''img_url = "https://www.marketbeat.com/scripts/temp/estimateswide4879.png"
response2 = requests.get(img_url)
img_data = response2.content
img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
panel = tkinter.Label(screen, image=img)
panel.grid(row=0,column=0) '''
player_hand_frame = tkinter.Frame(screen, bd = 10)
player_hand_frame.grid(row=3, column=0)

dealer_hand_frame = tkinter.Frame(screen, bd = 10)
dealer_hand_frame.grid(row=1,column=0)

game = Game()

def dealer_wins():
    game.game_message.config(text="Dealer Wins with: "+str(dealer_hand.value_total))
    game.game_message.grid(row=4, column=0)

    money_display.config(text="Money: $" +str(player_money.money)+ ".00")
    money_display.grid(row=5,column=0)
    #new_deal()
    #eventually I will code lose money to dealer

def bust():

    game.game_message.config(text="Lord have mercy you done busted")
    game.game_message.grid(row=4, column=0)
    dealer_wins()

def new_deal():
    game.game_message.config(text="")

    response = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=4")

    global dealer_hand
    global player_hand

    dealer_hand = Hand(response.json()['cards'][:2])

    player_hand = Hand(response.json()['cards'][2:4])


    display_hand(player_hand)
    display_dealer_hand(dealer_hand)

    if player_hand.value_total == 21:
        player_wins()



def display_dealer_hand(hand):
    #do this so cards dont stay leftover every new game
    for widgets in dealer_hand_frame.winfo_children():
        widgets.destroy()
    hand.value_total = 0
    for i in range(len(hand.cards)):
        # print("i: ", i)
        # print("hand.cards[i] ====== ", hand.cards[i])
        code = hand.cards[i]['code']
        hand.url = hand.cards[i]['image']
        if hand.cards[i]['value'] == "QUEEN" or hand.cards[i]['value'] == "KING" or hand.cards[i]['value'] == "JACK":
            hand.value_total += 10
        elif hand.cards[i]['value'] == "ACE":
            if hand.value_total + 11 > 21:
                hand.value_total += 1
            else:
                hand.value_total += 11
        else:
            hand.value_total += int(hand.cards[i]['value'])


        if hand.value_total > 21:
            print("lord have mercy the dealer just busted")


        img_url = hand.url
        response2 = requests.get(img_url)
        img_data = response2.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        if i == 0:
            img = tkinter.PhotoImage(file='facedown.png')

        panel = tkinter.Label(dealer_hand_frame, image=img)
        panel.photo = img
        panel.grid(row=1, column=i)

def display_hand(hand):
    # do this so cards dont stay leftover every new game
    for widgets in player_hand_frame.winfo_children():
        widgets.destroy()
    hand.value_total = 0
    for i in range(len(hand.cards)):
        #print("i: ", i)
        #print("hand.cards[i] ====== ", hand.cards[i])
        code = hand.cards[i]['code']
        hand.url = hand.cards[i]['image']
        if hand.cards[i]['value'] == "QUEEN" or hand.cards[i]['value'] == "KING" or hand.cards[i]['value'] == "JACK":
            hand.value_total += 10
        elif hand.cards[i]['value'] == "ACE":
            if hand.value_total + 11 > 21:
                hand.value_total+= 1
            else:
                hand.value_total+= 11
        else:
            hand.value_total += int(hand.cards[i]['value'])

        value_total_display = tkinter.Label(player_hand_frame, text=str(hand.value_total), font='Helvetica 22 bold')
        value_total_display.grid(row=4)

        if hand.value_total > 21:
            print("lord have mercy I just busted")
            bust()



        print("code: ", code)
        img_url = hand.url
        response2 = requests.get(img_url)
        img_data = response2.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        panel = tkinter.Label(player_hand_frame, image=img)
        panel.photo = img
        panel.grid(row= 3, column=i)

def hit_player(hand):
    response = requests.get("https://deckofcardsapi.com/api/deck/"+deck_id+"/draw/?count=1")

    #this [0] is important so that it adds just the card info to the hand list rather than adding a list into another list
    player_hand.cards.append(response.json()['cards'][0])
    #print(hand.cards)
    #print("hand size: ", len(hand.cards))
    #print("response.json()['cards'] : ", response.json()['cards'])


    display_hand(hand)
    if hand.value_total > 21:
        bust()

def hit_dealer(hand):
    response = requests.get("https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=1")

    # this [0] is important so that it adds just the card info to the hand list rather than adding a list into another list
    dealer_hand.cards.append(response.json()['cards'][0])
    # print(hand.cards)
    # print("hand size: ", len(hand.cards))
    # print("response.json()['cards'] : ", response.json()['cards'])

    display_dealer_hand(hand)

def dealer_turn():
    value_total = 0
    for i in range(len(dealer_hand.cards)):
        if dealer_hand.cards[i]['value'] == "QUEEN" or dealer_hand.cards[i]['value'] == "KING" or dealer_hand.cards[i]['value'] == "JACK":
            value_total += 10
        elif dealer_hand.cards[i]['value'] == "ACE":
            if value_total + 11 > 21:
                value_total+= 1
            else:
                value_total+= 11
        else:
            value_total += int(dealer_hand.cards[i]['value'])
    if value_total < 17:
        hit_dealer(dealer_hand)
        dealer_turn()
    else:
        #dealer goes 2nd so if he stays, the hand ends
        hand_over()
def stay():
    dealer_turn()

def player_wins():
    game.game_message.config(text="Player Wins. Dealer had: "+str(dealer_hand.value_total))
    game.game_message.grid(row=4, column=0)

    player_money.money += player_money.bet * 2
    money_display.config(text="Money: $" + str(player_money.money) + ".00")

def push():
    game.game_message.config(text="Push. Player is returned their bet")
    game.game_message.grid(row=4,column=0)
    player_money.money += player_money.bet
    money_display.config(text="Money: $" + str(player_money.money) + ".00")

def hand_over():
    print("hand over, dealer either busted or stayed")
    dealer_score = 21 - dealer_hand.value_total
    player_score = 21 - player_hand.value_total
    print("dealer score: ", dealer_score)
    if player_score < 0:
        dealer_wins()
    elif dealer_score < 0:
        player_wins()

    elif dealer_score < player_score:
        print("dealer wins")
        dealer_wins()
    elif player_score < dealer_score:
        player_wins()
        print("player wins")
    elif player_score == dealer_score:
        push()
        print("tie")

def bet_1():
    player_money.bet = 1
    if player_money.money <1:
        game.game_message.config(text="You do not have enough money to bet.")
    else:
        player_money.money -= 1
        money_display.config(text="Money: $"+str(player_money.money)+".00")
        new_deal()
def bet_5():
    player_money.bet = 5
    if player_money.money <1:
        game.game_message.config(text="You do not have enough money to bet.")
    else:
        player_money.money -= 5
        money_display.config(text="Money: $" + str(player_money.money) + ".00")
        new_deal()
def bet_10():
    player_money.bet = 10
    if player_money.money <1:
        game.game_message.config(text="You do not have enough money to bet.")
    else:
        player_money.money -= 10
        money_display.config(text="Money: $" + str(player_money.money) + ".00")
        new_deal()

dealer_label = tkinter.Label(text="Dealer",  font='Helvetica 22 bold')
player_label = tkinter.Label(text="Player",  font='Helvetica 22 bold')

dealer_label.grid(row=0, column=0)
player_label.grid(row=2, column=0)

new_deal()

button_frame = tkinter.Frame(screen, bg="green")
button_frame.grid(row=3, column= 1)

hit_button = tkinter.Button(button_frame, text="Hit", fg="blue", height= 15, width= 15, command=lambda: hit_player(player_hand))
hit_button.grid(row=3,column=0)

stay_button = tkinter.Button(button_frame, text= "Stay", height= 10, width= 10, command= stay)
stay_button.grid(row= 3, column=1)

money_display = tkinter.Label(screen,text="Money: $"+str(player_money.money)+".00", font='Helvetica 22 bold')
money_display.grid(row=5, column=0)


bet_button_frame = tkinter.Frame(screen)
bet_button_frame.grid(row=6, column=0)

bet1_button = tkinter.Button(bet_button_frame, text="Bet $1", font='Helvetica 22 bold',command=bet_1)
bet5_button = tkinter.Button(bet_button_frame, text="Bet $5", font='Helvetica 22 bold', command=bet_5)
bet10_button = tkinter.Button(bet_button_frame, text="Bet $10", font='Helvetica 22 bold', command=bet_10)

bet1_button.grid(row=1, column=0, padx=10)
bet5_button.grid(row=1, column=1, padx=10)
bet10_button.grid(row=1, column=2,padx=10)



screen.mainloop()