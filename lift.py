from abc import abstractproperty
from threading import Timer
import csv

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

class mallShops:
    def __init__(self):
        with open('DataMall.csv', encoding="utf-8-sig", newline='') as f:
            reader = csv.reader(f)
            self.data = list(reader)
    
    def getStoreTypes(self):
        storeTypes = []

        for store in self.data:
            storeType = store[1]
            if (not(storeType in storeTypes)):
                storeTypes.append(storeType)
        
        return storeTypes

    def getStoresByType(self, storeType):
        stores = []

        for store in self.data:
            if (store[1] == storeType):
                stores.append(store)
        
        return stores
    
    def getStoresByFloor(self, floor):
        stores = []

        for store in self.data:
            if (int(store[2]) == floor):
                stores.append(store)
        
        return stores
    
    def getStoresByName(self, name):
        stores = []

        for store in self.data:
            if (store[0].lower().find(name.lower()) != -1):
                stores.append(store)

        return stores

class accessCards:
    def __init__(self):
        with open('kartuLift.csv', encoding="utf-8-sig", newline='') as f:
            reader = csv.reader(f)
            self.data = list(reader) 

def printDivider():
    print("=======================================================")

def inputPrompt():
    return input("Masukkan input: ")

def mallInfo(shopData, elevator):
    category = 0
    while (category < 1 or category > 3):
        printDivider()
        print("Pilih kategori pencarian: ")
        print("1. Pencarian nama toko")
        print("2. Jenis toko")
        print("3. Lantai")
        category = int(inputPrompt())
    
    if (category == 1):
        printDivider()
        storeName = input("Masukkan nama toko yang ingin dicari: ")

        stores = shopData.getStoresByName(storeName)

        printDivider()
        for i in range(len(stores)):
            print("{}. {}".format(i+1, stores[i][0]))

        storeIdx = 0
        while (storeIdx < 1 or storeIdx > len(stores)):
            printDivider()
            storeIdx = int(input("Masukkan nomor toko yang ingin dicari: "))
        storeIdx -= 1

        printDivider()
        print("{} terdapat pada lantai {}".format(stores[storeIdx][0], stores[storeIdx][2]))
    elif (category == 2):
        storeTypes = shopData.getStoreTypes()

        printDivider()
        for i in range(len(storeTypes)):
            print("{}. {}".format(i+1, storeTypes[i]))
        
        storeTypeIdx = 0
        while (storeTypeIdx < 1 or storeTypeIdx > len(storeTypes)):
            printDivider()
            storeTypeIdx = int(input("Masukkan nomor kategori toko yang ingin dicari: "))
        
        storeType = storeTypes[storeTypeIdx-1]
        stores = shopData.getStoresByType(storeType)

        printDivider()
        for i in range(len(stores)):
            print("{}. {}".format(i+1, stores[i][0]))

        storeIdx = 0
        while (storeIdx < 1 or storeIdx > len(stores)):
            printDivider()
            storeIdx = int(input("Masukkan nomor toko yang ingin dicari: "))
        storeIdx -= 1

        printDivider()
        print("{} terdapat pada lantai {}".format(stores[storeIdx][0], stores[storeIdx][2]))
    else:
        printDivider()
        for i in range(elevator.maxFloor - elevator.minFloor + 1):
            print("{}. Lantai {}".format(i + 1, elevator.minFloor + i))
        
        floorIdx = 0
        while (floorIdx < 1 or floorIdx > elevator.maxFloor - elevator.minFloor + 1):
            printDivider()
            floorIdx = int(input("Masukkan nomor indeks lantai toko yang ingin dicari: "))
        floorIdx += elevator.minFloor - 1

        printDivider()
        stores = shopData.getStoresByFloor(floorIdx)
        for i in range(len(stores)):
            print("{}. {}".format(i+1, stores[i][0]))

def checkCard(cardData, destination):
    data = cardData.data
    id = str()
    pw = str()

    while (True):
        printDivider()
        id = input("Enter your access card ID: ")
        
        for i in range(len(data)):
            if (destination != int(data[i][0][:2])):
                continue

            if (id == data[i][0]):
                if (data[i][1] == "0"):
                    return True
                else:
                    pw = input("Enter your access card password: ")
                    if (pw == data[i][1]):
                        return True
        
        tryAgain = input("Your credentials are incorrect, do you want to try again (Y/N) :")
        if (tryAgain == "N" or tryAgain == "n"):
            return False


def runMallLift(globalState, shopData, elevator):
    validInput = False
    floorNum = elevator.currentFloor
    mallMin = elevator.minFloor
    mallMax = elevator.maxFloor

    while (not validInput):
        printDivider()
        print("Anda sedang di Mall lantai {}".format(floorNum))
        if (floorNum == mallMax):
            print("1: call elevator\n2: Info Toko\n0: exit\n3: Pindah ke Apartemen")
        else:
            print("1: call elevator\n2: Info Toko\n0: exit")
        
        action = int(inputPrompt())
        if (floorNum == mallMax and (action >= 0 and action <= 3)):
            validInput = True
        elif (action >= 0 and action <= 2):
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
        mallInfo(shopData, elevator)
    elif (action == 3):
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
            print("1: call elevator\n0: exit\n3: Pindah ke Mall")
        else:
            print("1: call elevator\n0: exit")

        action = int(inputPrompt())
        if (floorNum == apartMin and (action == 0 or action == 1 or action == 3)):
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
        else:
            printDivider()
            print("\nanda sedang di dalam lift\n")
            elevator.goTo(globalState, destination)

    elif (action == 3):
        globalState.changeArea(1)
    else:
        globalState.turnOff()

def main():
    mallMin = -1
    mallMax = 4

    apartMin = 0
    apartMax = 10

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
    shopData = mallShops()

    while (globalState.systemOn):
        if (globalState.insideElev):
            continue

        if (globalState.currentArea == 1):
            runMallLift(globalState, shopData, mallElevator)

        elif (globalState.currentArea == 2):
            runApartLift(globalState, cardData, apartElevator)

main()