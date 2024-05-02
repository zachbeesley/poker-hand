import tkinter
from tkinter import *
from poker_hand import winning_hand, Card, texas_best, hand_type, two_card_probs
import math

from PIL import ImageTk, Image


def change_players(val):
    app.num_of_players = int(val)

class MyApp():
    def __init__(self):
        self.text = Label(root, text="What is your first card?")
        self.text.grid(row=0, column=0, sticky=W, columnspan=3)

        self.btn_continue = Button(root, text = "Next Card", bd = '5',
                          command = lambda : cont(), bg="blue", fg = "black", activebackground="blue") 
        self.btn_continue.place(x=0, y=195)

        self.hand = []
        self.table = []

        self.current_number = ""
        self.current_suit = ""
        self.number2 = ""

        self.suit1 = ""
        self.suit2 = ""

        self.suit_text = Label(root, text="")
        self.suit_text.grid(row=2, column=4, sticky=W, columnspan=3)

        self.number_text = Label(root, text="")
        self.number_text.grid(row=7, column=6, sticky=W, columnspan=1)

        self.card_text = Label(root, text="")
        self.card_text.place(x=0, y=170)

        self.change = 0
        self.best_hand = Label(root, text="Best Hand:")
        self.best_hand.place(x=5, y=230)

        self.stats = Label(root, text="Win Prob:")
        self.stats.place(x=5, y=250)

        #self.waiting = Label(root, text="")
        #self.waiting.place(x=100, y=250)

        #self.hand_text = Label(root, text="Current Hand: " + str(self.hand))
        #self.hand_text.place(x=0, y=270)

        #self.table_text = Label(root, text="Table: " + str(self.table))
        #self.table_text.place(x=0, y=290)

        self.btn_restart = Button(root, text = "Start Over", bd = '5',
                          command = lambda : start_over(), bg="blue", fg = "black", activebackground="blue")
        self.btn_restart.place(x=0, y=270)

        self.num_players = Label(root, text="Number of players")
        self.num_players.place(x=270, y=200)
        self.player_slider = Scale(root, from_=2, to=10, orient=HORIZONTAL, length=120, highlightthickness=0, 
        background='black', fg='light blue', troughcolor='orange', activebackground='light blue', command=change_players)
        self.player_slider.place(x=270, y=230)

        self.num_of_players = 2

        self.your_cards = Label(text="Your Cards", font=('Helvetica bold', 26))
        self.your_cards.place(x=0, y=320)

        self.card1_image = Label(root)#, image=self.img)#, text="Card 1")
        self.card1_image.place(x=-10, y =370)

        self.card2_image = Label(root)#, text="Card 2")
        self.card2_image.place(x=90, y =370)

        self.table_cards = Label(text="Table's Cards", font=('Helvetica bold', 26))
        self.table_cards.place(x=0, y=500)

        self.table_card1_image = Label(root)#, text="Table Card 1")
        self.table_card1_image.place(x=-10, y =550)

        self.table_card2_image = Label(root)#, text="Table Card 2")
        self.table_card2_image.place(x=90, y =550)

        self.table_card3_image = Label(root)#, text="Table Card 3")
        self.table_card3_image.place(x=190, y =550)

        self.table_card4_image = Label(root)#, text="Table Card 4")
        self.table_card4_image.place(x=290, y =550)

        self.table_card5_image = Label(root)#, text="Table Card 5")
        self.table_card5_image.place(x=390, y =550)
    



root = Tk()
root.title("Poker odds")
root.minsize(200, 200)  # width, height
root.geometry("600x800+50+50")
app = MyApp()

def show_image(card_suit, card_num, card_amount):
    d = {1:app.card1_image, 2:app.card2_image, 3:app.table_card1_image, 4:app.table_card2_image, 5:app.table_card3_image, 6:app.table_card4_image, 7:app.table_card5_image}
    card_suit_to_png = {"c": "cl", "h": "he", "d":"di", "s":"sp"}
    img = Image.open("cards/{0}_{1}.png".format(card_suit[:2], card_num if card_num != "t" else "10"))
    resize_image = img.resize((100, 100))
 
    img = ImageTk.PhotoImage(resize_image)

    d[card_amount].configure(image=img)
    d[card_amount].image = img

