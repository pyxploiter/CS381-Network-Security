import random
import copy

cipherTab = {'a': ["10", "48", "22", "36", "24", "13", "42", "06"],
			'b': ["37"],
			'c': ["57", "77", "92"],
			'd': ["99", "56", "96", "30"],
			'e': ["89", "85", "47", "28", "91", "63", "55", "09", "07", "11", "51", "08"],
			'f': ["02", "01"],
			'g': ["52", "16"],
			'h': ["05", "66", "54", "32", "29", "33"],
			'i': ["81", "67", "00", "74", "58", "72", "71"],
			'j': ["69"],
			'k': ["25"],
			'l': ["76", "17", "95", "46"],
			'm': ["50", "15"],
			'n': ["04", "98", "34", "70", "53", "97"],
			'o': ["90", "64", "40", "18", "62", "73", "49"],
			'p': ["38", "93"],
			'q': ["31"],
			'r': ["78", "20", "59", "39", "21", "26"],
			's': ["88", "65", "79", "94", "83", "27"],
			't': ["41", "35", "68", "19", "87", "82", "60", "23", "14", "43"],
			'u': ["12", "61", "84"],
			'v': ["44"],
			'w': ["86", "45"],
			'x': ["80"],
			'y': ["03"],
			'z': ["75"]}

def encrypt(text, cipherTable):
	text = text.lower()
	cipherText = []
	for letter in text:
		if (letter.isalpha()):
			substitutionList = cipherTable[letter]
			replace = random.randint(0,len(substitutionList)-1)
			cipherText.append(substitutionList[replace])
		else:
			cipherText.append(letter)
	
	return ''.join(cipherText)

def decrypt(text, cipherTable):
	plainText = copy.deepcopy(text)
	counter = 0
	loopcounter = len(text)

	for i in range(0, loopcounter, 2):
		#break if cipher text is complete
		if (i+counter+1 >= len(text)):
			break
		#ignore the non-digits
		if (not text[i+counter].isdigit()):
			counter += 1
		
		#get pair of letters
		cipherLetter = text[i+counter:i+counter+2]
		
		#find key against value 
		for key, value in cipherTable.items():
			
			if (cipherLetter in value):
				plainText = plainText.replace(cipherLetter, key, 1)
	return plainText

print ("1. Encrypt Message \n2. Decrypt Message")
option = int(raw_input("\nSelect option: "))
if (option == 1):
	plainText = raw_input("> Enter Plain Text:- \n")
	print ("\n> Cipher Text:- \n"+encrypt(plainText, cipherTab))
elif (option == 2):
	cipherText = message = raw_input("> Enter Cipher Text:- \n")
	print ("\n> Plain Text:- \n"+decrypt(cipherText, cipherTab))
else:
	print ("Invalid option.")