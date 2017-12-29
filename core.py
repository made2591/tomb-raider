# -*- coding: utf-8 -*-
import json, sys, time, random, urllib2, re
from BeautifulSoup import BeautifulSoup

# levels of game
LEVELS = [
	"https://www.wikiraider.com/index.php/Walkthrough:Caves"
	"https://www.wikiraider.com/index.php/Walkthrough:City_of_Vilcabamba",
	"https://www.wikiraider.com/index.php/Walkthrough:Lost_Valley",
	"https://www.wikiraider.com/index.php/Walkthrough:Tomb_of_Qualopec",
	"https://www.wikiraider.com/index.php/Walkthrough:St._Francis%27_Folly",
	"https://www.wikiraider.com/index.php/Walkthrough:Colosseum",
	"https://www.wikiraider.com/index.php/Walkthrough:Palace_Midas",
	"https://www.wikiraider.com/index.php/Walkthrough:The_Cistern",
	"https://www.wikiraider.com/index.php/Walkthrough:Tomb_of_Tihocan",
	"https://www.wikiraider.com/index.php/Walkthrough:City_of_Khamoon",
	"https://www.wikiraider.com/index.php/Walkthrough:Obelisk_of_Khamoon",
	"https://www.wikiraider.com/index.php/Walkthrough:Sanctuary_of_the_Scion",
	"https://www.wikiraider.com/index.php/Walkthrough:Natla%27s_Mines",
	"https://www.wikiraider.com/index.php/Walkthrough:Atlantis",
	"https://www.wikiraider.com/index.php/Walkthrough:The_Great_Pyramid"
]

# character printing pause
CHAR_PAUSE = 0

# exit command
EXIT_COMMAND = "exit"

# help command 
HELP_COMMAND = "help"

# columns shell dimensions
COLUMNS_DIM = 80

# starting sequence
STARTING_SEQUENCE = "> "

# default action
DEFAULT_ACTION = "move up"

# items keywords
ITESM_KEYWORDS = ["footprints", "key", "wolf", "wolves", "bear", "small medipack", "large medipack", "lever", "secret"]

# stopwords
STOPWORDS = ["the", "a", "with"]

