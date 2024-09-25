import serial as serial


def checkBPM():
    data = "x"
    while not data.isdigit() or data == "0":
        ser = serial.Serial("COM5", 115200)

        data = str(ser.readline())
        data = data.replace("'", "")
        data = data.replace(chr(92), "")
        data = data.replace("rn", "")
        data = data.replace(" ", "")
        data = data.replace("b", "")
        ser.close()

    return data
