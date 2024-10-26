#colum
import math
key= "TYCS"
def encrypt_message(msg):
    cipher=""
    k_indx=0
    msg_len=float(len(msg))
    msg_lst=list(msg)
    key_lst=sorted(list(key))
    col=len(key)
    row=int(math.ceil(msg_len/col))
    fill_null = int((row * col) - msg_len)
    msg_lst.extend("_"*fill_null)
    matrix = [msg_lst[i: i + col]
        for i in range(0,len(msg_lst),col)]
    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])
        cipher += "".join([row[curr_idx]
                        for row in matrix])
        k_indx += 1
    return cipher

msg = "NetworkSecurity"
cipher = encrypt_message(msg)
print("Encrypt message: {}".format(cipher))















#add

def encrypt(message, key):
    cipher = ""
    for i in message:
        if i.isupper():
            cipher += chr((ord(i) + key - 65) % 26+65)
        elif i.islower():
            cipher += chr((ord(i)+ key - 97) % 26+97)
        else:
            cipher+=""
    return cipher

message = input("Enter the plain text: ")
key = input("enter the key: ")
if key.isupper():
    key = ord(key) - 65
elif key.islower():
    key = ord(key) - 97
else:
    key = int(key)
print("Cipher text:",encrypt(message,key))






















#ver


def stringEncryption(text,key):
    cipherText = ""
    cipher = []
    for i in range(len(key)):
        cipher.append(ord(text[i]) - ord('A') + ord(key[i]) - ord('A'))
    for i in range(len(key)):
        if cipher[i] > 25:
            cipher[i] = cipher[i] -26
    for i in range(len(key)):
        x = cipher[i] + ord('A')
        cipherText += chr(x)
    return cipherText

plainText = "HelloTYCS"
key = "MONEYBANK"
encryptedText = stringEncryption(plainText.upper(),key.upper())
print("Cipher Text - ",encryptedText)






#railfence







def encryptRailFence(text,key):
    rail = [["\n" for i in range(len(text))]
            for j in  range (key)]
    dir_down = False
    row,col = 0,0
    for i in range(len(text)):
        if (row==0) or (row==key-1):
            dir_down = not dir_down
        rail[row][col] = text[i]
        col += 1
        if dir_down:
            row+=1
        else:
            row -=1
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != "\n":
                result.append(rail[i][j])
    return("".join(result))

def decryptRailFence(cipher,key):
    rail = [["\n" for i in range(len(cipher))]
            for j in range(key)]
    dir_down = None
    row,col = 0,0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row  == key - 1:
            dir_down = False
        rail[row][col] = "*"
        col += 1
        if dir_down:
            row +=1
        else:
            row -=1
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if((rail[i][j] == "*") and (index < len(cipher))):
                rail[i][j] = cipher[index]
                index += 1

    result = []
    row,col = 0,0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key-1:
            dir_down = False
        if (rail[row][col] != "*"):
            result.append(rail[row][col])
            col += 1
        if dir_down:
            row += 1
        else:
            row -= 1
    return("".join(result))

if __name__ == "__main__":
    print(encryptRailFence("HelloTYCS",2))
    print(encryptRailFence("NetworkSecurity",3))
    print(decryptRailFence("HloYSelTC",2))
    print(decryptRailFence("NoeiewrScrttkuy",3))









#cae
def encrypt_text(plaintext,n):
    ans = ""
    for i in range(len(plaintext)):
        ch = plaintext[i]
        if ch=="":
            ans+=""
        elif (ch.isupper()):
            ans += chr((ord(ch)+ n-65)%26+65)
        else:
            ans += chr((ord(ch) + n-97) %26+97)
    return ans

plaintext = "HELLO TYCS "
n = 2
print("Plain Text is: ",plaintext)
print("Shift Pattern is: ",str(n))
print("Cipher Text is: ",encrypt_text(plaintext,n))






































