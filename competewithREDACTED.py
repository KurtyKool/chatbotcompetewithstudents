import numpy as np
import pandas as pd
import csv

#############################################################
##                  CompeteWithREDACTED.py                 ##
#############################################################
##                                                         ##
## Get wrecked, you scrub. This is what good python looks  ##
## like. This takes in an input to allow users to write    ##
## their own chat bots. The chatbots are programmed using  ##
## a csv file of potential responses. Each line must be    ##
## labelled according to the following format:             ##
##                                                         ##
## LineName, Statment, Options...                          ##
##                                                         ##
## The 'LineName' cell is a string containing a symbolic   ##
## reference to the line of chat you're intereacting with. ##
## These are often easier for humans to parse than line-   ##
## numbers. Avoids the much hated behaviour of GoTo.       ##
##                                                         ##
## The 'Statement' cell contains a string of text for the  ##
## chatbot to respond with at that juncture.               ##
##                                                         ##
## The 'Options' cells must contain three strings sepa-    ##
## rated by semi-colons (;). The first string contains the ##
## long-form text of that option. The second string con-   ##
## tains the short-hand abbreviation for the option. Last- ##
## ly, the third string contains the LineName that the bot ##
## should jump to if a user selects this option. The csv   ##
## can have multiple options for a single csv statement.   ##
## An example has been provided below:                     ##
##                                                         ##
## START, What's your favourite animal?, Cats;C;LikeCats,\ ##
## Dogs;D;LikeDogs, Birds;B;LikeBirds                      ##
##                                                         ##
## The csv file would thus contain lines titled LikeCats   ##
## LikeDogs and LikeBirds, respectively.                   ##
##                                                         ##
#############################################################

#######################
### INITIAL MESSAGE ###
#######################
# We need to load the csv first, since the functions depend on it. 
print("Hello, which chatbot would you like to interact with today?")
print("- TestBot")
print("- Default")
print("- SnoopDog")
chatbotname = input()
chatbotcsv = list(csv.reader(open('./' + chatbotname + '.csv')))

chatbotNameList = {} #Keeps a record of the line number of each "Name"
# This allows chatbot responses to be given by name, rather than by line number.

############################
### DEFINE ALL FUNCTIONS ###
############################

def readAllChatNames():
    # Updates the chatbotNameList with all names in the csv.
    # The Name values are keys in a dictionary, their values are their line \
    # number.
    for i in range(0,len(chatbotcsv)):
        chatbotNameList[chatbotcsv[i][0]] = i
    return chatbotcsv[0][0]

def readMessage(inline):
    # Reads the chatbotmessage
    message = str(chatbotcsv[inline][1])
    return(message)

def readOptions(inline):
    # Extracts the options for a given line of text
    finOpt = len(chatbotcsv[inline])
    curropts = {}
    for i in range(2,finOpt):
        [optTxt,optChr,optJmp] = str(chatbotcsv[inline][i]).split(";")
        curropts[optTxt] = [optChr,optJmp]
    return curropts
        
def getResponse(chatMessage,currOpts):
    # Takes in a message and list of options from readMessage and readOptions\
    # and fetches the user response
    print(chatMessage)
    if currOpts == {}:
        return(-1)
    for key in  currOpts.keys():
        print('- (' + currOpts[key][0] + ') ' +  str(key))
    response = str(input()).lower()
    for key in currOpts.keys():
        if response == str(key).lower():
            return(currOpts[key][1])
        if response == currOpts[key][0].lower():
            return(currOpts[key][1])
    print("That is not an option, please try again.")
    return(getResponse(chatMessage,currOpts))

def runChatBot(lineName):
    # Runs the chatbot for a single parse.
    currentLine = chatbotNameList[lineName]
    currentMessage = readMessage(currentLine)
    currentOptions = readOptions(currentLine)
    nextName = getResponse(currentMessage,currentOptions)
    if nextName == -1:
        return(0)
    else:
        runChatBot(nextName)
    return(0)

#######################
### RUN THE CHATBOT ###
#######################

print("The chat session has started")
firstline = readAllChatNames()
runChatBot(firstline)
print("Chat session ended")
