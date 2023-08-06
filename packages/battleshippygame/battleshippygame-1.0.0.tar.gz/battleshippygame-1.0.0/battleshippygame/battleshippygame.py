import os, time, random



BATTLESHIP = r"""
██████╗░░█████╗░████████╗████████╗██╗░░░░░███████╗░██████╗██╗░░██╗██╗██████╗░██╗
██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║░░░░░██╔════╝██╔════╝██║░░██║██║██╔══██╗██║
██████╦╝███████║░░░██║░░░░░░██║░░░██║░░░░░█████╗░░╚█████╗░███████║██║██████╔╝██║
██╔══██╗██╔══██║░░░██║░░░░░░██║░░░██║░░░░░██╔══╝░░░╚═══██╗██╔══██║██║██╔═══╝░╚═╝
██████╦╝██║░░██║░░░██║░░░░░░██║░░░███████╗███████╗██████╔╝██║░░██║██║██║░░░░░██╗
╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚══════╝╚══════╝╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░╚═╝"""



alpha = ["a", "b", "c", "d", "e"]
num = ["1", "2", "3", "4", "5"]
usedcoordsai = []
usedcoordsplayer = []
aiattackedtargetcount = 0
playerattackedtargetcount = 0



withoutshipai = ["a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3", "b4", "b5", "c1", "c2", "c3", "c4", "c5", "d1", "d2", "d3", "d4", "d5", "e1", "e2", "e3", "e4", "e5"]
withshipai = random.sample(withoutshipai, 4)
withoutshipai = [x for x in withoutshipai if x not in withshipai]
withoutshipplayer = ["a1", "a2", "a3", "a4", "a5", "b1", "b2", "b3", "b4", "b5", "c1", "c2", "c3", "c4", "c5", "d1", "d2", "d3", "d4", "d5", "e1", "e2", "e3", "e4", "e5"]
withshipplayer = random.sample(withoutshipplayer, 4)
withoutshipplayer = [x for x in withoutshipplayer if x not in withshipplayer]



bar = ["[█             ]", 
       "[██            ]", 
       "[███           ]", 
       "[████          ]", 
       "[█████         ]", 
       "[██████        ]", 
       "[███████       ]", 
       "[████████      ]", 
       "[█████████     ]", 
       "[██████████    ]", 
       "[███████████   ]", 
       "[████████████  ]", 
       "[█████████████ ]", 
       "[██████████████]"]
barcontrol = 0



def loadingscreen(loadingtext):
       global bar
       global barcontrol
       while True:
              if barcontrol < 14:
                     print(loadingtext + bar[barcontrol % len(bar)], end="\r")
                     time.sleep(0.1)
                     barcontrol += 1
              else:
                     #The print statement below is just to avoid text overlapping by replace the text before with spaces and letting text after to override the spaces, and the cause for this is most likely the "\r" function because it makes the textcursor to write at the first place of the line, not by straight up deleting. (I didn't find any other solutions for this)
                     print("                                ", end = "\r")
                     time.sleep(0.5)
                     break
              


def game():
    global barcontrol
    global BATTLESHIP
    startinput = input("Type \"play\", \"help\", or \"about\" to continue: ")
    if startinput == "play":
        os.system('cls')
        print(BATTLESHIP)
        barcontrol = 0
        loadingscreen("Loading game: ")
        #main part of the game
        playgame()
        #main part of the game
    elif startinput == "help":
        os.system("cls")
        print(BATTLESHIP)
        print("You don't get any help because I haven't implemented the help option lmao\n")
        game()
    elif startinput == "about":
        os.system('cls')
        print(BATTLESHIP)
        print("This game is created by David H Peterson, he had taken inspiration from the original game, aka \"Battleship\"\nBecause he had nothing to do in spring break, and he got the idea to make a console-based game from his teacher\nDavid recreated Battleship in the terminal using Python.\n")
        game()
    else:
        game()



def playgame():
    global alpha
    global num
    global usedcoordsplayer
    global playerattackedtargetcount
    global aiattackedtargetcount
    guess = input("You turn: ")
    guesscharnum = []
    for letter in guess:
        guesscharnum.append(letter)
    if len(guesscharnum) == 2:
        firstletter = guesscharnum[0]
        lastletter = guesscharnum[1]
        if firstletter in alpha:
            if lastletter in num:
                if guess in usedcoordsplayer:
                    print("You missed your shot here, remember?\n")
                    playgame()
                else:
                    usedcoordsplayer.append(guess)
                    if guess in withshipai:
                        playerattackedtargetcount += 1
                        withshipai.remove(guess)
                        print("Right on target!\n")
                        if not withshipai:
                            print("You won! All the opposing ships have been destroyed!")
                            print("The AI has successfully eliminated " + str(aiattackedtargetcount) + " of your ships. (unfortunately)")
                        else:
                            generatecoordinateai()
                    else:
                        print("You missed!\n")
                        generatecoordinateai()
            else:
                print("Please enter a correct coordinate\n")
                playgame()
        else:
            print("Please enter a correct coordinate\n")
            playgame()
    else:
        print("Please enter a two-letter coordinate\n")
        playgame()



def generatecoordinateai():
    global alpha
    global num
    global usedcoordsai
    global aiattackedtargetcount
    global playerattackedtargetcount
    firstletterforai = random.sample(alpha, 1)
    lastnumforai = random.sample(num, 1)
    aiguess = firstletterforai+lastnumforai
    while True:
        if aiguess in usedcoordsai:
            firstletterforai = random.sample(alpha, 1)
            lastnumforai = random.sample(num, 1)
        else:
            break
    aiguessfinalform = "".join(aiguess)
    usedcoordsai.append(aiguessfinalform)
    print("AI's turn: ", end="\r")
    time.sleep(0.2)
    print("AI's turn: " + aiguessfinalform)
    if aiguessfinalform in withshipplayer:
        aiattackedtargetcount += 1
        withshipplayer.remove(aiguessfinalform)
        print("Right on target!\n")
        while True:
            if not withshipplayer:
                print("The AI won, you are such a loser!")
                print("You have successfully eliminated " + str(playerattackedtargetcount) + " of the AI's ships. (You'll get 'em nex' time)")
            else:
                break
        time.sleep(0.5)
        playgame()
    else:
        print("AI missed!\n")
        time.sleep(0.5)
        playgame()



def startup():
    os.system('cls')
    print(BATTLESHIP)
    loadingscreen("Loading assets: ")