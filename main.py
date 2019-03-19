from FileHandler import FileHandler
from TDESCipher import TDESCipher
import matplotlib.pyplot as plt # importación por alias
import matplotlib.pyplot as plt2
import os

def main():
    option = ""
    while option != "E":
        option = input("[C]ipher, [D]ecipher,[T]ime Trials, [E]xit: ").upper()
        if option=="E":
            exit()
        elif option=="T":
            timeTrial()
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

def timeTrial():
    keySize=int(input("Key size(16 or 24):"))
    files=("trial1.odt","trial2.pdf","trial3.pdf","trial4.tar.gz")
    path="timeTrial/"
    i=0
    filesSize=[]
    cbcTimes=[]
    ctrTimes=[]
    ofbTimes=[]
    cfbTimes=[]
    cbcDTimes=[]
    ctrDTimes=[]
    ofbDTimes=[]
    cfbDTimes=[]
    labels=("CBC encryption","CTR encryption","OFB encryption","CFB encryption")
    labelsD=("CBC encryption","CTR encryption","OFB encryption","CFB encryption")
    i=0
    for x in files:
        filesSize.append(os.stat(path+x).st_size/1024)
        dataFile=FileHandler.openFile(path+x)
        ##  CREAMOS UN OBJETO TDESCipher PARA CIFRAR O DESCIFRAR
        cipher=TDESCipher(keySize=keySize)
        ##  ESCRIBIMOS LA LLAVE EN UN ARCHIVOO
        FileHandler.saveCodedFile(path+"k{}.key".format(i),cipher.getKey())
        ciphered_data,timeA=cipher.cipherCBC(dataFile)
        cbcTimes.append(timeA)
        FileHandler.saveFile(path+"cbc_"+x,ciphered_data)
        print("For {}: size in encryption=>{}".format(x,len(ciphered_data)))
        #ciphered_data,timeB=cipher.cipherCTR(dataFile)
        #ctrTimes.append(timeB)
        #FileHandler.saveFile(path+"ctr_"+x,ciphered_data)

        #ciphered_data,timeC=cipher.cipherOFB(dataFile)
        #ofbTimes.append(timeC)
        #FileHandler.saveFile(path+"ofb_"+x,ciphered_data)

        #ciphered_data,timeD=cipher.cipherCFB(dataFile)
        #cfbTimes.append(timeD)
        #FileHandler.saveFile(path+"cfb_"+x,ciphered_data)
        i=i+1

    plt.plot(filesSize, cbcTimes, "o-", color="hotpink")
    #plt.plot(filesSize, ctrTimes, "o-", color="cornflowerblue")
    #plt.plot(filesSize, ofbTimes, "o-", color="lime")
    #plt.plot(filesSize, cfbTimes, "o-", color="red")
    #plt.legend(labels, loc='upper right')
    plt.title("Encryption time with {} key size".format(keySize))
    plt.show()

    i=0
    for x in files:
        #PARA DESCIFRAR
        ##  RECUPERAMOS LA LLAVE
        key=FileHandler.openCodedsFile(path+"k{}.key".format(i))

        dataFileC=FileHandler.openFile(path+"cbc_"+x)
        print("For {}: size=>{}".format(x,len(dataFileC)))
        iv=dataFileC[len(dataFileC)-8:len(dataFileC)]
        dataFileC=dataFileC[0:len(dataFileC)-8]
        
        cipher=TDESCipher(key=key,iv=iv)
        deciphered_data,time=cipher.decipherCBC(dataFileC)
        print("For {}: size after decipher=>{}".format(x,len(deciphered_data)))
        FileHandler.saveFile(path+"cbcD_"+x,deciphered_data)
        cbcDTimes.append(time)
        

        #dataFileC=FileHandler.openFile(path+"ctr_"+x)
        #iv=dataFileC[len(dataFileC)-8:len(dataFileC)]
        #dataFileC=dataFileC[0:len(dataFileC)-8]
        #cipher=TDESCipher(key=key,iv=iv)
        #deciphered_data,time=cipher.decipherCTR(dataFileC)
        #ctrDTimes.append(time)
        #FileHandler.saveFile(path+"ctrD_"+x,deciphered_data)

        #dataFileC=FileHandler.openFile(path+"ofb_"+x)
        #iv=dataFileC[len(dataFileC)-8:len(dataFileC)]
        #dataFileC=dataFileC[0:len(dataFileC)-8]
        #cipher=TDESCipher(key=key,iv=iv)
        #deciphered_data,time=cipher.decipherOFB(dataFileC)
        #ofbDTimes.append(time)
        #FileHandler.saveFile(path+"ofbD_"+x,deciphered_data)

        #dataFileC=FileHandler.openFile(path+"cfb_"+x)
        #iv=dataFileC[len(dataFileC)-8:len(dataFileC)]
        #dataFileC=dataFileC[0:len(dataFileC)-8]
        #cipher=TDESCipher(key=key,iv=iv)
        #deciphered_data,time=cipher.decipherCFB(dataFileC)
        #cfbDTimes.append(time)
        #FileHandler.saveFile(path+"cfbD_"+x,deciphered_data)
        i=i+1

    plt2.plot(filesSize, cbcDTimes, "o-", color="hotpink")
    #plt2.plot(filesSize, ctrDTimes, "o-", color="cornflowerblue")
    #plt2.plot(filesSize, ofbDTimes, "o-", color="lime")
    #plt2.plot(filesSize, cfbDTimes, "o-", color="blue")
    #plt2.legend(labels, loc='upper right')
    plt2.title("Decryption time with {} key size".format(keySize))
    plt2.show()
    
if __name__ == '__main__':
    main()