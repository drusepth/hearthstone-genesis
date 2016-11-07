import random #random.choice
import copy #copy.copy
import re

class MinionAbility:
	templates = [
		{'value': 0.00, 'text': '<ability>.' },
		{'value': 0.20, 'text': 'Battlecry: <effect>.'},
		{'value': 0.20, 'text': 'Battlecry: <targetable_effect>.'},
		{'value': 0.20, 'text': 'Battlecry: If <condition>, <targetable_effect>.'},
		{'value': 0.30, 'text': 'Battlecry: If <condition>, <targetable_effect> and <effect>.'},
		{'value': 1.50, 'text': 'Battlecry: Gain <stackable_effect> for every spell in your hand.'},
		{'value': 1.50, 'text': 'Battlecry: Gain <stackable_effect> for every minion in your hand.'},
		{'value': 0.20, 'text': 'Deathrattle: <effect>.'},
		{'value': 0.50, 'text': 'Inspire: <effect>.'},
		{'value': 0.50, 'text': 'Inspire: Gain <stackable_effect>.'},
		{'value': 0.50, 'text': 'Inspire: Gain "<ability_aura>".'},
		{'value': 0.50, 'text': 'At the beginning of your turn, <effect>.'},
		{'value': 0.50, 'text': 'At the end of your turn, gain <ability>.'},
		{'value': 0.50, 'text': 'At the end of each turn, <effect>.'},
		{'value': 0.20, 'text': 'Combo: <effect>.'},
		{'value': 0.20, 'text': 'Combo: <targetable_effect>.'},
		{'value': 0.20, 'text': 'Enrage: <ability_aura>.'},
		{'value': 0.20, 'text': 'Has <ability> while <condition>.'},
		{'value': 0.30, 'text': 'Your <minion_type>s are <minion_type>s.'},
		{'value': 0.30, 'text': 'Your <minion_type>s gain <stackable_effect>.'},
		{'value': 0.30, 'text': 'Your <minion_type>s gain <ability>.'},
		{'value': -1.30, 'text': 'Choose One - <targetable_effect>; or <targetable_effect>.'},
		{'value': -1.30, 'text': 'Choose One - <effect>; or <effect>.'},
		{'value': -1.30, 'text': 'Choose One - Gain <ability>; or Gain <ability>.'},
		{'value': -1.30, 'text': 'Choose One - <ability_aura>; or <ability_aura>.'},
		{'value': 0.30, 'text': 'Whenever this minion attacks, <effect>.'},
		{'value': 0.30, 'text': 'After this attacks and kills a minion, <effect>.'},
		{'value': 0.30, 'text': 'Whenever this minion takes damage, <effect>.'},
		{'value': 0.30, 'text': 'Whenever you cast a spell, <effect>.'},
		{'value': 0.30, 'text': 'Whenever a <minion_type> dies, <effect>.'},
		{'value': 0.30, 'text': 'Whenever you discard a card, <effect>.'},
		{'value': 0.30, 'text': 'Whenever your hero is attacked, <effect>.'},
		{'value': 0.30, 'text': 'Whenever you gain Armor, <effect>.'},
		{'value': -1.30, 'text': 'Whenever this minion loses <ability>, <effect>.'},
		{'value': -1.30, 'text': 'Whenever this minion gains <ability>, <effect>.'},
		{'value': 1.30, 'text': 'Adjacent minions have <stackable_effect>.'},
	]

	conditions = [
		{'value': -5.0, 'text': 'your deck has no more than 1 of any card' },
		{'value': -0.40, 'text': 'your deck has at least <i+(2-20)> <minion_type>s'},
		{'value': -0.40, 'text': 'your deck has no more than <i+(2-20)> <minion_type>s'},
		{'value': 0.00, 'text': 'you have at least <i+(2-8)> cards in hand'},
		{'value': 0.00, 'text': 'your hand is empty'},
		{'value': 0.00, 'text': 'you control no minions'},
		{'value': 0.00, 'text': 'your opponent has at least <i+(1-6)> minions'},
		{'value': 0.00, 'text': 'you control a Secret'},
		{'value': -0.50, 'text': 'your opponent controls a Secret'},
	]

	effects = [
		{'value': 1.84, 'text': 'Draw a card'},
		{'value': 1.00, 'text': 'Draw <V+(2-4)> cards'},
		{'value': -1.25, 'text': 'Discard a card'},
		{'value': -1.98, 'text': 'Your opponent draws a card'},
		{'value': -0.27, 'text': 'Deal <q+(1-10)> damage to your hero'},
		{'value': -0.27, 'text': 'Deal <q+(1-10)> damage a random allied character'},
		{'value': -0.27, 'text': 'Deal <q+(1-10)> damage to HIMSELF'},
		{'value': 0.27, 'text': 'Deal <q+(1-10)> damage a random enemy'},
		{'value': -1.27, 'text': 'Destroy a Mana Crystal'},
		{'value': 0.75, 'text': 'Equip a random weapon'},
		{'value': 0.15, 'text': 'Add a random weapon to your hand'},
		{'value': 1.31, 'text': 'Your other minions gain <stackable_effect>'},
		{'value': 1.31, 'text': 'Your <minion_type>s gain <stackable_effect>'},
		{'value': 1.31, 'text': 'Your other minions gain "<ability_aura>"'},
		{'value': 1.31, 'text': 'Your <minion_type>s gain "<ability_aura>"'},
		{'value': 0.31, 'text': 'Gain <stackable_effect> for every <minion_type> in your hand'},
		{'value': 0.31, 'text': 'Give a random friendly minion <ability>'},
		{'value': 0.31, 'text': 'Give a random friendly minion "<ability_aura>"'},
		{'value': 0.31, 'text': 'Give a random friendly minion <stackable_effect>'},
		{'value': 0.31, 'text': 'Gain <ability> until end of turn'},
		{'value': 0.31, 'text': 'Gain <stackable_effect> for each damaged minion on the battlefield'},
		{'value': 0.42, 'text': 'Summon a random <v+(0-10)>-Cost minion'},
		{'value': 0.42, 'text': 'Restore <v+(1-10)> Health to a random character'},
		{'value': 0.22, 'text': 'Gain <v+(1-10)> Armor'},
		{'value': 0.33, 'text': 'The next <minion_type> you play costs Health instead of mana'},
		{'value': 0.33, 'text': 'Summon a random <minion_type>'},
		{'value': 0.33, 'text': 'Return this minion to your hand'},
		{'value': 2.33, 'text': 'Put a <minion_type> from your hand into play'},
		{'value': 1.33, 'text': 'Give all <minion_type>s in your hand and deck <stackable_effect>'},
		{'value': -5.0, 'text': 'Destroy a random friendly minion'},
		{'value': 4.20, 'text': 'Destroy all <minion_type>s'},
		{'value': 0.20, 'text': 'Shuffle this minion into your deck'},
		{'value': -0.70, 'text': "Shuffle this minion into your opponent's deck"},
	]

	targetable_effects = [
		{'value': 0.82, 'text': 'Deal <v+(0-8)> damage to a minion'},
		{'value': 0.82, 'text': 'Deal <v+(1-6)> damage to an enemy'},
		{'value': 1.84, 'text': 'Deal <V+(0-8)> damage to all enemy minions'},
		{'value': 5.33, 'text': 'Destroy a minion'},
		{'value': 2.73, 'text': 'Destroy a <minion_type>'},
		{'value': 1.02, 'text': 'Freeze a minion'},
		{'value': 0.42, 'text': 'Freeze a <minion_type>'},
		{'value': 0.83, 'text': 'Silence a minion'},
		{'value': 0.13, 'text': 'Silence a <minion_type>'},
		{'value': 0.13, 'text': 'Return a <minion_type> to your hand'},
		{'value': 1.05, 'text': 'Discover a <minion_type>'},
		{'value': 0.35, 'text': 'Discover a weapon'},
		{'value': 0.35, 'text': 'Discover a spell'},
		{'value': 0.05, 'text': 'Discover a <v+(1-10)>-Cost spell'},
		{'value': 0.42, 'text': 'Restore <v+(1-10)> Health to a character'},
		{'value': 0.92, 'text': 'Take control of a minion with <v+(1-10)> or less Health'},
		{'value': 0.92, 'text': 'Take control of a minion with <v+(1-10)> or less Attack'},
	]

	stackable_effects = [
		{'value': 0.57, 'text': '+<v+(1-5)> Attack'},
		{'value': 0.40, 'text': '+<v+(1-5)> Health'},
		{'value': 1.10, 'text': '+<v+(1-5)>/+<v+(1-5)>'},
		{'value': 0.46, 'text': 'Spell Power +1'},
	]

	abilities = [
		{'value': 0.51, 'text': 'Taunt'},
		{'value': 1.40, 'text': 'Divine Shield'},
		{'value': 1.19, 'text': 'Windfury'},
		{'value': 5.40, 'text': 'Mega-Windfury'},
		{'value': 0.46, 'text': 'Spell Power +<v+(1-3)>'},
		{'value': 0.33, 'text': 'Charge'},
		{'value': 0.61, 'text': 'Stealth'},
		{'value': -0.83, 'text': 'Overload (<i+(1-3)>)'},
		{'value': -0.83, 'text': "Can't attack"},
	]

	ability_auras = [
		{'value': 3.40, 'text': 'Your Hero is Immune'},
		{'value': -0.53, 'text': "50% chance to attack the wrong target"},
		{'value': 0.36, 'text': 'Your spells cost (<v+(1-3)>) less.'},
		{'value': 0.26, 'text': 'Your minions cost (<v+(1-3)>) less.'},
		{'value': 0.06, 'text': 'Your weapons cost (<v+(1-3)>) less.'},
		{'value': 0.36, 'text': 'Your spells cost (<i+(1-3)>) more.'},
		{'value': 0.26, 'text': 'Your minions cost (<i+(1-3)>) more.'},
		{'value': 0.06, 'text': 'Your weapons cost (<i+(1-3)>) more.'},
		{'value': 0.33, 'text': 'Your Hero Power costs (<V+(1-2)>) less.'},
		{'value': -0.53, 'text': "Your opponent's Hero Power costs (<V+(1-2)>) less."},
		{'value': 0.53, 'text': "Your weapon has +<v+(1-3)> Attack."},
		{'value': 0.33, 'text': "Can't be targeted by spells or Hero Powers"},
	]

	minion_types = [
		'Beast', 'Dragon', 'Murloc', 'Demon', 'Mech', 'Pirate', 'Totem'
	]

	def __init__(self, text="", value=0):
		#print("MinionAbility init with text=%s & value=%s" % (text, value))
		self.text = text
		self.value = value

	@staticmethod
	def random():
		#print("Generating random minion ability")

		ability = copy.copy(random.choice(MinionAbility.templates))
		#print("Chose template %s" % ability)

		while '<effect>' in ability.get('text'):
			random_effect    = random.choice(MinionAbility.effects)
			ability['text']  = ability['text'].replace('<effect>', random_effect.get('text'), 1)
			ability['value'] = ability['value'] + random_effect.get('value')

		while '<targetable_effect>' in ability.get('text'):
			random_effect    = random.choice(MinionAbility.targetable_effects)
			ability['text']  = ability['text'].replace('<targetable_effect>', random_effect.get('text'), 1)
			ability['value'] = ability['value'] + random_effect.get('value')

		while '<stackable_effect>' in ability.get('text'):
			random_effect    = random.choice(MinionAbility.stackable_effects)
			ability['text']  = ability['text'].replace('<stackable_effect>', random_effect.get('text'), 1)
			ability['value'] = ability['value'] + random_effect.get('value')

		while '<condition>' in ability.get('text'):
			condition        = random.choice(MinionAbility.conditions)
			ability['text']  = ability['text'].replace('<condition>', condition.get('text'), 1)
			ability['value'] = ability['value'] + condition.get('value')

		while '<ability>' in ability.get('text'):
			random_ability   = random.choice(MinionAbility.abilities)
			ability['text']  = ability['text'].replace('<ability>', random_ability.get('text'), 1)
			ability['value'] = ability['value'] + random_ability.get('value')

		while '<ability_aura>' in ability.get('text'):
			random_ability   = random.choice(MinionAbility.ability_auras)
			ability['text']  = ability['text'].replace('<ability_aura>', random_ability.get('text'), 1)
			ability['value'] = ability['value'] + random_ability.get('value')

		# Replace variable rolls
		while True:
			match = re.search('\<(\w*)\+*\((\d+)\-(\d+)\)\>', ability.get('text'))
			if not match:
				break

			flags, lower_bound, upper_bound = match.group(1), match.group(2), match.group(3)

			roll = random.randint(int(lower_bound), int(upper_bound))
			#print("Rolled %s for %s in %s" % (roll, match.group(0), ability.get('text')))

			if False: pass     # Flags defined below:
			elif 'v' in flags: # increase value by the roll amount
				ability['value'] = ability['value'] + roll
			elif 'V' in flags: # increase value by 2 times the roll amount
				ability['value'] = ability['value'] + 2 * roll
			elif 'i' in flags: # decrease value by the roll amount
				ability['value'] = ability['value'] - roll
			elif 'q' in flags: # decrease value by 0.25 * roll around
				ability['value'] = ability['value'] - 0.25 * roll
			elif 'm' in flags: # multiply ability times roll
				ability['value'] = ability['value'] * roll

			# Do the text substitution
			ability['text'] = re.sub('\<(\w*)\+*\((\d+)\-(\d+)\)\>', str(roll), ability.get('text'), count=1)

		# Replace minion types
		while '<minion_type>' in ability.get('text'):
			random_type      = random.choice(MinionAbility.minion_types)
			ability['text']  = ability['text'].replace('<minion_type>', random_type, 1)

		#print("Built ability: %s" % ability)

		return MinionAbility(text=ability.get('text'), value=ability.get('value'))

