def encrypt(text,s):
    result = ""
    # transver the plain text
    for i in range (len(text)):
        char = text[i]
        #encyption upercase characters in plain text
        if (char.isupper()):
            result += chr((ord(char) + s-65) % 26 + 65)
        else:
             result += chr((ord(char) + s - 97) % 26 +97)
             return result
text = "CEASER CIPHER DEMO"
s = 4
print("Plain text : "+ text)
print("Shift pattern : "+ str(s))
print("Cipher : " + encrypt(text,s))
