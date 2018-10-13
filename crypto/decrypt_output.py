import base64

encrypted_output = base64.decodestring("")
key = ""
decrypted_output = ""

for i in range(len(encrypted_output)):
	decrypted_output += chr(ord(encrypted_output[i])^ord(key[i%len(key)]))

print decrypted_output