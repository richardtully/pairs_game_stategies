from random import *




def conc_mem_strat(player,cards,revealed):

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
		return sample([card for card in cards if card not in player.memory and card not in player.picked],1)



	def check_mem():
		'''
		Return a pair that is stored in memory.
		If multiple pairs can be remembered: choose the pair containing the most recently picked (but still active) card.
		'''
		for card1 in player.memory:
			for card2 in player.memory:
				if card1.code == card2.code and card1.position != card2.position:
					return [card1,card2]
				
		return []		
	
	def compare_mem():
		'''
		Compare a card in player.picked with cards in your memory, to see if the 'partner' of the card you've just picked has been picked recently
		'''
		if player.memory != []:
			for card in player.memory:
				if card.code == player.picked[0].code and card.position != player.picked[0].position:
					return [card]
				else:
					return []
		return []


	update_memory()
	'''
	Player will check player.memory first for an easy pair.
	When player HAS to randomly choose (lucky dip), it uses player.memory and player.picked to know where NOT to look.
	'''
	player.picked += check_mem()
	if len(player.picked) == 2:
		return(player.picked)	
	player.picked += lucky_dip(cards)
	player.picked += compare_mem()
	if len(player.picked) == 2:
		return(player.picked)
	player.picked += lucky_dip(cards)
	return(player.picked)