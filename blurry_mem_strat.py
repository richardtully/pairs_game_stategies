from random import *
from random import random

def blurry_mem_strat(player,cards,revealed):

	def blurry_pick(aim_card):
		'''
		This function is designed to loosley imitate a human with a 'blurry' memory.

		'''
		x = player.memory.index(aim_card) # The higher the cards index in memory, the more recently it was added to memory
		p = (1/ player.memsize)*x  # Probability of picking the card we're aiming for
		
		random_num = random()
		if random_num < p:
			return aim_card
		else:
			nearby = [] 
			for card in cards:
				if card.status == 'active':
					if card not in player.picked:
						if abs(card.position[0]-aim_card.position[0]) < 2:
							if abs(card.position[1]-aim_card.position[1]) < 2:
								nearby.append(card)

			chosen = sample(nearby,1)[0]
			chosen.status = 'active'
			return chosen




	def update_memory():
		'''
		Add the last x cards in revealed (where x is the players memsize) to player.memory IF the card is active.
		'''
		if player.memsize == 0:
			player.memory = []
		else:
			player.memory = [card for card in revealed[-player.memsize:] if card.status == 'active']

	def lucky_dip(cards):
		'''
		Randomly pick a card that is NOT in player.picked nor in player.memory
		'''
		chosen = sample([card for card in cards if card not in player.memory and card not in player.picked],1)
		return chosen


	def check_mem():
		'''
		Return a pair that is stored in memory.
		If multiple pairs can be remembered: choose the pair containing the most recently picked (but still active) card.
		'''
		for card1 in player.memory[::-1]: # Looking for the pair of cards most recently added to memory
			for card2 in player.memory[::-1]:
				if card1.code == card2.code and card1.position != card2.position:
					return [blurry_pick(card1)]
	
		return []		
	
	
	def compare_mem():
		'''
		Compare a card in player.picked with cards in your memory, to see if the 'partner' of the card you've just picked has been picked recently
		'''
		for card in player.memory:
			if card.code == player.picked[0].code and card.position != player.picked[0].position:
				return [blurry_pick(card)]

		return []

	update_memory()

	player.picked += check_mem()
	if len(player.picked)>0:
		player.picked += compare_mem()
	if len(player.picked) == 2:
		return(player.picked)
	player.picked += lucky_dip(cards)
	if len(player.picked) == 2:
		return(player.picked)
	player.picked += compare_mem()
	if len(player.picked) == 2:
		return(player.picked)
	player.picked += lucky_dip(cards)
	return(player.picked)