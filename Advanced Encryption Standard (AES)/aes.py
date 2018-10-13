from Crypto.Cipher import AES
from Crypto import Random
import binascii
from PIL import Image

def encrypt(key, msg, iv):
	#padding with spaces
	while (len(msg)%16 != 0):
		msg+=" "
	return binascii.hexlify((AES.new(key, AES.MODE_CBC, iv)).encrypt(msg))
	
def decrypt(key, cipher, iv):
	return (AES.new(key, AES.MODE_CBC, iv)).decrypt(binascii.unhexlify(cipher))

def encrypt_image(key, filename):
	imgPixelArray = []
	#open image
	img = Image.open(filename)
	#load image pixels
	img_pix = img.load()

	#get image dimensions
	img_w = img.size[0]
	img_h = img.size[1]
	
	#append image pixels in array
	for y in range(0,img_h):
		for x in range(0,img_w):
			imgPixelArray.append(img_pix[x,y])

	plainTextImg = ""
	# add 100 to each tuple value to make sure each are 3 digits long.  
	for i in range(0,len(imgPixelArray)):
		for j in range(0,3):
			aa = int(imgPixelArray[i][j])+100
			plainTextImg = plainTextImg + str(aa)

	# length save for encrypted image reconstruction
	enc_length = len(imgPixelArray)

    # append dimensions of image for reconstruction after decryption
	plainTextImg += "h" + str(img_h) + "h" + "w" + str(img_w) + "w"
	
	# make sure that plantextstr length is a multiple of 16 for AES.  if not, append "n". 
	while (len(plainTextImg) % 16 != 0):
		plainTextImg = plainTextImg + "n"

	# encrypt plaintext
	obj = AES.new(key, AES.MODE_ECB)
	ciphertext = obj.encrypt(plainTextImg)

	asciicipher = binascii.hexlify(ciphertext)
	def replace_all(text, dic):
		for i, j in dic.iteritems():
			text = text.replace(i, j)
		return text

    # use replace function to replace ascii cipher characters with numbers
	reps = {'a':'1', 'b':'2', 'c':'3', 'd':'4', 'e':'5', 'f':'6', 'g':'7', 'h':'8', 'i':'9', 'j':'10', 'k':'11', 'l':'12', 'm':'13', 'n':'14', 'o':'15', 'p':'16', 'q':'17', 'r':'18', 's':'19', 't':'20', 'u':'21', 'v':'22', 'w':'23', 'x':'24', 'y':'25', 'z':'26'}
	asciiciphertxt = replace_all(asciicipher, reps)

    # construct encrypted image
	step = 3
	imgFirstCopy=[asciiciphertxt[i:i+step] for i in range(0, len(asciiciphertxt), step)]
    
    # if the last pixel RGB value is less than 3-digits, add a digit a 1
	if int(imgFirstCopy[len(imgFirstCopy)-1]) < 100:
		imgFirstCopy[len(imgFirstCopy)-1] += "1"
    
    # check to see if we can divide the string into partitions of 3 digits.  if not, fill in with some garbage RGB values
	if len(imgFirstCopy) % 3 != 0:
		while (len(imgFirstCopy) % 3 != 0):
			imgFirstCopy.append("101")

	imgFinal=[(int(imgFirstCopy[int(i)]),int(imgFirstCopy[int(i+1)]),int(imgFirstCopy[int(i+2)])) for i in range(0, len(imgFirstCopy), step)]

	while (int(enc_length) != len(imgFinal)):
		imgFinal.pop()

	encim = Image.new("RGB", (int(img_w),int(img_h)))
	encim.putdata(imgFinal)
	encim.save(filename+"_encrypt.jpeg")
	encim.show()

#16 byte random Initialization Vector
iv = Random.new().read(AES.block_size)
#16 byte random key
key = Random.new().read(AES.block_size)

while 1:
	print ("--------------------------------")
	print ("==> Advanced Encryption Standard\n")
	print ("1. Encrypt text\n2. Decrypt text\n3. Encrypt Image\n")
	option = int(raw_input("Select option: "))
	print ("--------------------------------")
	if (option == 1):
		plainText = raw_input("Enter Plain Text: ")
		print ("Random key: "+ binascii.hexlify(key))
		print ("Cipher Text: "+ encrypt(key, plainText, iv))

	elif (option == 2):
		cipherText = raw_input("Enter Cipher Text: ") 
		print ("Random key: "+ binascii.hexlify(key))
		print ("Plain Text: "+ decrypt(key, cipherText, iv))
	
	elif (option == 3):
		filename = raw_input("Enter file name: ")
		encrypt_image(key, filename)
	else:
		print ("Invalid option")