# game structure
GAME = {
		"player":{
		  "name":"made2591",
		  "life":100,
		  "items":[],
		  "level":"cave"
		  "step":0,
		},
		"defaultMessages":{
			"default": "You can't do this right now.",
			"noWalk":[
				"You can't walk in this direction.",
				"It is not the right thing to do..."
			],
			"noRun":[
				"You can't run in this direction.",
				"It is not the right thing to do..."
			],
			"noJump":[
				"You can't jump here.",
				"It is not the right thing to do..."
			],		
			"noClimb":[
				"You can't climb here.",
				"It is not the right thing to do..."
			],
			"noCome":[
				"You can't do this now.",
				"It is not the right thing to do..."
			],
			"noExamine":[
				"There is nothing strange here.",
				"You can't see no more...",
				"It is not the right thing to do..."
			],
			"noGet":[
				"There is nothing on the floor.",
				"Nothing useful in the scene.",
				"It is not the right thing to do..."
			],
			"noUse":[
				"It is not the right thing to do...",
				"Maybe later",
				"You don't have this item in your pocket"
			],
			"noSave":[
				"No diamond on the horizon..."
			]
		},
		"actions":{
		  "walk":{
		     "usageMessage":"The WALK command lets Lara moving slow into the scenario. If Lara is not stucked by something in the scene, or there's any reason why she can not move, you will be always able to walk. You can move in a specific direction in the scene using the command WALK [STRAIGHT/DOWN/LEFT/RIGHT]. Note: if you type and execute WALK, you will WALK STRAIGHT by default."
		  },
		  "run":{
		     "usageMessage":"The RUN command lets Lara moving fast in the scene. If Lara is not stucked by something in the scene, or there's any reason why she can not move, you will be always able to run. You can move in a specific direction in the scene using the command RUN [STRAIGHT/DOWN/LEFT/RIGHT]. Note: if you type and execute RUN, you will RUN STRAIGHT by default."
		  },
		  "jump":{
		     "usageMessage":"The JUMP command lets Lara jump into the scenario. If Lara is not stucked by something in the scene, or there's any reason why she can not move, you will be always able to jump. The jump command automatically setup the number of steps needed and eventually let Lara hang on the edge. You can jump in a specific direction in the scene using the command JUMP [STRAIGHT/DOWN/LEFT/RIGHT]. Note: if you type and execute JUMP, you will JUMP STRAIGHT by default."
		  },
		  "climb":{
		     "usageMessage":"The CLIMB command lets Lara climb up/on something in the scene. You won't be always able to climb: Lara need something to climb up/on to complete this action. You can climb in the scene using the command CLIMB [UP/ON] [SOMETHING]. Note: if you type and execute CLIMB without specific element, Lara won't complete the action."
		  },
		  "come":{
		     "usageMessage":"The COME command lets Lara get off gently from high places. You won't be always able to come: Lara need something to come up/down to complete this action. Use the command COME [UP/DOWN] to . Note: if you type and execute COME, you will COME STRAIGHT by default."
		  },
		  "examine":{
		     "usageMessage":"The EXAMINE action is useful to help you explore the scene or a particular item in the scene. You can examine the scene using simply EXAMINE. If you try to examine an item you don't have in your pocket, the examine action will fail and nothing happens. You can examine an item using the command EXAMINE [ITEM_NAME] with the name of an item in the scene."
		  },
		  "get":{
		     "usageMessage":"The GET action is used to get an item from the scene. If there are no items in the scene, nothing will be added to your pocket. You can get an item using the command GET [ITEM_NAME] with the name of an item in the scene."
		  },
		  "use":{
		     "usageMessage":"The USE action is used to use an item you hold. If you can't use the item in the scene than the item will remain in your pocket. You can use an item using the command USE [ITEM_NAME] with the name of an item in the scene."
		  },
		  "save":{
		     "usageMessage":"The SAVE action is used to save the game. You can save the game only when you meet a SAVE DIAMOND in the scene, using the command SAVE."
		  }
		},
		"levels":{
			"cave" : {
				"levelDescription": "Welcome to Tomb Raider I. You will interprete the role of Lara, a British archaeologist and treasure hunter, most commonly known for her discovery of several noted artefacts, including Excalibur, the fabled sword of King Arthur. You was hired by Jacqueline Natla to travel to the Andes mountain range, in Peru, in search of an artefact known as the Scion, which rests in the Tomb of Qualopec somewhere in the mountains. Accompanied by a guide you arrived at a huge pair of stone doors, the entrance to an ancient Incan civilisation. You climbed to the top of the doors and found a hidden switch that opens the doors. A pack of ferocious wolves suddenly attacked you from inside the cave. You leaped to the ground, killing the wolves in a barrage of pistol fire. However, you are too late, and your guide is dead in the snow. Alone, you headed into the caves in search for the village Vilcabamba.", 
				"steps" : {}
			}
		}
}

# getting the raw data and manually copy the source for each level
def getLinksLevel():

	# get level page
	html_page = urllib2.urlopen("https://www.wikiraider.com/index.php/Tomb_Raider#Levels")

	# create parser
	soup = BeautifulSoup(html_page)

	# create list of links
	links = []

	# for each link
	for link in soup.findAll('a'):

		# raw cleaning 
		if link.get('href') != None and "/index.php/" in link.get('href') and "jpg" not in link.get('href') and "gif" not in link.get('href'):
			links.append(link.get('href'))

	# return list
	return links

# create game starting from sentences in source and fill the game structures
def createGame(defaultAction = DEFAULT_ACTION):

	# separate lines
	with open("./levels/caves.txt", "r") as f:
		
		# read each lines
		lines = f.readlines()

		# accumulate steps
		steps = []
		for line in lines:
			steps += line.split(".")
	
	# clean steps
	steps = [x.strip().replace("\n","") for x in steps if x != "\n" or len(x.strip().replace("\n","")) > 1]

	# for each step
	for index, step in enumerate(steps):

		# create level structure
		game["levels"]["cave"]["steps"][index] = {
			"stateDescription" : step,
			"availableItems" : [],
			"availableActions" : {},
		}

		# insert items
		for keyword in ITESM_KEYWORDS:
			
			# check if keyword of item appears in state description and it not already added to items list
			if keyword in step and keyword.lower().strip() not in game["levels"]["cave"]["steps"][index]["availableItems"]:

				# add to items
				availableItems.append(keyword.lower().strip())

		# create level structure
		game["levels"]["cave"]["steps"][index]["availableActions"] = {
			"walk" : index+1,
			"walk straight" : index+1,
			"walk back" : "",
			"walk left" : "",
			"walk right" : "",
			"run" : index+1,
			"run straight" : index+1,
			"run back" : "",
			"run left" : "",
			"run right" : "",
			"examine" : "",
			"get" : "",
			"use" : "",
			"save": ""
		}

	# for index, state in enumerate(states):
	# 	print "\ta"+str(index)+"[ label=\""+state+"\" ];"
	# 	if index > 0 and index % 2 == 1:
	# 		print "\ta"+str(index-1)+" -> a"+str(index)+" [ label=\""+defaultAction+"\" ];"

	# save output game
	with open("./levels/caves_base.json", "wb") as f:

		# save json output
		f.write(json.dumps(game, indent=4, ensure_ascii=False, sort_keys=True))

