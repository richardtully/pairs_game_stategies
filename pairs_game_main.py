

from random import *
import matplotlib.pyplot as plt
import math
from concentrated_memory_strat import conc_mem_strat
from blurry_mem_strat import blurry_mem_strat



# Card - these are the cards that will played with
class Card:
    def __init__(self, position, code, status):
    	# It's location in the grid of cards
        self.position = position
        # Each card shares a code with one other card: i'ts pair
        self.code = code
        # The status indicates if a card has been picked or not
        self.status = status

# These are the players who will play the game
class Player:
	def __init__(self, score, memsize, name, revealed, pick_strat):
		# cumulative score
		self.score = score 
		# updated after every players turn
		self.score_record = []
		# Players can see details of the last x cards in revealed, where x is their memsize
		self.memsize = memsize
		# a list of cards that they know the details of, updated when non-pairs are placed back on the grid
		self.memory = []
		# the cards selected from the table on a players turn, they get replaced if they're not a pair
		self.picked = []
		self.name = name
		self.pick_strat = pick_strat

	def pick(self):
		return self.pick_strat(self,cards,revealed)



def create_cards (width,height):
	'''
	This creates a a set of cards, they are each paired with one other card in a randomly assigned position
	'''
	number_of_cards = width*height
	v = [i for i in range (number_of_cards)] 
	shuffle(v)

	# The cards on the 'board'. 
	cards=[Card((i%width,math.floor(i/height)), str(v.pop(-1)%(number_of_cards/2)), 'active') for i in range(number_of_cards)]
	return(cards)

def check_picked(player, picked):
	'''
	Check if the 2 cards in a players hand (player.picked) are a pair.
	If they make a pair, remove those cards from the board (make them inactive) and increase the players score.
	If they don't make a pair, add those cards to the revealed list
	'''
	global revealed

	if len(picked) == 2: 
		if picked[0].code == picked[1].code:
			for i in picked:		
				cards.remove(i)
				i.status = 'inactive'
			player.score += 1
			return 'Success'

	revealed += picked




'''

  .g8"""bgd                                          `7MM"""YMM `7MM                              
.dP'     `M                                            MM    `7   MM                              
dM'       `   ,6"Yb.  `7MMpMMMb.pMMMb.   .gP"Ya        MM   d     MM   ,pW"Wq.  `7M'    ,A    `MF'
MM           8)   MM    MM    MM    MM  ,M'   Yb       MM""MM     MM  6W'   `Wb   VA   ,VAA   ,V  
MM.    `7MMF' ,pm9MM    MM    MM    MM  8M""""""       MM   Y     MM  8M     M8    VA ,V  VA ,V   
`Mb.     MM  8M   MM    MM    MM    MM  YM.    ,       MM         MM  YA.   ,A9     VVV    VVV    
  `"bmmmdPY  `Moo9^Yo..JMML  JMML  JMML. `Mbmmd'     .JMML.     .JMML. `Ybmd9'       W      W 

                                                                                                  
'''


# Width and height of the grid of cards
width = 10
height = 10

# If 2 cards get picked but they aren't a pair, they're added to the revealed list
# Players can see details of the last x cards in revealed, where x is their memory length
revealed = []


player1 = Player(0,0, 'player_1', revealed, blurry_mem_strat)
player2 = Player(0,5, 'player_2', revealed, blurry_mem_strat)
player3 = Player(0,10, 'player_3', revealed, blurry_mem_strat)
player4 = Player(0,5, 'player_4', revealed, conc_mem_strat)
player5 = Player(0,10, 'player_5', revealed, conc_mem_strat)

players = [player1, player2, player3, player4, player5]

cards = create_cards(width, height)





# Turn Starts:
n=0

# The game continues until all the pairs have been removed
while cards:
	current_player = players[n%len(players)]
	while cards:

		# Current player picks
		current_player.picked = []
		x = current_player.pick() 

		# If he doesn't pick a pair, its the next players turn.
		if check_picked(current_player, x) != 'Success': 
			break

	# Before the next players turn, we update each players score record		
	for i in players:
		i.score_record.append(i.score)


	n += 1





# Print everyones final score
f = lambda x: x.name + ':  ' + str(x.score)
for i in players:
	print(f(i))


print('Total number of turns taken to finish the game: ' + str(len(player1.score_record)))


x = range(len(player1.score_record))


# Creating a graph to summarise the game
for i in players:
	plt.plot(x,i.score_record, label = str(i.name) + ' used ' + str(i.pick_strat.__name__) + ' with memory length: ' + str(i.memsize))
plt.xlabel('Turn number \n (every players turns contribute to this number)')
plt.ylabel('Score')
plt.legend()
plt.show()