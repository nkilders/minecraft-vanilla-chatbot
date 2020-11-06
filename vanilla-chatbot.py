from mcrcon import MCRcon  # pip install mcrcon
import time


######### SETTINGS #########

serverAddress = "127.0.0.1"
rconPort = 25575
rconPassword = "5€cr3t"

logFilePath = "path/to/latest.log"

###### EVENT HANDLERS ######


def handleJoin(player: str):
    print(player + " joined")

    rconSend("/say Welcome, " + player)


def handleLeave(player: str):
    print(player + " left")

    rconSend("/say Bye, " + player)


def handleChat(player: str, words: list):
    print(player + ": " + ' '.join(words))

    rconSend("/say " + player + " said \"" + ' '.join(words) + "\"")

############################


lastNumLines = -1

rcon = MCRcon(serverAddress, rconPassword, rconPort)
rconConnected = False


def handleLine(line: str):
    global rconConnected

    args = line.split()
    argsLen = len(args)

    if argsLen >= 5 and args[1] == "[Server" and args[2] == "thread/INFO]:":
        if args[3].startswith("<"):
            handleChat(args[3][1:len(args[3])-1], args[4:])
        elif argsLen == 7:
            if args[4] == "joined" and args[5] == "the" and args[6] == "game":
                handleJoin(args[3])
            elif args[4] == "left" and args[5] == "the" and args[6] == "game":
                handleLeave(args[3])
            elif args[3] == "Thread" and args[4] == "RCON" and args[5] == "Listener" and args[6] == "stopped":
                if rconConnected:
                    rcon.disconnect()
                    rconConnected = False


def rconSend(command: str):
    global rconConnected

    if not rconConnected:
        try:
            rcon.connect()
        except ConnectionRefusedError:
            print("Error: Connection refused")
            return

        rconConnected = True

    print(">> " + command)
    print("<< " + rcon.command(command))


print("######### SETTINGS #########")
print("")
print("Server address:\t" + serverAddress)
print("RCON port:\t" + str(rconPort))
print("")
print("Log file path:\t" + logFilePath)
print("")
print("############################")
print("")

try:
    with open(logFilePath, "r") as f:
        lastNumLines = len(f.readlines())
except FileNotFoundError:
    print("ERROR: Logfile not found")
    exit()

while True:
    with open(logFilePath, "r") as f:
        lines = f.readlines()
        numLines = len(lines)

        if numLines > lastNumLines:
            for l in range(lastNumLines, numLines):
                line = lines[l]

                if line != "\n":
                    handleLine(line)

        lastNumLines = numLines

    time.sleep(0.5)
