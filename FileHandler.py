import codecs
import base64

class FileHandler:
    @staticmethod 
    def openFile(fileName):
        file = open(fileName,"rb")
        data = file.read()
        file.close()
        return data
    @staticmethod 
    def saveFile(fileName,data):
        file = open(fileName,"wb")
        data = file.write(data)
        file.close()
    @staticmethod 
    def openCodedsFile(fileName):
        with open(fileName, "rb") as file:
           data=file.read()
           file.close()
        return base64.b64decode(data)
    @staticmethod 
    def saveCodedFile(fileName,data):
        b64= base64.b64encode(data)
        with open(fileName, "wb") as file:
            file.write(b64)
            file.close()