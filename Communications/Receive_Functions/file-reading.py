from digi.xbee.devices import XBeeDevice
import time
import os
import base64


class MessageBuffer:
    msg_type = ""
    file_size = 0 #max file size
    offset = 0 #number of bytes sent?
    buffer = "" #data to be sent
    len = 0 #len of msg sent this is for the last message so you dont read to much
    cont = True

    def printObj(self):
        print("Msg_type: " + self.msg_type + " File Size: " + str(self.file_size) + " Offset: " + str(
            self.offset) + " Buffer: " + self.buffer)

    def firstmsg(self):
        return self.msg_type + ":" + str(self.file_size) + ":" + str(self.offset) + ":" + self.buffer

    def prepmsg(self):
        return self.msg_type + ":" + str(self.offset) + ":" + str(self.buffer)

    def getheadersize(self):
        return len(self.msg_type + ":" + str(self.offset) + ":")

    def resetbuffer(self):
        self.buffer = ""


def saveimg(data, name, path):
    decoded_data = base64.b64decode(data)
    completepath = path + name
    #print(decoded_data)
    #print(completepath)
    file = open(completepath, "wb")
    file.write(decoded_data)
    file.close()


PORT = "COM5"
BAUD_RATE = 9600
encoded_img = " "


def main():
    print(" +-------------------------------------+")
    print(" | Image Receive Rest - Xbee to Python |")
    print(" +-------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)
    first_message = MessageBuffer()
    message = MessageBuffer()
    image_file = MessageBuffer()
    first_message.cont = True
    path = "/Users/Michael/Desktop/PICSFROMXBEE/"

    def data_receive_callback(xbee_message):
        xbeemsg = device.read_data()
        data = xbeemsg.data
        temp = data.decode("utf-8")
        print(temp)
        spliter = temp.split(':')
        if spliter[0] == "BN":
            first_message.msg_type = spliter[0]
            first_message.file_size = spliter[1]
            first_message.offset = spliter[2]
            first_message.buffer = spliter[3]  # file name
        elif spliter[0] == "DT":
            message.msg_type = spliter[0]
            message.offset = spliter[1]
            message.buffer = spliter[2]
            image_file.buffer = image_file.buffer + spliter[2]
        elif spliter[0] == "ED":
            message.msg_type = spliter[0]
            message.offset = spliter[1]
            message.buffer = spliter[2]
            image_file.buffer = image_file.buffer + spliter[2]
            print(image_file.buffer)
            print((len(image_file.buffer)))
            first_message.cont = False
            saveimg(image_file.buffer, first_message.buffer, path)
            image_file.resetbuffer()
        else:
            print("ERROR")

    try:
        device.open()
        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        while True:
            if first_message.cont:
                input()
            else:
                break

        print("here")

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(end - start)
