data = [["",""] for i in range(1000)]

for i in range(len(data)):
    x = ""
    if (i // 50 < 10):
        x += str(0)
    x += str(i // 50 + 1)
    x += "0"
    if ((i+1) % 50 < 10):
        x += "0"
    x += str(i % 50 + 1)

    data[i][0] = x

    y = ""
    if (i < 10000):
        y = "000000"
    else:
        y = "123456"
    
    data[i][1] = y

f = open("kartuBaru.data", "w")
s = ""

for i in range(len(data)):
    s += data[i][0]
    s += ","
    s += data[i][1]
    s += "\n"
f.write(s)