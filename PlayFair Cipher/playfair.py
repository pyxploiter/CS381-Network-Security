import re

#keep only alphabets and capitalize
def parseString(text):
	return re.sub(r"[^a-zA-Z]","",text.upper())
	
#remove duplicate characters in string
def removeDuplicateChar(text):
	while re.search(r'([a-zA-Z])(.*)\1', text):
		text = re.sub(r'([a-zA-Z])(.*)\1', r'\1\2', text)
	return text

#locate char in cipher table
def locateEntry(table, entry):
	return [(x,y) for x in xrange(5) for y in xrange(5) if table[x][y] == entry]

#create cipher table
def cipherTable(key):
	entries = []
	key = removeDuplicateChar(parseString(key))
	alphabet="ABCDEFGHIKLMNOPQRSTUVWXYZ"
	[entries.append(letter) for letter in key]
	[entries.append(letter) for letter in alphabet if letter not in entries]
	table = list()
	[table.append(entries[x:x+5]) for x in range(0,21,5)]
	return table

#encode plaintext
def encode(message, key):
	table = cipherTable(key)
	message = parseString(message)
	msg_pairs, message_arr, codedText = list(), list(), list()
	[message_arr.append(e) for e in message]
	#add X if duplicate char found in pair
	[message_arr.insert(x+1, "X") for x in range(0, len(message_arr)-1, 2) if message_arr[x] == message_arr[x+1]]
	#add X if length of message is odd
	message_arr.append("X") if len(message_arr)%2 == 1 else None
	#convert message into pairs
	[msg_pairs.append(message_arr[x:x+2]) for x in range(0, len(message_arr)-1, 2)]
	for pair in msg_pairs:
		row1, col1 = locateEntry(table, pair[0])[0]
		row2, col2 = locateEntry(table, pair[1])[0]
		#for same row
		if (row1 == row2):
			col1 = -1 if col1 == 4 else col1
			col2 = -1 if col2 == 4 else col2
			codedText.append(table[row1][col1+1])
			codedText.append(table[row2][col2+1])
		#for same column
		elif (col1 == col2):
			row1 = -1 if row1 == 4 else row1
			row2 = -1 if row2 == 4 else row2
			codedText.append(table[row1+1][col1])
			codedText.append(table[row2+1][col2])
		else:
			codedText.append(table[row1][col2])
			codedText.append(table[row2][col1])
	return "".join(codedText)

def decode(codedText, key):
	table = cipherTable(key)
	msg_pairs = list()
	#convert message into pairs
	[msg_pairs.append(codedText[x:x+2]) for x in range(0, len(codedText)-1, 2)]
	plainText = list()
	for pair in msg_pairs:
		row1, col1 = locateEntry(table, pair[0])[0]
		row2, col2 = locateEntry(table, pair[1])[0]
		#for same row
		if (row1 == row2):
			col1 = -1 if col1 == 4 else col1
			col2 = -1 if col2 == 4 else col2
			plainText.append(table[row1][col1-1])
			plainText.append(table[row2][col2-1])
		#for same column
		elif (col1 == col2):
			row1 = -1 if row1 == 4 else row1
			row2 = -1 if row2 == 4 else row2
			plainText.append(table[row1-1][col1])
			plainText.append(table[row2-1][col2])
		else:
			plainText.append(table[row1][col2])
			plainText.append(table[row2][col1])
	#remove extra 'X'
	[plainText.remove("X") for i in range(len(plainText)) if "X" in plainText]
	plainText = "".join(plainText)
	return plainText.lower()

if __name__ == "__main__":
	while 1:
		print "-----------------------"
		print "==> Playfair Cipher <=="
		print "-----------------------"
		print "\n1. Encode \n2. Decode"
		choice = raw_input("\nChoose: ")
		if choice == "1":
			key = raw_input("Enter the key: ")
			msg = raw_input("Enter the message: ")
			table = cipherTable(key)
			print "Cipher Table:"
			for x in range(5):
				print(table[x])
			print "\nCipher: "+encode(msg, key)
		elif choice == "2":
			key = raw_input("Enter the key: ")
			cipher = raw_input("Enter the cipher: ")
			table = cipherTable(key)
			print "Cipher Table:"
			for x in range(5):
				print(table[x])
			print "\nPlain Text: "+ decode(cipher, key)
		
