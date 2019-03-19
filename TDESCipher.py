#Morales Flores Victor Leonel
#ESCOM-IPN(MX)
#18/03/2019

from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES3
from Crypto.Util.py3compat import *
from Crypto import Random
from Crypto.Util import Counter
from time import time
class TDESCipher:
    
    def __init__(self,keySize=None,key=None,iv=None):
        if key is None:
            if keySize is None:
                self.__key=Random.new().read(16)
            else:
                self.__key=Random.new().read(keySize)
        else:
            self.__key=key
        if iv is None:
            self.__iv=Random.new().read(DES3.block_size)
        else:
            self.__iv=iv
        
####################PADDING##########################
    def padding(self,data):
        block_size=DES3.block_size
        padding_len = block_size-len(data)%block_size
        print(padding_len )
        padding = bchr(padding_len)*padding_len
        data=data+padding
        print("padding:"+str(padding))
        return data


    def unpadding(self,data):        
        block_size=DES3.block_size
        padding_len = block_size-len(data)%block_size
        pdata_len = len(data)
        if pdata_len % block_size:    
            print("Input data is not padded")
        else:
            padding_len = bord(data[-1])
            data=data[:-padding_len]
            print("Padding len:{}".format(padding_len))
        print(padding_len )
        #if data[-padding_len:]!=bchr(padding_len)*padding_len:
        #    raise ValueError("PKCS#7 padding is incorrect.")
        
        return data
    
    
    
    
#########CIPHER#########
    def __generalCipher(self,data,mode):
        initial_time=time()
        cipherO = DES3.new(self.__key,mode, self.__iv)
        ciphered_data=cipherO.encrypt(self.padding(data))
        final_time=time()
        total_time=final_time-initial_time
        return ciphered_data,total_time


    def cipherCTR(self,data):
        initial_time=time()
        ctr = Counter.new(DES3.block_size*8,initial_value=int.from_bytes(self.__iv, byteorder='big', signed=False))
        cipherO = DES3.new(self.__key, DES3.MODE_CTR,counter=ctr)
        ciphered_data=cipherO.encrypt(data)
        final_time=time()
        total_time=final_time-initial_time
        return ciphered_data,total_time
    def cipherCBC(self,data):
        return self.__generalCipher(data,DES3.MODE_CBC)
    def cipherOFB(self,data):
        return self.__generalCipher(data,DES3.MODE_OFB)
    def cipherCFB(self,data):
        return self.__generalCipher(data,DES3.MODE_CFB)

#########DECIPHER#########
    def __generalDecipher(self,data,mode):
        
        initial_time=time()
        cipherO = DES3.new(self.__key, mode, self.__iv)
        deciphered_data=cipherO.decrypt(data)
        deciphered_data=self.unpadding(deciphered_data)
        final_time=time()
        total_time=final_time-initial_time
        return deciphered_data,total_time

    def decipherCBC(self,data):
        return self.__generalDecipher(data,DES3.MODE_CBC)
    def decipherOFB(self,data):
        return self.__generalDecipher(data,DES3.MODE_OFB)
    def decipherCFB(self,data):
        return self.__generalDecipher(data,DES3.MODE_CFB)

    def decipherCTR(self,data):
        initial_time=time()
        ctr = Counter.new(DES3.block_size*8,initial_value=int.from_bytes(self.__iv, byteorder='big', signed=False))
        cipherO = DES3.new(self.__key, DES3.MODE_CTR,counter=ctr)
        deciphered_data=cipherO.decrypt(data)
        final_time=time()
        total_time=final_time-initial_time
        return deciphered_data,total_time
#########GETTERS#########
    def getKey(self):
        return self.__key

    def getIV(self):
        return self.__iv
#########SETTERS#########
    def setKey(self,key):
        self.__key=key

    def settIV(self,iv):
        self.__iv=iv




    