from ircbotframe import ircBot
import sys

# Bot specific function definitions
    
def authFailure(recipient, name):
    bot.say(recipient, "You could not be identified")

def quitSuccess(quitMessage):
    bot.disconnect(quitMessage)
    bot.stop()
    
def joinSuccess(channel):
    bot.joinchan(channel)

def saySuccess(channel, message):
    bot.say(channel, message)

def kickSuccess(nick, channel, reason):
    bot.kick(nick, channel, reason)

def identPass():
    pass
    
def identFail():
    pass

def privmsg(sender, headers, message):
    if message.startswith("!say "):
        firstSpace = message[5:].find(" ") + 5
        if sender == owner:
            bot.identify(sender, saySuccess, (message[5:firstSpace], message[firstSpace+1:]), authFailure, (headers[0], sender))
    elif message.startswith("!quit"):
        if sender == owner:
            if len(message) > 6:
                bot.identify(sender, quitSuccess, (message[6:],), authFailure, (headers[0], sender))
            else:
                bot.identify(sender, quitSuccess, ("",), authFailure, (headers[0], sender))
    elif message.startswith("!join "):
        if sender == owner:
            bot.identify(sender, joinSuccess, (message[6:],), authFailure, (headers[0], sender))
    elif message.startswith("!kick "):
        firstSpace = message[6:].find(" ") + 6
        secondSpace = message[firstSpace+1:].find(" ") + (firstSpace + 1)
        if sender == owner:
            bot.identify(sender, kickSuccess, (message[6:firstSpace], message[firstSpace+1:secondSpace], message[secondSpace+1:]), authFailure, (headers[0], sender))
    else:
        print "PRIVMSG: \"" + message + "\""
            
def actionmsg(sender, headers, message):
    print "An ACTION message was sent by " + sender + " with the headers " + str(headers) + ". It says: \"" + sender + " " + message + "\""

def endMOTD(sender, headers, message):
    bot.joinchan(chanName)
    bot.say(chanName, "I am an example bot.")
    bot.say(chanName, "I have 4 functions, they are Join, Kick, Quit and Say.")
    bot.say(chanName, "Join (joins a channel); Usage: \"!join #<channel>\"")
    bot.say(chanName, "Kick (kicks a user); Usage: \"!kick <nick> #<channel> <reason>\"")
    bot.say(chanName, "Quit (disconnects from the IRC server); Usage: \"!quit [<quit message>]\"")
    bot.say(chanName, "Say (makes the bot say something); Usage: \"!say <channel/user> <message>\"")
    bot.say(chanName, "The underlying framework is in no way limited to the above functions.")
    bot.say(chanName, "This is merely an example of the framework's usage")

def useSSL(argv):
    return len (argv) == 6 and argv[5] == "ssl"

# Main program begins here
if __name__ == "__main__":
    if len(sys.argv) == 5 or useSSL(sys.argv):
        server = sys.argv[1]
        port = int(sys.argv[2])
        owner = sys.argv[3]
        chanName = "#" + sys.argv[4]
        bot = ircBot(server, port, "ExampleBot", "An example bot written with the new IRC bot framework", ssl=useSSL(sys.argv))
        bot.bind("PRIVMSG", privmsg)
        bot.bind("ACTION", actionmsg)
        bot.bind("376", endMOTD)
        bot.debugging(True)
        bot.start()
        inputStr = "" 
        while inputStr != "stop":
            inputStr = raw_input()
        bot.stop()
        bot.join()
    else:
        print "Usage: python examplebot.py <server> <port> <your IRC nick> <irc channel (no '#' character please)> <ssl (optional)>"


