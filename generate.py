import random #random.choice
import copy #copy.copy
import re

class Ability:
	templates = [
		{'value': -0.30, 'text': 'Choose One - <targetable_effect>; or <targetable_effect>.'},
		{'value': -0.30, 'text': 'Choose One - <effect>; or <effect>.'},
		{'value': -0.30, 'text': 'When you draw this card, <effect>.'},
		{'value': -0.30, 'text': 'When this card is discarded, <effect>.'},
	]

	conditions = [
		{'value': -5.0, 'text': 'your deck has no more than 1 of any card' },
		{'value': 1.40, 'text': 'your deck has at least <(2-20)> <minion_type>s'},
		{'value': 1.40, 'text': 'your deck has no more than <i+(2-20)> <minion_type>s'},
		{'value': 0.00, 'text': 'you have at least <i+(2-8)> cards in hand'},
		{'value': 0.00, 'text': 'your hand is empty'},
		{'value': 0.00, 'text': 'you control no minions'},
		{'value': 0.00, 'text': 'your opponent has at least <i+(1-6)> minions'},
		{'value': 0.00, 'text': 'you control a Secret'},
		{'value': -0.50, 'text': 'your opponent controls a Secret'},
	]

	triggers = [
		{'value': 2.00, 'text': 'you receive fatal damage'},
		{'value': 0.20, 'text': 'you draw a card'},
		{'value': 0.20, 'text': 'you discard a card'},
		{'value': 0.20, 'text': 'your opponent draws a card'},
		{'value': 0.20, 'text': 'your hero is attacked'},
		{'value': 0.20, 'text': 'a friendly minion is attacked'},
		{'value': 0.20, 'text': 'your opponent casts a spell'},
		{'value': 0.20, 'text': 'a spell is cast'},
		{'value': 0.20, 'text': 'a spell is cast targeting a minion'},
		{'value': 0.20, 'text': 'an enemy minion is summoned'},
		{'value': 0.20, 'text': 'a <minion_type> is summoned'},
		{'value': -1.4, 'text': 'a minion with <ability> is summoned'},
		{'value': -2.0, 'text': 'a <minion_type> with <ability> is summoned'},
		{'value': 0.20, 'text': 'a <card_type> is played'},
		{'value': 0.20, 'text': 'your opponent uses their Hero Power'},
		{'value': 0.20, 'text': 'a <minion_type> dies'},
		{'value': 0.20, 'text': 'a weapon is equipped'},
		{'value': 0.20, 'text': 'a weapon is broken'},
		{'value': 0.20, 'text': 'a weapon loses durability'},
		{'value': 0.20, 'text': 'you gain Armor'},
		{'value': 0.20, 'text': 'a minion takes damage'},
		{'value': 0.20, 'text': 'a minion is healed'},
		{'value': 0.20, 'text': 'a Hero is healed'},
		{'value': 0.20, 'text': 'more than <i+(1-10)> Health is restored in a turn'},
	]

	effects = [
		{'value': 1.84, 'text': 'Draw a card'},
		{'value': 1.00, 'text': 'Draw <V+(2-4)> cards'},
		{'value': -1.25, 'text': 'Discard a card'},
		{'value': -1.98, 'text': 'Your opponent draws a card'},
		{'value': -0.27, 'text': 'Deal <q+(1-10)> damage to your hero'},
		{'value': -0.27, 'text': 'Deal <q+(1-10)> damage to a random allied character'},
		{'value': 0.27, 'text': 'Deal <q+(1-10)> damage to a random enemy'},
		{'value': -1.27, 'text': 'Destroy a Mana Crystal'},
		{'value': 0.75, 'text': 'Equip a random weapon'},
		{'value': 0.15, 'text': 'Add a random weapon to your hand'},
		{'value': 1.31, 'text': 'Your <minion_type>s gain <stackable_effect>'},
		{'value': 1.31, 'text': 'Your <minion_type>s gain "<ability_aura>"'},
		{'value': 0.31, 'text': 'Give a random friendly minion <ability>'},
		{'value': 0.31, 'text': 'Give a random friendly minion "<ability_aura>"'},
		{'value': 0.31, 'text': 'Give a random friendly minion <stackable_effect>'},
		{'value': 2.33, 'text': 'Put a <minion_type> from your hand into play'},
		{'value': 0.42, 'text': 'Summon a random <v+(0-10)>-Cost minion'},
		{'value': 0.42, 'text': 'Restore <v+(1-10)> Health to a random character'},
		{'value': 0.22, 'text': 'Gain <v+(1-10)> Armor'},
		{'value': 0.33, 'text': 'The next <minion_type> you play costs Health instead of mana'},
		{'value': 2.33, 'text': 'Summon a random <minion_type>'},
		{'value': 4.33, 'text': 'Give all <minion_type>s in your hand and deck <stackable_effect>'},
		{'value': -5.0, 'text': 'Destroy a random friendly minion'},
		{'value': 4.20, 'text': 'Destroy all <minion_type>s'},
	]

	targetable_effects = [
		{'value': 0.82, 'text': 'Deal <v+(0-8)> damage to a minion'},
		{'value': 0.82, 'text': 'Deal <v+(1-6)> damage to an enemy character'},
		{'value': 1.84, 'text': 'Deal <V+(0-8)> damage to all enemy minions'},
		{'value': 5.33, 'text': 'Destroy a minion'},
		{'value': 2.73, 'text': 'Destroy a <minion_type>'},
		{'value': 1.02, 'text': 'Freeze a minion'},
		{'value': 0.42, 'text': 'Freeze a <minion_type>'},
		{'value': 0.23, 'text': 'Silence a minion'},
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

	abilities = [
		{'value': -0.83, 'text': 'Overload (<i+(1-3)>)'},
	]

	ability_auras = [
		{'value': 3.40, 'text': 'Your Hero is Immune'},
		{'value': 0.36, 'text': 'Your spells cost (<v+(1-3)>) less'},
		{'value': 0.26, 'text': 'Your minions cost (<v+(1-3)>) less'},
		{'value': 0.06, 'text': 'Your weapons cost (<v+(1-3)>) less'},
		{'value': 0.36, 'text': 'Your spells cost (<i+(1-3)>) more'},
		{'value': 0.26, 'text': 'Your minions cost (<i+(1-3)>) more'},
		{'value': 0.06, 'text': 'Your weapons cost (<i+(1-3)>) more'},
		{'value': 0.33, 'text': 'Your Hero Power costs (<V+(1-2)>) less'},
		{'value': -0.53, 'text': "Your opponent's Hero Power costs (<V+(1-2)>) less"},
		{'value': 0.53, 'text': "Your weapon has +<v+(1-3)> Attack"},
	]

	stackable_effects = [
		{'value': 0.57, 'text': '+<v+(1-5)> Attack'},
		{'value': 0.40, 'text': '+<v+(1-5)> Health'},
		{'value': 1.10, 'text': '+<v+(1-5)>/+<v+(1-5)>'},
		{'value': 1.46, 'text': 'Spell Power +1'},
	]

	minion_types = [
		'Beast', 'Dragon', 'Murloc', 'Demon', 'Mech', 'Pirate', 'Totem'
	]

	card_types = [
		'minion', 'spell', 'weapon'
	]

	def __init__(self, text="", value=0):
		self.text = text
		self.value = value

	@classmethod
	def replace_tokens(ability_subclass, ability):
		while '<effect>' in ability.get('text'):
			random_effect    = random.choice(ability_subclass.effects)
			ability['text']  = ability['text'].replace('<effect>', random_effect.get('text'), 1)
			ability['value'] = ability['value'] + random_effect.get('value')

		while '<targetable_effect>' in ability.get('text'):
			random_effect    = random.choice(ability_subclass.targetable_effects)
			ability['text']  = ability['text'].replace('<targetable_effect>', random_effect.get('text'), 1)
			ability['value'] = ability['value'] + random_effect.get('value')

		while '<stackable_effect>' in ability.get('text'):
			random_effect    = random.choice(ability_subclass.stackable_effects)
			ability['text']  = ability['text'].replace('<stackable_effect>', random_effect.get('text'), 1)
			ability['value'] = ability['value'] + random_effect.get('value')

		while '<condition>' in ability.get('text'):
			condition        = random.choice(ability_subclass.conditions)
			ability['text']  = ability['text'].replace('<condition>', condition.get('text'), 1)
			ability['value'] = ability['value'] + condition.get('value')

		while '<ability>' in ability.get('text'):
			random_ability   = random.choice(ability_subclass.abilities)
			ability['text']  = ability['text'].replace('<ability>', random_ability.get('text'), 1)
			ability['value'] = ability['value'] + random_ability.get('value')

		while '<ability_aura>' in ability.get('text'):
			random_ability   = random.choice(ability_subclass.ability_auras)
			ability['text']  = ability['text'].replace('<ability_aura>', random_ability.get('text'), 1)
			ability['value'] = ability['value'] + random_ability.get('value')

		while '<minion_type>' in ability.get('text'):
			random_type      = random.choice(ability_subclass.minion_types)
			ability['text']  = ability['text'].replace('<minion_type>', random_type, 1)

		while '<trigger>' in ability.get('text'):
			random_trigger   = random.choice(ability_subclass.triggers)
			ability['text']  = ability['text'].replace('<trigger>', random_trigger.get('text'), 1)

		while '<card_type>' in ability.get('text'):
			random_type      = random.choice(ability_subclass.card_types)
			ability['text']  = ability['text'].replace('<card_type>', random_type, 1)

		#TODO: clean all this up so ordering doesn't matter

		while '<ability>' in ability.get('text'):
			random_ability   = random.choice(ability_subclass.abilities)
			ability['text']  = ability['text'].replace('<ability>', random_ability.get('text'), 1)
			ability['value'] = ability['value'] + random_ability.get('value')

		while '<minion_type>' in ability.get('text'):
			random_type      = random.choice(ability_subclass.minion_types)
			ability['text']  = ability['text'].replace('<minion_type>', random_type, 1)

		return ability

	@classmethod
	def roll_variables(ability_subclass, ability):
		while True:
			match = re.search('\<(\w*)\+*\((\d+)\-(\d+)\)\>', ability.get('text'))
			if not match:
				return ability

			flags, lower_bound, upper_bound = match.group(1), match.group(2), match.group(3)
			roll = random.randint(int(lower_bound), int(upper_bound))

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

	@classmethod
	def random(ability_subclass):
		ability = copy.copy(random.choice(ability_subclass.templates))
		ability = ability_subclass.replace_tokens(ability)
		ability = ability_subclass.roll_variables(ability)

		return ability_subclass(text=ability.get('text'), value=ability.get('value'))

class MinionAbility(Ability):
	templates = Ability.templates + [
		{'value': 0.00, 'text': '<ability>.' },
		{'value': 0.20, 'text': 'Battlecry: <effect>.'},
		{'value': 0.20, 'text': 'Battlecry: <targetable_effect>.'},
		{'value': 0.20, 'text': 'Battlecry: If <condition>, <targetable_effect>.'},
		{'value': 0.30, 'text': 'Battlecry: If <condition>, <targetable_effect> and <effect>.'},
		{'value': 2.50, 'text': 'Battlecry: Gain <stackable_effect> for every spell in your hand.'},
		{'value': 2.50, 'text': 'Battlecry: Gain <stackable_effect> for every minion in your hand.'},
		{'value': 0.20, 'text': 'Deathrattle: <effect>.'},
		{'value': 0.50, 'text': 'Inspire: <effect>.'},
		{'value': 0.50, 'text': 'Inspire: Gain <stackable_effect>.'},
		{'value': 0.50, 'text': 'Inspire: Gain "<ability_aura>".'},
		{'value': 0.50, 'text': 'At the beginning of your turn, <effect>.'},
		{'value': 0.50, 'text': 'At the end of your turn, gain <ability>.'},
		{'value': 0.50, 'text': 'At the end of each turn, <effect>.'},
		{'value': 0.20, 'text': 'Enrage: <ability_aura>.'},
		{'value': 0.20, 'text': 'Has <ability> while <condition>.'},
		{'value': 0.30, 'text': 'Your <minion_type>s are <minion_type>s.'},
		{'value': 0.30, 'text': 'Your <minion_type>s gain <stackable_effect>.'},
		{'value': 0.30, 'text': 'Your <minion_type>s gain <ability>.'},
		{'value': -1.30, 'text': 'Choose One - Gain <ability>; or Gain <ability>.'},
		{'value': -1.30, 'text': 'Choose One - <ability_aura>; or <ability_aura>.'},
		{'value': 0.30, 'text': 'Whenever this minion attacks, <effect>.'},
		{'value': 0.30, 'text': 'After this attacks and kills a minion, <effect>.'},
		{'value': 0.30, 'text': 'Whenever this minion takes damage, <effect>.'},
		{'value': 0.30, 'text': 'Whenever <trigger>, <effect>.'},
		{'value': -1.30, 'text': 'Whenever this minion loses <ability>, <effect>.'},
		{'value': -1.30, 'text': 'Whenever this minion gains <ability>, <effect>.'},
		{'value': 1.30, 'text': 'Adjacent minions have <stackable_effect>.'},
		{'value': 0.20, 'text': 'Combo: <effect>.'},
		{'value': 0.20, 'text': 'Combo: <targetable_effect>.'},
		{'value': 1.00, 'text': 'Costs (<v+(1-4)>) less for each <minion_type> you control.'},
	]

	effects = Ability.effects + [
		{'value': -0.27, 'text': 'Deal <q+(1-10)> damage to HIMSELF'},
		{'value': 1.31, 'text': 'Your other minions gain <stackable_effect>'},
		{'value': 1.31, 'text': 'Your other minions gain "<ability_aura>"'},
		{'value': 0.31, 'text': 'Gain <stackable_effect> for every <minion_type> in your hand'},
		{'value': 0.31, 'text': 'Gain <ability> until end of turn'},
		{'value': 0.31, 'text': 'Gain <stackable_effect> for each damaged minion on the battlefield'},
		{'value': 0.33, 'text': 'Return this minion to your hand'},
		{'value': 0.20, 'text': 'Shuffle this minion into your deck'},
		{'value': -0.70, 'text': "Shuffle this minion into your opponent's deck"},
		{'value': -1.27, 'text': 'Destroy <i+(2-5)> of your Mana Crystals'},
	]

	targetable_effects = Ability.targetable_effects + [
		{'value': 1.42, 'text': "Deal damage equal to this minion's Attack"},
		{'value': 1.42, 'text': "Deal damage equal to this minion's Health"},
	]

	abilities = Ability.abilities + [
		{'value': 0.51, 'text': 'Taunt'},
		{'value': 1.40, 'text': 'Divine Shield'},
		{'value': 1.19, 'text': 'Windfury'},
		{'value': 5.40, 'text': 'Mega-Windfury'},
		{'value': 0.46, 'text': 'Spell Power +<v+(1-3)>'},
		{'value': 0.33, 'text': 'Charge'},
		{'value': 0.61, 'text': 'Stealth'},
		{'value': -0.83, 'text': "Can't attack"},
	]

	ability_auras = Ability.ability_auras + [
		{'value': -0.53, 'text': "50% chance to attack the wrong target"},
		{'value': 0.33, 'text': "Can't be targeted by spells or Hero Powers"},
	]

class SpellAbility(Ability):
	templates = [
		{'value': 0.00, 'text': 'Secret: When <trigger>, <effect>.'},
		{'value': 0.00, 'text': '<effect>.'},
		{'value': 0.00, 'text': '<targetable_effect>.'},
		{'value': 2.00, 'text': 'Give your minions <ability> until end of turn.'},
		{'value': 2.00, 'text': 'Give your minions "<ability_aura>" until end of turn.'},
		{'value': 2.00, 'text': 'Give your minions <stackable_effect> until end of turn.'},
		{'value': 2.00, 'text': 'Give your minions <stackable_effect>.'},
		{'value': 0.00, 'text': 'Give a random minion in your hand <ability>.'},
		{'value': 0.00, 'text': 'Give a random minion in your hand "<ability_aura>".'},
		{'value': 0.00, 'text': 'Give a random minion in your hand <stackable_effect>.'},
		{'value': -3.00, 'text': 'Give a random minion in your deck <ability>.'},
		{'value': -3.00, 'text': 'Give a random minion in your deck "<ability_aura>".'},
		{'value': -3.00, 'text': 'Give a random minion in your deck <stackable_effect>.'},
		{'value': 0.20, 'text': 'If <condition>, <targetable_effect>. Otherwise, <effect>.'},
		{'value': 0.20, 'text': 'If <condition>, <targetable_effect>. Otherwise, <targetable_effect>.'},
		{'value': 0.30, 'text': 'If <condition>, <targetable_effect> and <effect>.'},
		{'value': 2.50, 'text': '<effect> for every spell in your hand.'},
		{'value': 2.50, 'text': '<effect> for every minion in your hand.'},
		{'value': 2.50, 'text': '<targetable_effect> for every minion in your hand.'},
		{'value': 2.50, 'text': '<targetable_effect> for every spell in your hand.'},
		{'value': 0.00, 'text': 'Give your <ability> minions <ability>.'},
		{'value': 0.50, 'text': 'At the beginning of your next turn, <effect>.'},
		{'value': 0.50, 'text': 'At the end of your turn, <effect>.'},
		{'value': 0.30, 'text': 'Whenever <trigger> this turn, <effect>.'},
		{'value': 0.20, 'text': 'Combo: <effect>.'},
		{'value': 0.20, 'text': 'Combo: <targetable_effect>.'},
		{'value': 1.00, 'text': 'Costs (<v+(1-4)>) less for each <minion_type> you control.'},
	]

class Card:
	def __init__(self):
		self.name = "Unnamed card"
		self.cost = 0
		self.hero = 'neutral'
		self.card_type = 'UNKNOWN'

	def ability_value(self):
		sum([ability.value for ability in self.abilities])
		return sum([ability.value for ability in self.abilities])

	def __str__(self):
		return "%s (%s) %s %s: %s" % (
			self.name,
			self.cost,
			self.hero,
			self.card_type,
			' '.join([ability.text for ability in self.abilities])
		)

	def to_csv(self):
		return "%s;%s;%s;%s;%s" % (
			self.name,
			self.cost,
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
		self.card_type = 'minion'
		self.hero = 'neutral'

		self.name = self.random_name()
		self.abilities = self.random_abilities()
		self.cost, self.attack, self.health = self.generate_stats()

		self.sanity_check_edges()

	def random_name(self):
		return ' '.join([
			random.choice(MinionCard.name_prefaces),
			random.choice(MinionCard.names)
		])

	def random_abilities(self):
		abilities = []

		number_of_abilities = 1 #random.randint(1, 2)
		for a in range(0, number_of_abilities):
			abilities.append(MinionAbility.random())

		return abilities

	def generate_stats(self):
		ability_value = self.ability_value()

		if ability_value > 10:
			extra_value = random.uniform(0, 5)
		elif ability_value < 0:
			extra_value = random.uniform(-ability_value, 10)
		else:
			extra_value = random.uniform(0, 10 - ability_value)

		attack_value_distribution = random.uniform(0.01, extra_value)
		attack = int(attack_value_distribution / MinionCard.value_per_attack_point)

		health_value_distribution = extra_value - attack_value_distribution
		health = int(health_value_distribution / MinionCard.value_per_health_point)

		cost = int(round(ability_value + extra_value))

		return cost, attack, health

	def sanity_check_edges(self):
		if self.cost < 0:
			self.cost = 0
		elif self.cost > 10:
			self.cost = 10

		if self.health < 1:
			self.health = 1

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

class SpellCard(Card):
	def __init__(self):
		self.card_type = 'spell'
		self.hero = 'neutral'

		self.name = 'Unnamed spell'
		self.abilities = self.random_abilities()
		self.cost = int(round(self.ability_value()))

		self.sanity_check_edges()

	def random_abilities(self):
		abilities = []

		number_of_abilities = 1 #random.randint(1, 2)
		for a in range(0, number_of_abilities):
			abilities.append(SpellAbility.random())

		return abilities

	def sanity_check_edges(self):
		if self.cost < -1:
			self.abilities.append(Ability(value=1, text='Draw a card.'))
			self.cost = 1
		elif self.cost < 0:
			self.cost = 0
		elif self.cost > 10:
			self.cost = 10

print('Name;Cost;Attack;Health;Class;Type;Effect')
for x in range(1, 100):

	if random.randint(0, 1) == 0:
		card = MinionCard()
	else:
		card = SpellCard()

	print card.to_csv()