def start_over():
        app.text.config(text="What is your first card?")
        app.text.grid(row=0, column=0, sticky=W, columnspan=3)

        #app.btn_continue = Button(root, text = "Continue", bd = '5',
         #                 command = lambda : cont(), bg="blue", fg = "black", activebackground="blue") 
        #app.btn_continue.place(x=-2, y=195)

        app.hand = []
        app.table = []

        app.current_number = ""
        app.current_suit = ""
        app.number2 = ""

        app.suit1 = ""
        app.suit2 = ""

        app.suit_text.config(text="")

        app.number_text.config(text="")

        app.card_text.config(text="")

        app.change = 0
        app.best_hand.config(text="Best Hand:")

        app.stats.config(text="Win Prob:")

        #app.hand_text.config(text="Current Hand: " + str(app.hand))

        #app.table_text.config(text="Table: " + str(app.table))

        #app.btn_restart = Button(root, text = "Start Over", bd = '5',
         #                 command = lambda : start_over(), bg="blue", fg = "black", activebackground="blue")
        #app.btn_restart.place(x=0, y=320)
        img = Image.open("cards/cl_10.png")
        resize_image = img.resize((100, 100))
        img = ImageTk.PhotoImage(resize_image)

        app.card1_image.config(image=img)
        

        app.card2_image.config(image=img)

        app.table_card1_image.config(image=img)

        app.table_card2_image.config(image=img)

        app.table_card3_image.config(image=img)

        app.table_card4_image.config(image=img)

        app.table_card5_image.config(image=img)

def selected_suit(text, app):
    if app.change != 7:
        app.current_suit = text

        app.suit_text.config(text=app.current_suit + "s")
        #suit_text.grid(row=2, column=4, sticky=W, columnspan=3)
        if app.current_number != "":
            app.card_text.config(text=f"{app.current_number} of {app.current_suit}s")
    else:
        app.suit2 = text
        app.suit_text.config(text=app.suit2 + "s")
        #suit_text.grid(row=2, column=4, sticky=W, columnspan=3)
        if app.current_number != "":
            app.card_text.config(text=f"{app.current_number} of {app.current_suit}s")

def selected_number(text, app):
    if app.change != 7:
        number = text
        #print(number)
        app.current_number = number
        app.number_text.config(text=number)
        #number_text.grid(row=7, column=6, sticky=W, columnspan=1)
        if app.current_suit != "":
            app.card_text.config(text=f"{number} of {app.current_suit}s")
        
    else:
        number2 = text
        #print(number2)
        app.number2 = number2
        app.number_text.config(text=number2)
        #app.number_text.grid(row=7, column=6, sticky=W, columnspan=1)
        if app.current_suit != "":
            app.card_text.config(text=f"{number2} of {app.suit2}s")


def cont():
    mapping = {0: "What is your first card?", 1: "What is your second card?", 
    2: "What is the table's first card?", 3: "What is the table's second card?", 4: "What is the table's third card?",
    5: "What is the table's fourth card?", 6: "What is the table'a fifth card?", 7: ""}

    mapping2 = {0: app.hand, 1: app.hand, 2: app.table, 3: app.table, 4: app.table, 5: app.table, 6: app.table}
    mapping2[app.change].append(Card(app.current_number, app.current_suit[0]))
    if app.change >= 4:
        best_card = hand_type(texas_best(app.hand, app.table))
        app.best_hand.config(text="Best Hand: {}".format(best_card))

    if app.change >= 5 or app.change == 1:
        #app.waiting.config(text="Getting Stats...")
        app.stats.config(text=winning_hand(app.hand, app.table, app.num_of_players))
        #app.waiting.config(text="")
    
    app.change += 1
    app.text.config(text=mapping[app.change])
    app.card_text.config(text="")
    app.number_text.config(text="")
    app.suit_text.config(text="")
    app.btn_continue.config(text="Next Card")
    
    #app.hand_text.config(text="Current Hand: " + str(app.hand))
    #app.table_text.config(text="Table: " + str(app.table))

    show_image(app.current_suit, app.current_number.lower(), app.change)

    app.current_number = ""
    app.current_suit = ""


