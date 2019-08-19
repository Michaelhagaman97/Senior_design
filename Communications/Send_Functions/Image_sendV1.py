
from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import XBee64BitAddress
import os
import base64
import time

class MessageBuffer:
    msg_type = ""
    file_size = 0 #max file size
    offset = 0 #number of bytes sent?
    buffer = "" #data to be sent
    len = 0 #len of msg sent this is for the last message so you dont read to much

    def printObj(self):
        print("Msg_type: " + self.msg_type + " File Size: " + str(self.file_size) + " Offset: " + str(
            self.offset) + " Buffer: " + self.buffer)

    def firstmsg(self):
        return self.msg_type + ":" + str(self.file_size) + ":" + str(self.offset) + ":" + self.buffer

    def prepmsg(self):
        return self.msg_type + ":" + str(self.offset) + ":" + str(self.buffer)

    def getheadersize(self):
        return len(self.msg_type + ":" + str(self.offset) + ":")


PORT = "COM4"
BAUD_RATE = 9600


def main():
    print(" +----------------------------------+")
    print(" | Image send test - Xbee to Python |")
    print(" +----------------------------------+\n")
    Overallstart = time.time()
    dir = "/Users/IEEE/Desktop/Hog-pics/"
    pics = os.listdir("/Users/IEEE/Desktop/Hog-pics")
    device = XBeeDevice(PORT, BAUD_RATE)
    for img in pics: #put everything in this loop so you until you send all the pic in the dir
        with open(dir + img, 'rb') as image:
            t0 = time.time()
            f = image.read()
            teststring = base64.b64encode(f)
            test1 = teststring.decode("utf-8")

            first_message = MessageBuffer()
            first_message.msg_type = 'BN'
            first_message.file_size = len(test1)
            first_message.offset = 0
            first_message.buffer = img  # filename

            s = first_message.firstmsg()
            print(s)

            try:
                device.open()
                device.send_data_broadcast(s)

                message = MessageBuffer()
                place = 0
                headersize = 0
                MAXbuffersize = 256
                buffersize = 0
                next_sting = 0
                packetcount = 0
                while place < first_message.file_size:

                    if first_message.file_size - place > 255:
                        message.msg_type = 'DT'
                    else:
                        message.msg_type = 'ED'

                    message.offset = place
                    headersize = message.getheadersize()
                    buffersize = MAXbuffersize - headersize
                    next_sting = buffersize + next_sting
                    message.buffer = test1[message.offset:next_sting]
                    place = buffersize + place
                    q = message.prepmsg()
                    #print(q)
                    device.send_data_broadcast(q)
                    packetcount = packetcount + 1

                t1 = time.time()
                total = t1 - t0
                print("Success")
                print("Number of Packets: " + str(packetcount))
                print("Time for Image " + first_message.buffer + ": " + str(total))
                print("Size for Image " + first_message.buffer + ": " + str(first_message.file_size))

            finally:
                if device is not None and device.is_open():
                    device.close()

    Overallend = time.time()
    overall = Overallend - Overallstart
    print("Overall time = " + str(overall))


if __name__ == '__main__':
    main()