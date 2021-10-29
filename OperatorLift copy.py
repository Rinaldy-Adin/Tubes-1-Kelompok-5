mesinNyala = True
no_kartuLift = str()
pin_kartu = str()
username_admin = str()
password_admin = 0
userIndex = -1
admin = [["admin_kantor", 123456], ["admin_apartemen", 234567]]

users = open('test.data', 'r+').readlines()
for i in range(len(users)):
  users[i] = users[i][:-1].split(",")
for i in range(len(users)):
  for j in range(len(users[i])):
    print(type(users[i][j]))
    users[i][j] = str(users[i][j])
    print(type(users[i][j]))
    print("")

def loadState():
  global users
  f = open('test.data', 'r+')
  users = f.readlines()
  for i in range(len(users)):
    users[i] = users[i][:-1].split(",")
  for i in range(len(users)):
    for j in range(len(users[i])):
      users[i][j] = str(users[i][j])

def saveState():
  global users
  f = open('kartuLift.data', 'w+')
  data = ""
  for i in range(len(users)):
    for j in range(len(users[i])):
      data += str(users[i][j])
      if j != len(users[i]) - 1:
        data += ","
    data += "\n"
  f.write(data)


def getUser(nomor):
  for i in range(len(users)):
    if nomor == str(users[i][0]):
      return i
  return - 1

def isValidPIN(nomor, pin):
  return pin == str(users[nomor][1])

def getAdmin(username):
  for i in range(len(admin)):
    if username == str(admin[i][0]):
      return i
  return - 1

def isValidPassword(username, password):
  return password == int(admin[username][1])

def printDivider():
  print("=======================================================")

def reset():
  global no_kartuLift, pin_kartu
  no_kartuLift = str()
  pin_kartu = str()
  userIndex = -1

def resetAdmin():
  global username_admin, password_admin
  username_admin = str()
  password_admin = 0
  userIndex = -1

def main():
  global users, mesinNyala, username_admin, password_admin, userIndex
  while (mesinNyala):
    printDivider()
    print("Operator Lift Gedung Mall dan Apartemen Tuan Dic")
    while (username_admin == str()):
      printDivider()
      temp = str(input("Username: "))
      userIndex = getAdmin(temp)
      if userIndex >= 0:
        username_admin = temp
      else:
        print("Username tidak tersedia. Harap coba lagi.")
        printDivider()
    while (username_admin != str() and password_admin == 0):
      temp = int(input("Password: "))
      if isValidPassword(userIndex, temp):
        password_admin = temp
        printDivider()
        print("Log in berhasil")
      else:
        resetAdmin()
        print("Password Anda salah.")
        printDivider()
    while (username_admin != str() and password_admin != 0):
      operasi()


def operasi():
  printDivider()
  print("1. Ubah PIN kartu penghuni apartemen atau  pengguna kantor \n2. Tambah kartu baru\n3. Log Out")
  printDivider()
  commands = int(input())
  if commands==1:
    cekKartu()
  elif commands==2:
    cekAdmin()
  elif commands ==3:
    resetAdmin()
    main()

def cekKartu():
  global users, mesinNyala, no_kartuLift, pin_kartu, userIndex
  while (mesinNyala):
    while (no_kartuLift == str()):
      printDivider()
      temp = str(input("User mengetap kartu apartemen\nNomor Kartu : "))
      userIndex = getUser(temp)
      if userIndex >= 0:
        no_kartuLift = temp
      else:
        print("Kartu apartemen tidak tersedia. Harap coba lagi.")
    while (no_kartuLift != str() and pin_kartu == str()):
      temp = str(input("PIN Kartu  Lift : "))
      if isValidPIN(userIndex, temp):
        pin_kartu = temp
      else:
        reset()
        print("PIN Anda salah.")
        printDivider()
    while (no_kartuLift != str() and pin_kartu != str()):
      gantiPassword()


def gantiPassword():
    temp = str(input("Masukkan PIN Anda sekali lagi: "))
    printDivider()
    if isValidPIN(userIndex, temp):
        loadState()
        temp = input("Masukkan PIN baru Anda: ")
        if len(temp) == 6:
            temp1 = temp
            temp2 = input("Masukkan PIN baru Anda sekali lagi: ")
            if temp1 == temp2:
                users[userIndex][1] = temp
                saveState()
                print("PIN kartu lift Anda berhasil diubah.")
                main()
            else:
              print("PIN Kartu tidak sesuai")
              gantiPassword()
        else:
            print("PIN kartu lift tidak sesuai dengan ketentuan.")
    else:
        print("PIN tidak sesuai")

def cekAdmin():
    global users, mesinNyala, username_admin, password_admin, userIndex, step
    resetAdmin()
    while (username_admin == str()):
      temp = str(input("Harap memverifikasi admin\nUsername: "))
      userIndex = getAdmin(temp)
      if userIndex >= 0:
        username_admin = temp
      else:
        print("Username tidak tersedia. Harap coba lagi.")
        printDivider()
    while (username_admin != str() and password_admin == 0):
      temp = int(input("Password: "))
      if isValidPassword(userIndex, temp):
        password_admin = temp
        printDivider()
        print("Verifikasi berhasil")
      else:
        resetAdmin()
        print("Password Anda salah.")
        printDivider()
    while (username_admin != str() and password_admin != 0):
      tambahKartu()

def tambahKartu():
  kartuLift_baru =[]
  kartu_baru0 = int(input("Masukkan 5 digit nomor kartu baru: "))
  kartu_baru1 = str(kartu_baru0)
  if len(kartu_baru1)==5:
    kartuLift_baru.append(kartu_baru1)
    pin_baru0 = int(input("Masukkan 6 digit PIN kartu baru: "))
    pin_baru1 = str(pin_baru0)
    if len(pin_baru1)==6:
      kartuLift_baru.append(pin_baru1)
      print(kartuLift_baru)
      loadState()
      users.append(kartuLift_baru)
      saveState()
      print("Kartu berhasil disimpan")
    else:
      print("PIN tidak memenuhi syarat. Harap ulangi lagi")
      tambahKartu()
  else:
    print("Nomor kartu tidak memenuhi syarat. Harap ulangi lagi")
    tambahKartu()
  main()
      
main()