# Create Label in our window

suit_text1 = Label(root, text="Suit:")
suit_text1.grid(row=1, column=0, sticky=W, columnspan=3)


btn_spade = Button(root, text = chr(0x2660), bd = '5',
                          command = lambda : selected_suit("spade", app), bg="blue", fg = "black", activebackground="blue") 

btn_heart = Button(root, text = chr(0x2665), bd = '5',
                          command = lambda : selected_suit("heart", app), fg = "red") 

btn_diamond = Button(root, text = chr(0x2666), bd = '5',
                          command = lambda : selected_suit("diamond", app), fg = "red")

btn_club = Button(root, text = chr(0x2667), bd = '5',
                          command = lambda : selected_suit("club", app), fg="black") 

btn_ace = Button(root, text = "A", bd = '5',
                          command = lambda : selected_number("A", app), fg="purple")
btn_two = Button(root, text = "2", bd = '5',
                          command = lambda : selected_number("2", app), fg="purple")
btn_three = Button(root, text = "3", bd = '5',
                          command = lambda : selected_number("3", app), fg="purple")
btn_four = Button(root, text = "4", bd = '5',
                          command = lambda : selected_number("4", app), fg="purple")
btn_five = Button(root, text = "5", bd = '5',
                          command = lambda : selected_number("5", app), fg="purple")
btn_six = Button(root, text = "6", bd = '5',
                          command = lambda : selected_number("6", app), fg="purple")
btn_seven = Button(root, text = "7", bd = '5',
                          command = lambda : selected_number("7", app), fg="purple")
btn_eight = Button(root, text = "8", bd = '5',
                          command = lambda : selected_number("8", app), fg="purple")
btn_nine = Button(root, text = "9", bd = '5',
                          command = lambda : selected_number("9", app), fg="purple")
btn_ten = Button(root, text = "10", bd = '5',
                          command = lambda : selected_number("T", app), fg="purple")
btn_jack = Button(root, text = "J", bd = '5',
                          command = lambda : selected_number("J", app), fg="purple")
btn_queen = Button(root, text = "Q", bd = '5',
                          command = lambda : selected_number("Q", app), fg="purple")
btn_king = Button(root, text = "K", bd = '5',
                          command = lambda : selected_number("K", app), fg="purple")

btn_spade.grid(row=2,column=0, sticky=W)
btn_heart.grid(row=2,column=1, sticky=W)
btn_diamond.grid(row=2, column=2, sticky=W)
btn_club.grid(row=2, column=3, sticky=W)

number_text1 = Label(root, text="Number:")
number_text1.grid(row=3, column=0, sticky=W, columnspan=3)

btn_ace.grid(row=6, column=0, sticky=W)
btn_two.grid(row=6, column=1, sticky=W)
btn_three.grid(row=6, column=2, sticky=W)
btn_four.grid(row=6, column=3, sticky=W)
btn_five.grid(row=6, column=4, sticky=W)
btn_six.grid(row=6, column=5, sticky=W)
btn_seven.grid(row=6, column=6, sticky=W)
btn_eight.grid(row=7, column=0, sticky=W)
btn_nine.grid(row=7, column=1, sticky=W)
btn_ten.grid(row=7, column=2, sticky=W)
btn_jack.grid(row=7, column=3, sticky=W)
btn_queen.grid(row=7, column=4, sticky=W)
btn_king.grid(row=7, column=5, sticky=W)

#btn_continue = Button(root, text = "Next card", bd = '5',
#                          command = lambda : cont(), bg="blue", fg = "black", activebackground="blue") 
#btn_continue.grid(row=9, column=3, columnspan=2)

root.mainloop()

print(app.hand)
print(app.table)