class Card:
	def __init__(self):
		self.name = "Unnamed card"

	def generate_abilities(self):
		raise Exception("must implement generate_abilities in Card subclass")

	def ability_value(self):
		#print("Calculating cost")
		total_cost = sum([ability.value for ability in self.abilities])
		return total_cost

	def __str__(self):
		return "%s (%s), %s/%s %s %s: %s" % (
			self.name,
			self.cost,
			self.attack,
			self.health,
			self.hero,
			self.card_type,
			' '.join([ability.text for ability in self.abilities])
		)

	def to_csv(self):
		return "%s;%s;%s;%s;%s;%s;%s" % (
			self.name,
			self.cost,
			self.attack,
			self.health,
			self.hero,
			self.card_type,
			' '.join([ability.text for ability in self.abilities])
		)

class MinionCard(Card):
	value_per_attack_point = 0.57
	value_per_health_point = 0.40

	name_prefaces = [
		'Holy', 'Dark', 'Merchant', 'Lively', 'Blood', 'Furious', 'Death', 'Critical', 'High',
		'Fel', 'Time', 'Goblin', 'Elven', 'Shady', 'Deaf', 'Deadly', 'Arcane', 'Experienced',
		'Black', 'White', 'Gold', 'Silver', 'Green', 'Blue', 'Orange', 'Red', 'Grey', 'Shadow',
		'Silver Hand', 'Demonic', 'Wild', 'Power', 'Rowdy', 'Shattered', 'Sun', 'Moon',
		'Steamweedle', 'Parasitic', 'Lonely', 'Tauren', 'Murloc', 'Diabolic', 'Kvaldir',
		'Stealthy', 'Kabal', 'Babbling', 'Bubbling', 'Dragon', 'Armored', 'Jade', 'Diamond', 'Onyx',
		'Smoking', 'Coughing', 'Worthless', 'Awful', 'Bad', 'Wise', 'Tortured', 'Light',
		'Solemn', 'Divine', 'Zephyr', 'Electric', 'Amateur', 'Greedy', 'Humble', 'Skeletal',
		'Ancient', "Death's", 'Inspiring'
	]

	names = [
		'Knight', 'Soldier', 'Adventurer', 'Commander', 'Seeker', 'Priestess', 'Striker', 'Bomber',
		'Underground', 'Shade', 'Ghost', 'Apprentice', 'Wizard', 'Archer', 'Skullsplitter',
		'Medic', 'Destroyer', 'Reaver', 'Recruiter', 'Recruit', 'Demon', 'Conjurer', 'Monster',
		'Spellcaster', 'Keeper', 'Snake', 'Civilian', 'Sniper', 'Murloc', 'Mindbender',
		'Lifebender', 'Soulbender', 'Gatekeeper', 'Giant', 'Gargoyle', 'Vampire', 'Breadmaker',
		'Breeder', 'Grinder', 'Bloodsucker', 'Trapper', 'First Mate', 'Second Mate', 'Captain',
		'Master', 'Ogre', 'Alchemist', 'Kabalist', 'Gypsy', 'Merchant', 'Ambusher', 'Ninja',
		'Guardian', 'Squashbuckler', 'Brother', 'Whisperer', 'Initiate', 'Garbageman', 'Garbage',
		'Old Thing', 'Old One', 'Sergeant', 'Seer', 'Oracle', 'Beefcake', 'Bartender', 'Rager',
		'Bruiser', 'King', 'Queen', 'Bishop', 'Assassin', 'Barbarian', 'Sorcerer', 'Amazon',
		'Paladin', 'Predator', 'Banshee', 'Scourge', 'Marine', 'Scientist', 'Experiment', 'Mage',
		'Abomination', 'Wall'
	]

	def __init__(self):
		#print("Minion init")
		self.card_type = 'minion'
		self.hero = 'neutral'
		self.generate_name()
		self.generate_abilities()
		self.generate_stats()
		self.sanity_check_edges()

	def generate_name(self):
		self.name = ' '.join([
			random.choice(MinionCard.name_prefaces),
			random.choice(MinionCard.names)
		])

	def generate_abilities(self):
		#print('Generating minion abilities')
		self.abilities = []

		number_of_abilities = 1 #random.randint(1, 2)
		for a in range(0, number_of_abilities):
			self.abilities.append(MinionAbility.random())

	def generate_stats(self):
		#print('Generating minion stats')

		ability_value = self.ability_value()
		#print("Beginning with %s ability value" % ability_value)

		if ability_value >= 10:
			extra_value = random.uniform(0, 5)
		else:
			extra_value = random.uniform(0, 10 - ability_value)
		#print("Adding %s extra value in stats" % extra_value)

		attack_value_distribution = random.uniform(0.01, extra_value)
		self.attack = int(attack_value_distribution / MinionCard.value_per_attack_point)

		health_value_distribution = extra_value - attack_value_distribution
		self.health = int(health_value_distribution / MinionCard.value_per_health_point)

		self.cost = int(ability_value + extra_value)

	def sanity_check_edges(self):
		if self.cost < 0:
			self.cost = 0
		elif self.cost > 10:
			self.cost = 10

		if self.health < 1:
			self.health = 1


print('Name;Cost;Attack;Health;Class;Type;Effect')
for x in range(1, 10000):
	#print("Generating card %s" % x)

	card = MinionCard()
	print card.to_csv()