# simulate printing of sentence for vintage gaming experience
def printSentence(sentence, pause = CHAR_PAUSE, columns = COLUMNS_DIM):

	# create counter
	counter = 0

	# for each char in the sentence
	for character in sentence:

		# split sentence if the number of columns is reached 
		if counter > columns:

			# go ahead
			sys.stdout.write("\n")

			# if the sentence starts with tab
			for tab in sentence:

				# print the exactly number of tab in front of the new line
				if tab == "\t":
					sys.stdout.write(tab)
				else:
					break
			# if the sentence start with starting sequence
			if sentence[0:2] == STARTING_SEQUENCE:

				# print the starting sequence in front of the new line
				sys.stdout.write(STARTING_SEQUENCE)

			# reset column counter
			counter = 0

		# else print the next character
		else:
			sys.stdout.write(character)

		# flush output
		sys.stdout.flush()

		# pause
		time.sleep(pause)

		# increment columns counter
		counter += 1


def playGame():

	# load game from file
	game = json.loads((open("./levels/caves_base.json", "r").read()))

	# vintage print welcome sentence
	printSentence(STARTING_SEQUENCE+game["levels"]["cave"]["levelDescription"], 
				  pause = 0.03, 
				  columns = 80)

	# get states sorted
	states = sorted(game["levels"]["cave"]["states"].keys())

	# spacing and start of game	
	print "\n\n"
	raw_input(STARTING_SEQUENCE)

	# set actual state to the first in sequence
	actualState = states[0]

	# set the final state to the last in sequence
	finalState  = states[-1]

	# while the actual state is different from the final state
	while actualState != finalState:

		# spacing
		print "\n"

		# get description of the state
		stateDescription = game["levels"]["cave"]["states"][actualState]["stateDescription"]		

		# get available actions in the state
		availableActions = game["levels"]["cave"]["states"][actualState]["availableActions"]

		# vintage print state description
		printSentence(STARTING_SEQUENCE+stateDescription, 
					  pause = 0.03, 
					  columns = 80)

		# go on until needed
		continueLooping = True
		while continueLooping:

			# spacing
			print "\n"

			# ask the player for the action
			choice = raw_input(STARTING_SEQUENCE)

			# if the typed choice is in the available actions set
			if choice in availableActions.keys():

				# if the action let Lara move forward to next state
				if game["levels"]["cave"]["states"][actualState]["availableActions"][choice] != "": 

					# update the actual state to the next state for the action and stop looping
					actualState = game["levels"]["cave"]["states"][actualState]["availableActions"][choice]

					# stop looping
					continueLooping = False

				# epsilon move in the actual state: print a random message from the action taken
				else:

					matchAction = False

					# for each action in defaultMessages set
					for action in game["defaultMessages"].keys():

						# if choice match the action key
						if choice.strip().lower() in action.strip().lower():

							# pick up a random message for that action:
							randomMessage = random.randint(0, len(game["defaultMessages"][action])-1)

							# vintage print the message
							printSentence(game["defaultMessages"][action][randomMessage])
							matchAction = True
							break

					# if choice doesn't match any action key
					if not matchAction:

						# vintage print the message
						printSentence(game["defaultMessages"]["default"], 
									  pause = 0, 
									  columns = 80)

			# if the choice the help command
			elif choice == HELP_COMMAND:

				# pretty print help welcome
				print STARTING_SEQUENCE+"Available commands:\n"

				# for each available action in the game
				for action in game["actions"]:

					# vintage print the action name
					printSentence("- "+action.upper())
					print "\n"

					# vintage print the action manual
					printSentence("\t"+game["actions"][action]["usageMessage"], CHAR_PAUSE, columns = COLUMNS_DIM-6)
					print "\n"

					# wait for input
					raw_input("")

			# if the choice is the global available set
			else:

				# vintage print the message
				printSentence(game["defaultMessages"]["default"], 
							  pause = 0, 
							  columns = 80)

createGame()
#playGame()







