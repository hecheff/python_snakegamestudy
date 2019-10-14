#Python Study: Understanding command inputs and screen output to create crude interactive UI
#Based on tutorial found here: https://www.youtube.com/watch?v=rbasThWVb-c
#Modifications made:
# - Lose condition shown when window closed by player loss, including "GAME OVER" message
# - Bug fix: Direction change causing reverse movement (causing player to eat themself)
# - Initial player snake length can be easily set by changing one variable (instead of static preset)

#Important Notes before running this script: 
# - On Windows, this file must be run through the command line. 
#	- Otherwise window issues will occur if run directly on code editors.
# - 'curses' module is not natively available on Windows. Separate add-on used to allow this to work.

import random	#Needed for generating randomized spawn points for food item
import curses	#Library for screen-painting and handling keyboard inputs

#Initialize screen drawing
s = curses.initscr()				
curses.curs_set(0)					
sh, sw = s.getmaxyx()				#Establish max screen height and width
w = curses.newwin(sh, sw, 0, 0)     #Declare and set window variable's size and dimensions
w.keypad(1)                         #Set window keypad
w.timeout(200)						#Set window srefresh rate of window (ms)

#Establish player snake's initial spawn position
snake_x = sw/4      #Horizontal starting point (x-axis). Start at 1/4 left of window.
snake_y = sh/2      #Veritcal starting point (y-axis). Start at vertical middle of window.

#Set snake's head+body array and initial positon
snakeSpawnLength = 5    #Set snake's spawn length. Change this to modify starting length of player snake
lengthCountUp = 1       #Initial increment value. DO NOT CHANGE THIS

snake = [[snake_y, snake_x]]    #Player snake list
while lengthCountUp < snakeSpawnLength:
    #Set player snake initial length
    snake.append([snake_y, snake_x - lengthCountUp])
    lengthCountUp += 1

#Set food item variables
food = [sh/2, sw/2]                                     #Initial position of first food item (center of window)
w.addch(int(food[0]), int(food[1]), curses.ACS_PI)      #Add food item to window

key = curses.KEY_RIGHT  #Set initial last input default

#Loop until interrupted when player loses
while True:
	#Check player status
    #Lose Conditions: 
    # - Player snake head goes outside boundaries
    # - Player snake head goes inside space which is part of body
    if snake[0][0] in [0, sh] or snake[0][1] in [0, sw] or snake[0] in snake[1:]:
        #Output cause of player loss
        if snake[0][0] in [0, sh] or snake[0][1] in [0, sw]:
            print("Player crashed into wall boundary")
        elif snake[0] in snake[1:]:
            print("Player crashed into self")
        
        curses.endwin()         #Close opened window
        print("GAME OVER")
        quit()
    
    
    next_key = w.getch()                #Listen for keyboard inputs
    changeDirectionCommand = False      #(Re)set flag for determining whether to change direction
	
	#Set status of key
	#No change if no inputs detected in frame, otheerwise set to new key input
	#Set change direction flag to true if keyboard input is different axis movement (e.g. When moving up/down, only allow moving left/right, etc.)
    #   - Added to prevent player from eating themselves
    if key == curses.KEY_DOWN or key == curses.KEY_UP:
        #Check vertical movement
        if next_key != curses.KEY_DOWN and next_key != curses.KEY_UP:
            changeDirectionCommand = True
    
    elif key == curses.KEY_LEFT or key == curses.KEY_RIGHT:
        #Check horizontal movement
        if next_key != curses.KEY_LEFT and next_key != curses.KEY_RIGHT:
            changeDirectionCommand = True
    
    #If change direction flag is true, update this
    if changeDirectionCommand == True:
        key = key if next_key == -1 else next_key

	#Set new location of player's snake head
    new_head = [int(snake[0][0]), int(snake[0][1])]
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1
    snake.insert(0, new_head)

    #Make playeer snake react when head touches food item
    if snake[0] == food:
        food = None
        while food is None:
            #Respawn food item in random location not overlapping Snake
            nf = [
                random.randint(1, sh-1),
                random.randint(1, sw-1)
            ]
            food = nf if nf not in snake else None
        w.addch(int(food[0]), int(food[1]), curses.ACS_PI)
    else:
        tail = snake.pop()
        w.addch(int(tail[0]), int(tail[1]), ' ')
    
    w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)