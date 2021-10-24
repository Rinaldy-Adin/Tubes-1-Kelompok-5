from threading import Timer

insideElev = False

def getOutElev():
    global insideElev
    insideElev = False

def main():
    global insideElev

    mallMin = -1
    mallMax = 4

    apartMin = 0
    apartMax = 10

    floorNum = mallMin - 1
    area = 1 # 1: Mall; 2: Apartment; 3: kantor
    systemOn = True

    while (floorNum < mallMin or floorNum > 0):
        print("mulai di lantai apa?")
        floorNum = int(input("-1: Basement; 0: GF"))
        # masuk harus dari basement atau GF

    while (systemOn):
        if (insideElev):
            continue

        if (area == 1):
            print("Anda sedang di Mall lantai {}".format(floorNum))
            validInput = False

            while (not validInput):
                if (floorNum == mallMax):
                    print("1: call elevator, 0: exit, 2: Pindah ke Apartemen")
                else:
                    print("1: call elevator, 0: exit")

                action = int(input("Enter action: "))
                if (floorNum == mallMax and (action >= 0 and action <= 2)):
                    validInput = True
                elif (action >= 0 and action <= 1):
                    validInput = True

            if (action == 1):
                destination = int(input("Mau ke lantai brp: "))

                while (destination == floorNum or destination < mallMin or destination > mallMax):
                    destination = int(input("Masukkan nomor lantai yang sesuai: "))

                print("\nanda sedang di dalam lift\n")

                insideElev = True
                getInElev = Timer(abs(destination-floorNum) * 0.2, getOutElev)
                getInElev.start()
                floorNum = destination

            elif (action == 2):
                area = 2
                floorNum = 0
            else:
                systemOn = False

        elif (area == 2):
            print("Anda sedang di Apartemen lantai {}".format(floorNum))
            validInput = False

            while (not validInput):
                if (floorNum == apartMin):
                    print("1: call elevator, 0: exit, 2: Pindah ke Mall")
                else:
                    print("1: call elevator, 0: exit")

                action = int(input("Enter action: "))
                if (floorNum == apartMin and (action >= 0 and action <= 2)):
                    validInput = True
                elif (action >= 0 and action <= 1):
                    validInput = True

            if (action == 1):
                destination = int(input("Mau ke lantai brp: "))

                while (destination == floorNum or destination > apartMax or destination < apartMin):
                    destination = int(input("Masukkan nomor lantai yang sesuai: "))

                print("\nanda sedang di dalam lift\n")


                insideElev = True
                getInElev = Timer(abs(floorNum-destination) * 0.2, getOutElev)
                getInElev.start()
                floorNum = destination
            elif (action == 2):
                area = 1
                floorNum = mallMax
            else:
                systemOn = False

main()