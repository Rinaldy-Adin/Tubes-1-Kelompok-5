from threading import Timer
import os

class systemState:
    def __init__(self):
        self.insideElev = False
        self.systemOn = True
        self.currentArea = 1 # 1: Mall; 2: Apartment; 3: kantor

    def getInElev(self):
        self.insideElev = True

    def getOutElev(self):
        self.insideElev = False

    def changeArea(self, destination):
        self.currentArea = destination

    def turnOff(self):
        self.systemOn = False

class elevator:
    def __init__(self, minFloor, maxFloor, startingFloor):
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.currentFloor = startingFloor


    def goTo(self, globalState, destination):
        globalState.getInElev()
        elevTImer = Timer(abs(destination-self.currentFloor) * 0.2, globalState.getOutElev)
        elevTImer.start()
        self.currentFloor = destination

class accessCards:
    def __init__(self):
        self.data = open('test.txt', 'r+').readlines()
        for i in range(len(self.data)):
            self.data[i] = self.data[i][:-1].split(",")
        

def printDivider():
    print("=======================================================")

def inputPrompt():
    return input("Masukkan input: ")

def checkCard(cardData, destination):
    data = cardData.data
    id = str()
    pw = str()

    while (True):
        printDivider()
        id = input("Enter your access card ID: ")
        
        for i in range(len(data)):
            if (id == data[i][0]):
                if (data[i][1] == "0"):
                    return True
                else:
                    pw = input("Enter your access card password: ")
                    if (pw == data[i][1]):
                        return True
        
        tryAgain = input("Your credentials are incorrect, do you want to try again (Y/N) :")
        if (not tryAgain):
            return False


def runMallLift(globalState, elevator):
    validInput = False
    floorNum = elevator.currentFloor
    mallMin = elevator.minFloor
    mallMax = elevator.maxFloor

    while (not validInput):
        printDivider()
        print("Anda sedang di Mall lantai {}".format(floorNum))
        if (floorNum == mallMax):
            print("1: call elevator\n0: exit\n2: Pindah ke Apartemen")
        else:
            print("1: call elevator\n0: exit")
        
        action = int(inputPrompt())
        if (floorNum == mallMax and (action >= 0 and action <= 2)):
            validInput = True
        elif (action >= 0 and action <= 1):
            validInput = True

    if (action == 1):
        printDivider()
        destination = int(input("Masukkan lantai tujuan: "))

        while (destination == floorNum or destination < mallMin or destination > mallMax):
            printDivider()
            print("Lantai tujuan tidak sesuai")
            destination = int(input("Masukkan lantai tujuan: "))

        printDivider()
        print("\nanda sedang di dalam lift\n")

        elevator.goTo(globalState, destination)

    elif (action == 2):
        globalState.changeArea(2)
    else:
        globalState.turnOff()

def runApartLift(globalState, cardData, elevator):
    validInput = False
    floorNum = elevator.currentFloor
    apartMin = elevator.minFloor
    apartMax = elevator.maxFloor

    while (not validInput):
        printDivider()
        print("Anda sedang di Apartemen lantai {}".format(floorNum))
        if (floorNum == apartMin):
            print("1: call elevator\n0: exit\n2: Pindah ke Mall")
        else:
            print("1: call elevator\n0: exit")

        action = int(inputPrompt())
        if (floorNum == apartMin and (action >= 0 and action <= 2)):
            validInput = True
        elif (action >= 0 and action <= 1):
            validInput = True

    if (action == 1):
        printDivider()
        destination = int(input("Masukkan lantai tujuan: "))

        while (destination == floorNum or destination > apartMax or destination < apartMin):
            printDivider()
            print("Lantai tujuan tidak sesuai")
            destination = int(input("Masukkan lantai tujuan: "))

        if (destination != 0):
            cardAccepted = checkCard(cardData, destination)
        
            if (cardAccepted):
                printDivider()
                print("\nanda sedang di dalam lift\n")
                elevator.goTo(globalState, destination)            

    elif (action == 2):
        globalState.changeArea(1)
    else:
        globalState.turnOff()

def main():
    mallMin = -1
    mallMax = 4

    apartMin = 0
    apartMax = 20

    floorNum = mallMin - 1

    while (floorNum < mallMin or floorNum > 0):
        printDivider()
        print("Mulai di lantai apa?\n0: basement\n1: GF")
        printDivider()
        floorNum = int(inputPrompt())
        floorNum -= 1
        # masuk harus dari basement atau GF

    globalState = systemState()
    mallElevator = elevator(mallMin, mallMax, floorNum)
    apartElevator = elevator(apartMin, apartMax, 0)
    cardData = accessCards()

    while (globalState.systemOn):
        if (globalState.insideElev):
            continue

        if (globalState.currentArea == 1):
            runMallLift(globalState, mallElevator)

        elif (globalState.currentArea == 2):
            runApartLift(globalState, cardData, apartElevator)

main()