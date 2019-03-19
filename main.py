#Morales Flores Victor Leonel
#ESCOM-IPN(MX)
#18/03/2019

from FileHandler import FileHandler
from TDESCipher import TDESCipher
import os

def main():
    option = ""
    while option != "E":
        option = input("[C]ipher, [D]ecipher, [E]xit: ").upper()
        if option=="E":
            exit()
        else:
            fileName=input("File name:")
            operationMode=input("Chose the mode operation(CBC,CTR,OFB,CFB):").upper()
            keyFileName=input("Key file name:")
            if option=="C":
                keySize=int(input("Key size(16 or 24):"))
                #PARA CIFRAR
                ##  ABRIMOS EL ARCHIVO Y RECUPERAMOS LOS BYTES
                dataFile=FileHandler.openFile(fileName)
                ##  CREAMOS UN OBJETO TDESCipher PARA CIFRAR O DESCIFRAR
                cipher=TDESCipher(keySize=keySize)
                ##  ESCRIBIMOS LA LLAVE EN UN ARCHIVOO
                FileHandler.saveCodedFile(keyFileName,cipher.getKey())
                #  CIFRAMOS EL ARCHIVO
                if operationMode=="CBC":
                    ciphered_data,time=cipher.cipherCBC(dataFile)
                elif operationMode=="CTR":
                    ciphered_data,time=cipher.cipherCTR(dataFile)
                elif operationMode=="OFB":
                    ciphered_data,time=cipher.cipherOFB(dataFile)
                elif operationMode=="CFB":
                    ciphered_data,time=cipher.cipherCFB(dataFile)
                
                
                print("Time encrypting:"+str(time))
                ##  CONCATENAMOS IV PARA PODER DESCIFRAR
                ciphered_data+=cipher.getIV()
                ##  GUARDAMOS EL ARCHIVO CIFRADO
                FileHandler.saveFile("c_"+fileName,ciphered_data)
            elif option=="D":
                #PARA DESCIFRAR
                ##  RECUPERAMOS LA LLAVE
                key=FileHandler.openCodedsFile(keyFileName)
                ##  ABRIMOS EL ARCHIVO CIFRADO
                dataFileC=FileHandler.openFile(fileName)
                ##  RECUPERAMOS IV DEL ARCHIVO CIFRADO
                iv=dataFileC[len(dataFileC)-8:len(dataFileC)]
                #print(iv)
                ## RETIRAMOS EL VALOR DE IV DEL ARCHIVO CIFRADO
                dataFileC=dataFileC[0:len(dataFileC)-8]
                ##  CREAMOS UN OBJETO TDESCipher PARA CIFRAR O DESCIFRAR
                cipher=TDESCipher(key=key,iv=iv)
                ##  DESCIFRAMOS EL ARCHIVO
                if operationMode=="CBC":
                    deciphered_data,time=cipher.decipherCBC(dataFileC)
                elif operationMode=="CTR":
                    deciphered_data,time=cipher.decipherCTR(dataFileC)
                elif operationMode=="OFB":
                    deciphered_data,time=cipher.decipherOFB(dataFileC)
                elif operationMode=="CFB":
                    deciphered_data,time=cipher.decipherCFB(dataFileC)

                print("Time decrypting:"+str(time))
                ## GUARDAMOS EL ARCHIVO DESCIFRADO
                FileHandler.saveFile("d_"+fileName,deciphered_data)


if __name__ == '__main__':
    main()