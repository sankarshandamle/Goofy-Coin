import datetime
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from hashlib import sha1
import random,os


class cryptography:
    def generate_key(self,name):
        self.cipher=AES.new(name+str('{'*(16-len(name))), AES.MODE_ECB,os.urandom(16))
        return sha1(str(self.cipher)).hexdigest()
    def encrypt(self,s):
        enc=self.cipher.encrypt(s+((16-len(s)%16)*'{'))
        temp=sha1(enc).hexdigest()
        id_database[temp]=enc
        id_username[temp]=s
        return temp
    def decrypt(self,public_id):
        to_encode=id_database[public_id]
        dec =  self.cipher.decrypt(to_encode).decode('utf-8')
        l=dec.count('{')
        return dec[:len(dec)-l]


class transaction_block:
    def __init__(self):
        self.transaction_id=id(self)
        print "transaction 1 was", self.transaction_id
        array.append(self.transaction_id)
        self.value=0
        self.time_stamp=datetime.datetime.utcnow()
        self.next=None
        self.prev=None
        self.mode='Un-used'
    def add_block(self,value,id):
        self.id=id_username[id]
        self.value=value
        self.next=None
        self.prev=None

class transaction_chain:
    def __init__(self):
        self.first_transaction=None
        self.last_transaction=None

    def get_block(self,id):
        current=self.first_transaction
        while current.transaction_id != id and current.next != None:
            current=current.next
        return current

    def add_coin(self,value,id):
        if id != p1:
            print "only " + id_username[p1] + " can add coins"
            return;

        if self.first_transaction==None:
            self.first_transaction=transaction_block()
            self.first_transaction.add_block(value,id)
            self.last_transaction=self.first_transaction
        elif self.first_transaction==self.last_transaction:
            self.last_transaction=transaction_block()
            self.last_transaction.add_block(value,id)
            self.first_transaction.next=self.last_transaction
            self.last_transaction.prev=None
        else:
            current=transaction_block()
            current.add_block(value,id)
            self.last_transaction.next=current
            self.last_transaction=current
            self.last_transaction.prev=None

    def add_transaction(self,user_no,transaction_id,to_id,from_id,payment):
        payer=self.get_block(transaction_id)
        if payer.id==crypt_entry[user_no].decrypt(from_id) and payer.value >= payment and payer.mode=='Un-used':
            payer.mode='Used'
            if self.first_transaction==None:
                self.first_transaction=transaction_block()
                self.first_transaction.add_block(payment,to_id)
                self.last_transaction=self.first_transaction
            elif self.first_transaction==self.last_transaction:
                self.last_transaction=transaction_block()
                self.last_transaction.add_block(payment,to_id)
                self.first_transaction.next=self.last_transaction
                self.last_transaction.prev=payer
            else:
                current=transaction_block()
                current.add_block(payment,to_id)
                self.last_transaction.next=current
                self.last_transaction=current
                self.last_transaction.prev=payer
                print "this new block " + str(current.transaction_id) + " is backwardly linked to " + str(payer.transaction_id) + " input transaction"

            #for new add_block
            new_block=transaction_block()
            new_block.add_block(payer.value-payment,from_id)
            self.last_transaction.next=new_block
            self.last_transaction=new_block
            self.last_transaction.prev=payer
            print "this new block " + str(new_block.transaction_id) + " is backwardly linked to " + str(payer.transaction_id) + " input transaction"
        else:
            print "something not right"


    def print_transaction_forward(self):
        current=self.first_transaction
        print current.value,current.id,current.mode,current.transaction_id
        while current.next != None:
            current=current.next
            print current.value,current.id,current.mode,current.transaction_id

#100 users allowed
crypt_entry=[cryptography() for i in range(100)]

#global count of user
count=0

#dict to store public_id with encryption
id_database={}

#dict to keep public_id with username
id_username={}

#global array for transaction id, not required if prompt provided.
array=[]

#adding two users
name=raw_input("Enter your username: ")
print "You are now Goofy"
k1=crypt_entry[count].generate_key(name)
p1=crypt_entry[count].encrypt(name)
d1=crypt_entry[count].decrypt(p1)
count=count+1
name=raw_input("Enter your username: ")
k2=crypt_entry[count].generate_key(name)
p2=crypt_entry[count].encrypt(name)
d2=crypt_entry[count].decrypt(p2)

L=transaction_chain()
L.add_coin(5,p1)
L.add_coin(10,p1)
L.add_transaction(0,array[0],p2,p1,3)
L.add_coin(4,p2)
L.add_transaction(0,array[0],p2,p1,8)
L.print_transaction_forward()
