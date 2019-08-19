import os
import base64

'''
Message Types
BN = Begin, start of transfer. tells the receiver the file name and size of the file 
DT = Data Transfer, sends the offset and the encoded file
ED = End, lets the receiver know that we are done sending data
'''
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

path = "/Users/IEEE/Desktop/Hog-pics/"
pics = os.listdir("/Users/IEEE/Desktop/Hog-pics")

for img in pics:
    with open(path+img , 'rb') as image:
        f = image.read()
        temp = "Everyone believes Ant-Man could kill Thanos by shrinking, going up his asshole, and expanding. I thought about this, and I can’t think of a worse death.. for Ant-man. Thanos is pretty tough, like can take some punches from the Hulk kind-of-tough, well his butthole and insides have to be hulk-level strong too."
        teststring = base64.b64encode(f)
        test1 = teststring.decode("utf-8")

        first_message = MessageBuffer()
        first_message.msg_type = 'BN'
        first_message.file_size = len(test1)
        first_message.offset = 0
        first_message.buffer = img #filename
        first_message.printObj()
        s = first_message.firstmsg()

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
            packetcount = packetcount + 1

        print(packetcount)

