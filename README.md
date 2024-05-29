# Beehive-Solitaire
short little proof of concept of a solitaire game made within python with use of tkinter.
# How to make it run
run it with python IDE
# Basic rules of Beehive
the goal of the game is to remove all cards from the play field. this is done in groups of four (grouped by number) on the working area. a pile will be cleared when 4 cards of the same number are on there (suit and color don't matter only number). you have a reserve of 10 cards, and a stockpile that you can draw from infinitly. the only way to lose is to lock yourself out of victory by not thinking ahead when putting cards in the working area.
# My stratagy
what I would do is cycle through the stockpile and check which number appears the most when decided what to put on an empty slot in the working area. your reserve is best used to support the choice you make with your stockpile. never pass up the chance of placing a card into the working stacks, it can enable you to working with a differing pool of cards when cycling through the stockpile.
