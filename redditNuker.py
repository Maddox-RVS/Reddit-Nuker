import os
import praw
from colorama import Fore

nukeAllComments = False
nukeAllPosts = False

#Gets credentials
clientID = ""
clientSecret = ""
passcode = ""
handle = ""

file = open(os.getcwd() + "\\credentials.txt")
count = 0
for line in file:
    if count == 0: handle = line[9:].strip()
    elif count == 1: passcode = line[11:].strip()
    elif count == 2: clientID = line[11:].strip()
    elif count == 3: clientSecret = line[15:].strip()
    count += 1
    if count == 4:
        break
file.close()

#Loggin and validate reddit user
reddit = praw.Reddit(client_id=clientID, client_secret=clientSecret, password=passcode, user_agent='deletes my comments', username=handle)
reddit.validate_on_submit = True
redditor = reddit.user.me()

numberOfComments = 0
for comment in redditor.comments.new():
    numberOfComments+=1

numberOfPosts = 0
for submission in redditor.submissions.new():
    numberOfPosts+=1;

def printProgressBar(total, current, commentsOrPosts, color):
    progressPercent = (current/total)*100

    if progressPercent >= 100: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|███████████████|>{Fore.RESET}")
    elif progressPercent >= (100/15)*14: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|██████████████=|>{Fore.RESET}")
    elif progressPercent >= (100/15)*13: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|█████████████==|>{Fore.RESET}")
    elif progressPercent >= (100/15)*12: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|████████████===|>{Fore.RESET}")
    elif progressPercent >= (100/15)*11: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|███████████====|>{Fore.RESET}")
    elif progressPercent >= (100/15)*10: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|██████████=====|>{Fore.RESET}")
    elif progressPercent >= (100/15)* 9: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|█████████======|>{Fore.RESET}")
    elif progressPercent >= (100/15)* 8: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|████████=======|>{Fore.RESET}")
    elif progressPercent >= (100/15)* 7: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|███████========|>{Fore.RESET}")
    elif progressPercent >= (100/15)* 6: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|██████=========|>{Fore.RESET}")
    elif progressPercent >= (100/15)* 5: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|█████==========|>{Fore.RESET}")
    elif progressPercent >= (100/15)* 4: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|████===========|>{Fore.RESET}")
    elif progressPercent >= (100/15)* 3: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|███============|>{Fore.RESET}")
    elif progressPercent >= (100/15)* 2: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|██=============|>{Fore.RESET}")
    elif progressPercent >= (100/15)* 1: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|█==============|>{Fore.RESET}")
    elif progressPercent >= (100/15)* 0: print(f"{color}{current} out of {total} {commentsOrPosts} have been deleted! <|===============|>{Fore.RESET}")

def nukeComments():
    progress = 0
    for comment in redditor.comments.new():
        comment.edit(".")
        comment.delete()
        os.system('cls')
        print()
        progress+=1
        printProgressBar(numberOfComments, progress, "comments", Fore.BLUE)

def nukePosts():
    progress = 0
    for submission in redditor.submissions.new():
        submission.delete()
        os.system('cls')
        if nukeAllComments:
            print()
            printProgressBar(numberOfComments, numberOfComments, "comments", Fore.BLUE)
        print()
        progress+=1
        printProgressBar(numberOfPosts, progress, "posts", Fore.BLUE)

#Sets comment nuking options
userInput = input(f"{Fore.YELLOW}\nWould you like to nuke your newest 100 comments? (Y/N): {Fore.RESET}")
userInput = userInput.lower()
if userInput == "y" : nukeAllComments = True
print("Nuke newest 100 comments: ", end="")
if nukeAllComments : print(f"{Fore.RED}YES{Fore.RESET}")
else : print(f"{Fore.RED}NO{Fore.RESET}")

#Sets post nuking options
userInput = input(f"{Fore.YELLOW}\nWould you like to nuke your newest 100 posts? (Y/N): {Fore.RESET}")
userInput = userInput.lower()
if userInput == "y" : nukeAllPosts = True
print("Nuke newest 100 posts: ", end="")
if nukeAllPosts : print(f"{Fore.RED}YES{Fore.RESET}")
else : print(f"{Fore.RED}NO{Fore.RESET}")

#Confirmation of nuke
if nukeAllComments and nukeAllPosts:
    userInput = input(f"{Fore.YELLOW}\n[CONFIRMATION]\nAre you sure you want to nuke your {Fore.RED}NEWEST 100 comments{Fore.YELLOW} and your {Fore.RED}NEWEST 100 posts{Fore.YELLOW}? Once these are nuked there will be no way to recover them! (Y/N): {Fore.RESET}")
elif nukeAllComments:
    userInput = input(f"{Fore.YELLOW}\n[CONFIRMATION]\nAre you sure you want to nuke your {Fore.RED}NEWEST 100 comments{Fore.YELLOW}? Once these are nuked there will be no way to recover them! (Y/N): {Fore.RESET}")
elif nukeAllPosts:
    userInput = input(f"{Fore.YELLOW}\n[CONFIRMATION]\nAre you sure you want to nuke your {Fore.RED}NEWEST 100 posts{Fore.YELLOW}? Once these are nuked there will be no way to recover them! (Y/N): {Fore.RESET}")

#Begin nuking process
userInput = userInput.lower()
if userInput == "y":
    if nukeAllComments : nukeComments()
    if nukeAllPosts : nukePosts()
    print(f"\n{Fore.YELLOW}NUKE FINISHED!{Fore.RESET}")
    quit(0)
else:
    print(f"\n{Fore.BLUE}NUKE CANCELED!{Fore.RESET}")
    quit(0)