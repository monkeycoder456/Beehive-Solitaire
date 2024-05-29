import PokerNight as P
import tkinter as tk
import debugcolors as DB
import pathlib as PL

class Beehive(tk.Frame):

    def __init__(self, master=None):
        #stockpile will be the "mother deck"
        self.stockpile = P.Deck()
        self.stockvisable = P.Deck(0)
        self.reserve = P.Deck(0)
        self.workingStacks = [P.Deck(0),P.Deck(0),P.Deck(0),P.Deck(0),P.Deck(0),P.Deck(0)]
        self.discard = P.Deck(0)
        self.stockpile.shuffle(6)

        #input array 
        self.inputArray = [False,False,False,False,False,False,False,False,False]

        # stockpile, stockpile visable, reserve, workstack 1, workstack 2, workstack 3, workstack 4... workstack 6
        #sets up tkiter graphics

        super().__init__(master)
        self.master = master
        self.pack()
        self.setUpGamedata()
        self.setUpGameVisuals()
        self.setUpFrames()
        self.setupBottomframeButtons()
        self.setUpLeftframeButtons()
        self.setUpRightframeButtons()
    
    def setUpGamedata(self) -> None:
        """sets up the game's data. no visuals or any TK shit"""
        self.fillreserve()
        self.workingStacksSetUp()
        self.stockpileToVisable()
        self.setUpGameVariables()

    def setUpGameVariables(self) -> None:
        """sets up variables needed to be seen in gameplay"""
        self.stockpilenumber = self.stockpile.getsize()
        self.reservecardPipsdata = self.reserve.look()
        self.stockvisabletopcarddata = self.stockvisable.look()
        self.stockvisablebehindcard1data = self.stockvisable.pile[-2]
        self.stockvisablebehindcard2data = self.stockvisable.pile[-3]
        self.workingStacksReference = 0

    def setUpGameVisuals(self) -> None:
        """sets up graphics in Tkinter, specifically just the photos, no buttons or frames. just phot references."""

        #suited cards
        self.heartcard = tk.PhotoImage(file=PL.Path(__file__).parent / '1.gif')
        self.diamondcard = tk.PhotoImage(file=PL.Path(__file__).parent / "2.gif")
        self.spadecard = tk.PhotoImage(file=PL.Path(__file__).parent / "3.gif")
        self.clubcard = tk.PhotoImage(file=PL.Path(__file__).parent / "4.gif")

        #squished cards
        self.heartsquash = tk.PhotoImage(file=PL.Path(__file__).parent / "1s.gif")
        self.diamondsquash = tk.PhotoImage(file=PL.Path(__file__).parent / "2s.gif")
        self.spadesquash = tk.PhotoImage(file=PL.Path(__file__).parent / "3s.gif")
        self.clubsquash = tk.PhotoImage(file=PL.Path(__file__).parent / "4s.gif")

        #stack and empty stack card
        self.deckedout = tk.PhotoImage(file=PL.Path(__file__).parent / "emptycard.gif")
        self.stockpilecard = tk.PhotoImage(file=PL.Path(__file__).parent / "carddown.gif")

        #defualt cards with no data mainly placeholders
        self.defaultcard = tk.PhotoImage(file= PL.Path(__file__).parent / "cardup.gif")
        self.compressed = tk.PhotoImage(file=PL.Path(__file__).parent / "squished.gif")

        #logo and winner
        self.logo = tk.PhotoImage(file = PL.Path(__file__).parent / "logo.gif")
        self.winner = tk.PhotoImage(file = PL.Path(__file__).parent / "winner.gif")

    def setUpFrames(self) -> None:
        """sets up the most relevent frames"""
        self.gameframe = tk.Frame(master = self, padx=30, pady=30)
        self.gameframe.pack()

        self.leftframe = tk.Frame(master = self.gameframe, background = DB.LERE, padx=30, pady=30)
        self.rightframe = tk.Frame(master = self.gameframe, background = DB.LERE, padx=30, pady=30)
        self.bottomframe = tk.Frame(master = self.gameframe, background = DB.LERE, padx=30, pady=30)

        self.leftframe.grid(row=0,column=0)
        self.rightframe.grid(row=0,column=1)
        self.bottomframe.grid(row=1,column=0,columnspan=2)

    def setupBottomframeButtons(self) -> None:
        """sets up bottom frame buttons"""
        self.quitter = tk.Button(self.bottomframe, text="QUIT", fg="red",command=self.master.destroy)
        self.restarter = tk.Button(self.bottomframe, text="new game",command=self.restart)

        self.quitter.pack(side="left")
        self.restarter.pack(side="right")

    def restart(self) -> None:
        """restarts game"""
        self.stockpile = P.Deck()
        self.stockvisable = P.Deck(0)
        self.reserve = P.Deck(0)
        self.workingStacks = [P.Deck(0),P.Deck(0),P.Deck(0),P.Deck(0),P.Deck(0),P.Deck(0)]
        self.discard = P.Deck(0)
        self.stockpile.shuffle(6)
        self.inputArray = [False,False,False,False,False,False,False,False,False]

        self.setUpGamedata()
        self.refreshGraphics()

    def setUpLeftframeButtons(self) -> None:
        """sets up buttons for left frame"""
        self.stockpileButton = tk.Button(font=("Comic Sans MS",), master=self.leftframe, text=self.stockpilenumber, image=self.stockpilecard, compound="top", command=lambda: self.pressed(0))
        self.stockvisableButton = tk.Button(font=("Comic Sans MS",), master=self.leftframe, text=self.stockvisabletopcarddata.getpips(), image= self.grabProperCardVisuals(self.stockvisabletopcarddata), compound="center", command=lambda: self.pressed(1))
        self.stockvisablebehindcard1Label = tk.Label(font=("Comic Sans MS",),master=self.leftframe, text=self.stockvisablebehindcard1data.getpips(), image= self.grabProperCardVisualsSquashed(self.stockvisablebehindcard1data), compound="center")
        self.stockvisablebehindcard2Label = tk.Label(font=("Comic Sans MS",),master=self.leftframe, text=self.stockvisablebehindcard2data.getpips(), image= self.grabProperCardVisualsSquashed(self.stockvisablebehindcard2data), compound="center")
        self.logoLabel = tk.Label(font=("Comic Sans MS",),master=self.leftframe, image= self.logo, compound="center")
        self.reserveButton = tk.Button(font=("Comic Sans MS",),master=self.leftframe, text=self.reservecardPipsdata.getpips(), image=self.grabProperCardVisuals(self.reservecardPipsdata), compound="center",command=lambda: self.pressed(2))

        self.reserveButton.grid(row=0,column=3)
        self.stockpileButton.grid(row=1,column=0)
        self.stockvisablebehindcard1Label.grid(row=1,column=2,sticky="w")
        self.stockvisablebehindcard2Label.grid(row=1,column=1,sticky="w")
        self.stockvisableButton.grid(row=1, column=3)
        self.logoLabel.grid(row=0,column=0)

    def setUpRightframeButtons(self) -> None:
        """sets up right frame buttons"""
        self.workingStacksButtons : list[tk.Button]
        self.workingStacksButtons = []
        self.workingStacksReferences = [3,4,5,6,7,8]
        for deck in self.workingStacks:
            self.workingStacksButtons.append(tk.Button(master=self.rightframe,text=deck.look().getpips(), image=self.grabProperCardVisuals(deck.look()),compound="center",font=("Comic Sans MS",)))

        
        #i could not think of a more effective way of doing thins
        self.workingStacksButtons[0].bind('<Button-1>', lambda x: self.pressed(self.workingStacksReferences[0]))
        self.workingStacksButtons[1].bind('<Button-1>', lambda x: self.pressed(self.workingStacksReferences[1]))
        self.workingStacksButtons[2].bind('<Button-1>', lambda x: self.pressed(self.workingStacksReferences[2]))
        self.workingStacksButtons[3].bind('<Button-1>', lambda x: self.pressed(self.workingStacksReferences[3]))
        self.workingStacksButtons[4].bind('<Button-1>', lambda x: self.pressed(self.workingStacksReferences[4]))
        self.workingStacksButtons[5].bind('<Button-1>', lambda x: self.pressed(self.workingStacksReferences[5]))

        self.workingStacksButtons[0].grid(row=0,column=0)
        self.workingStacksButtons[1].grid(row=0,column=1)
        self.workingStacksButtons[2].grid(row=0,column=2)
        self.workingStacksButtons[3].grid(row=1,column=0)
        self.workingStacksButtons[4].grid(row=1,column=1)
        self.workingStacksButtons[5].grid(row=1,column=2)

    def stockpileToVisable(self) -> None:
        """puts the top 3 cards from stockpile to 
        visable stock pile.
        """
        self.stockvisable.put(self.stockpile.draw())
        self.stockvisable.put(self.stockpile.draw())
        self.stockvisable.put(self.stockpile.draw())
    
    def dumpOntoStockpile(self) -> None:
        """when the stockpile is decked out, fill it back up with the cards from stockvisable."""
        while len(self.stockvisable.pile)-1 != 0:
            self.stockpile.put(self.stockvisable.draw())

    def fillreserve(self) -> None:
        """at the beginning of the game, fills the reserve 
        with 10 cards."""
        for i in range(0,10):
            self.reserve.put(self.stockpile.draw())
    
    def workingStacksSetUp(self) -> None:
        """at the beginning of the game, puts one card
        on each working stack."""
        deck : P.Deck
        for deck in self.workingStacks:
            deck.put(self.stockpile.draw())

    def compare(self, deck1 : P.Deck, deck2 : P.Deck) -> bool:
        """compares the top cards on the two asked for decks, than confirms if
        it is valid to put a card on the first asked for deck to the second one.

        typical use is if you want to transfer a card from stock/reserve to work stacks.

        outputs true if the cards are matching.

            Args:

            deck1 (Deck) = the deck you want to take from

            deck2 (Deck) = the deck you want to push too
        """

        if deck1.look().getpips() == deck2.look().getpips():
            return True
        else:
            return False

    def moveCard(self, deck1 : P.Deck, deck2 : P.Deck) -> None:
        """moves a card between two decks

            Args:

            deck1 (Deck) : from deck
            deck2 (Deck) : to deck
        """
        deck2.put(deck1.draw())

    def grabProperCardVisuals(self, card : P.Card) -> tk.PhotoImage:
        if type(card) != P.Card:
            return self.deckedout
        else:
            match card.getsuit():
                case 0:
                    return self.deckedout
                case 1:
                    return self.heartcard
                case 2: 
                    return self.diamondcard
                case 3:
                    return self.spadecard
                case 4:
                    return self.clubcard

    def grabProperCardVisualsSquashed(self, card : P.Card) -> tk.PhotoImage:
        match card.getsuit():
            case 0:
                return self.compressed
            case 1:
                return self.heartsquash
            case 2: 
                return self.diamondsquash
            case 3:
                return self.spadesquash
            case 4:
                return self.clubsquash
        
    def inputGetter(self, signal : int) -> None:
        """with the recieved signal, write to the input array, signal is from 0-8"""
        self.inputArray[signal] = True
    
    def clearInputArray(self) -> None:
        """does what it says on the tin, replaces old array"""
        self.inputArray = [False,False,False,False,False,False,False,False,False]

    def refreshVariables(self) -> None:
        """refreshes key variables for graphics"""
        self.stockpilenumber = self.stockpile.getsize()
        self.reservecardPipsdata = self.reserve.look()
        self.stockvisabletopcarddata = self.stockvisable.look()
        self.stockvisablebehindcard1data = self.stockvisable.arbitrarylook(-2)
        self.stockvisablebehindcard2data = self.stockvisable.arbitrarylook(-3)
    
    def refreshGraphics(self) -> None:
        """refreshes all graphics"""
        self.stockpileButton.config(text=self.stockpilenumber)
        self.stockvisableButton.config(text=self.stockvisabletopcarddata.getpips(), image= self.grabProperCardVisuals(self.stockvisabletopcarddata))
        self.stockvisablebehindcard1Label.config(text=self.stockvisablebehindcard1data.getpips(), image= self.grabProperCardVisualsSquashed(self.stockvisablebehindcard1data))
        self.stockvisablebehindcard2Label.config(text=self.stockvisablebehindcard2data.getpips(), image= self.grabProperCardVisualsSquashed(self.stockvisablebehindcard2data))
        self.reserveButton.config(text=self.reservecardPipsdata.getpips(), image=self.grabProperCardVisuals(self.reservecardPipsdata))

        for buttondeck in zip(self.workingStacksButtons, self.workingStacks):
            buttondeck[0].config(text=buttondeck[1].look().getpips(), image=self.grabProperCardVisuals(buttondeck[1].look()))
    
    def stockpileHandler(self) -> None:
        """will handle stockpile and stockvisable interactions when stockpile is pressed"""
        if (self.stockpile.getsize() == 0) and (self.stockvisable.getsize() != 0):
            self.dumpOntoStockpile()
        else:
            self.stockpileToVisable()

    def logicCycle(self) -> None:
        """the main logical engine the game uses. this interpretes the input array
        data and makes changes or calls methods. """
        

        if self.discard.getsize() == 52:
            self.logoLabel.config(image=self.winner)


        #if its an input for stockpile, do that
        if self.inputArray[0] == True:
            self.stockpileHandler()
            self.clearInputArray()
        
        
        else:
            #quick glance over whole array
            record = 0
            for TRUES in self.inputArray:
                if TRUES == 1:
                    record += 1
            
            if record == 1:
                #not enough input, check if its a working stack input
                if self.inputArray[3:-1].count(True) != 0:
                    self.workingStacksReference = self.inputArray.index(True,3)
                    print(self.workingStacksReference)
                
            
            elif record == 2:
                if (self.inputArray[1] == True) and (self.inputArray[2] == True):
                    #if both inputs are for the two OUT decks than reset and start over
                    self.clearInputArray()
                    
                else:
                    #possibly the point of most bugs...
                    if self.inputArray[1] == True:
                        #stockpile visable
                        reference = self.inputArray.index(True,3)
                        if ((self.compare(self.stockvisable, self.workingStacks[reference-3]) == True) or (self.workingStacks[reference-3]).getsize() == 0):
                            self.moveCard(self.stockvisable, self.workingStacks[reference-3])
                        self.clearInputArray()
                        

                    elif self.inputArray[2] == True:
                        #reserve
                        reference = self.inputArray.index(True,3)
                        if ((self.compare(self.reserve, self.workingStacks[reference-3]) == True) or (self.workingStacks[reference-3]).getsize() == 0):
                            self.moveCard(self.reserve, self.workingStacks[reference-3])
                        self.clearInputArray()
                        
                    
                    else:
                        #this assumes both trues are from working stacks, and thus its an interaction beween them
                        reference2 = self.inputArray.index(True,3)
                        if reference2 == self.workingStacksReference:
                            reference2 = self.inputArray.index(True,self.workingStacksReference + 1)

                        if self.compare(self.workingStacks[reference2-3], self.workingStacks[self.workingStacksReference-3]) == True:
                            self.moveCard(self.workingStacks[self.workingStacksReference-3], self.workingStacks[reference2-3])
                        self.clearInputArray()
        if self.discard.getsize() == 52:
            self.logoLabel.config(image=self.winner)
                        

    def workingStacksOver4(self) -> None:
        for deck in self.workingStacks:
            if deck.getsize() == 4:
                self.discard.put(deck.draw())
                self.discard.put(deck.draw())
                self.discard.put(deck.draw())
                self.discard.put(deck.draw())

    def pressed(self, signal : int) -> None:
        """command used by buttons"""
        if self.discard.getsize() == 52:
            self.logoLabel.config(image=self.winner)
            return
        else:
            self.inputGetter(signal)
            self.logicCycle()
            self.workingStacksOver4()
            self.refreshVariables()
            self.refreshGraphics()
            

root = tk.Tk()
game = Beehive(root)
root.mainloop()
