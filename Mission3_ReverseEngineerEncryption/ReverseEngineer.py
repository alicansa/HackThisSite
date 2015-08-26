import hashlib

def md5Hash(string):
	md5 = hashlib.md5();
	md5.update(string);
	return md5.hexdigest();

def evalCrossTotal(strMD5):
	intTotal = 0;
	for chars in strMD5:
	  intTotal += int(('0x0'+chars),16);
	
	return intTotal;

def encryptString(strString, strPassword):
      
	#strString is the content of the entire file with serials
	strPasswordMD5 = md5Hash(strPassword);
	intMD5Total = evalCrossTotal(strPasswordMD5);

	arrEncryptedValues = [];
	for i in xrange(0,len(strString)):

		arrEncryptedValues.append(ord(strString[i])
		                       +  int(('0x0' + strPasswordMD5[i%32]),16)
		                       -  intMD5Total);


		strStringMD5 = md5Hash(strString[0:i+1]);
		intMD5TotalMD5 = md5Hash(str(intMD5Total));


		intMD5Total = evalCrossTotal(strStringMD5[0: 16]
		                       +  intMD5TotalMD5[0: 16]);

		

	return arrEncryptedValues;

def decryptString(encString, strPassword):
	#strString is the content of the entire file with serials
	strPasswordMD5 = md5Hash(strPassword);
	intMD5Total = evalCrossTotal(strPasswordMD5);

	arrDecryptedValues = "";
	for i in xrange(0,len(encString)):

		arrDecryptedValues = arrDecryptedValues + chr(encString[i]
		                       -  int(('0x0' + strPasswordMD5[i%32]),16)
		                       +  intMD5Total);


		strStringMD5 = md5Hash(arrDecryptedValues[0:i+1]);
		intMD5TotalMD5 = md5Hash(str(intMD5Total));


		intMD5Total = evalCrossTotal(strStringMD5[0: 16]
		                       +  intMD5TotalMD5[0: 16]);

		

	return arrDecryptedValues;


def bruteCheckPoint(decString,depth):
	passFlag = True;
	if ((decString >= 65 and decString <= 90) or decString==10 or 
				decString==45 or decString==46 or (decString >= 48 and decString <= 57)):
						
		#checkpoints
		if (depth == 3 or (depth-3)%20==0): # -
			if (chr(decString) != '-'):
				# print(chr(decString) + " - checkpoint\n");
				passFlag = False;

		elif (depth == 7 or (depth-7)%20==0): # -
			if (chr(decString) != '-'):
				# print(chr(decString) + " - checkpoint\n");
				passFlag = False;

		elif (depth == 8 or (depth-8)%20==0): # O
			if (chr(decString) != 'O'):
				# print(chr(decString) + " O checkpoint\n");
				passFlag = False;


		elif (depth == 9 or (depth-9)%20==0): # E
			if (chr(decString) != 'E'):
				# print(chr(decString) + " E checkpoint\n");
				passFlag = False;

		elif (depth == 10 or (depth-10)%20==0): # M
			if (chr(decString) != 'M'):
				# print(chr(decString) + " M checkpoint\n");
				passFlag = False;

		elif (depth == 11 or (depth-11)%20==0): # -
			if (chr(decString) != '-'):
				# print(chr(decString) + " - checkpoint\n");
				passFlag = False;


		elif (depth == 15 or (depth-15)%20==0): # -
			if (chr(decString) != '-'):
				# print(chr(decString) + " - checkpoint\n");
				passFlag = False;


		elif (depth == 16 or (depth-16)%20==0): # 1
			if (chr(decString) != '1'):
				# print(chr(decString) + " 1 checkpoint\n");
				passFlag = False;


		elif (depth == 17 or (depth-17)%20==0): # .
			if (chr(decString) != '.'):
				# print(chr(decString) + " . checkpoint\n");
				passFlag = False;

		elif (depth == 18 or (depth-18)%20==0): # 1
			if (chr(decString) != '1'):
				# print(chr(decString) + " 1 checkpoint\n");
				passFlag = False;

		elif (depth == 19 or (depth-19)%20==0): # \n
			if (chr(decString) != '\n'):
				passFlag = False;
	else:
		passFlag = False;

	return passFlag;

def bruteDecrypt(encString):

	#guess the first crossTotal -> must be between 0 and 480
	for crossTotalGuess in xrange(100,480):
		# for crossTotalGuess in range(0,480):
		print(crossTotalGuess);
		solution = [];
		hashLookBook = {}; #contains the possible password hash combinations and their corresponding decrypted strings
		crossTotalLookBook = {} # contains crosstotalvalues for the corresponding password hash

		#initialize the lookbooks
		for hashValue in xrange(0,16):
			#decrypt guess
			decString = int(encString[0]) + crossTotalGuess - hashValue;
			if ((decString >= 65 and decString <= 90) or decString==10 or 
				decString==45 or decString==46 or (decString >= 48 and decString <= 57)):

				strHash= str(hex(hashValue))
				hashLookBook[strHash[2]] = chr(decString);
				strStringMD5 = md5Hash(chr(decString));

				intMD5TotalMD5 = md5Hash(str(crossTotalGuess));
				crossTotalLookBook[strHash[2]] = evalCrossTotal(strStringMD5[0: 16]
				                       +  intMD5TotalMD5[0: 16]);

		solution = bruteDecryptRecursive(1,encString,hashLookBook,crossTotalLookBook);
		if (solution is not None and len(solution) > 0):
			return solution;

def bruteDecryptRecursive(depth,encString,hashLookBook,crossTotalLookBook): #helper function for breadth first search, tree repeats itself after 32 steps
	#if we reach the end without any errors return the passhashvalues
	if (depth >= len(encString) or len(hashLookBook) == 0): #termination case
		return hashLookBook;
	else:
		newHashLookBook = {};
		newCrossTotalLookBook = {};
		#add the new values to the lookbook
		for key in hashLookBook:

			if (depth < 32):
				for hashValue in xrange(0,16):
					
					#decrypt guess
					decString = int(encString[depth]) + crossTotalLookBook[key] - hashValue;

					passFlag = bruteCheckPoint(decString,depth);
					
					if (passFlag is True):
						strHash= str(hex(hashValue));
						keyNew = key + strHash[2];
						newHashLookBook[keyNew] = hashLookBook[key] + chr(decString);

						strStringMD5 = md5Hash(newHashLookBook[keyNew]);
						intMD5TotalMD5 = md5Hash(str(crossTotalLookBook[key]));
						newCrossTotalLookBook[keyNew] = evalCrossTotal(strStringMD5[0: 16]
				                       +  intMD5TotalMD5[0: 16]);

			else:
				#decrypt guess
					decString = int(encString[depth]) + crossTotalLookBook[key] - int(('0x0' + key[depth%32]),16)

					passFlag = bruteCheckPoint(decString,depth);
					
					if (passFlag is True):
						newHashLookBook[key] = hashLookBook[key] + chr(decString);

						strStringMD5 = md5Hash(newHashLookBook[key]);
						intMD5TotalMD5 = md5Hash(str(crossTotalLookBook[key]));
						newCrossTotalLookBook[key] = evalCrossTotal(strStringMD5[0: 16]
				                       +  intMD5TotalMD5[0: 16]);	
					
					
		# decValues = decValues + chr(decString);
		del hashLookBook;
		del crossTotalLookBook;

		# print(depth);

		return bruteDecryptRecursive(depth+1,encString,newHashLookBook,newCrossTotalLookBook);

password = "test";
md5Password = md5Hash(password);
print(md5Password);

encString = "-132 -170 -152 -170 -208 -124 -202 -153 -146 -97 -122 -183 -127 -154 -169 -233 -179 -111 -197 -216 -114 -185 -117 -232 -167 -100 -95 -245 -171 -177 -144 -169 -116 -141 -159 -151 -186 -177 -200 -213 -123 -148 -244 -177 -198 -161 -138 -190 -119 -161 -110 -216 -148 -172 -87 -200 -140 -222 -152 -189 -181 -203 -225 -187 -192 -141 -140 -158 -203 -178 -186 -142 -173 -173 -119 -189 -191 -186 -142 -237 -177 -130 -128 -133 -149 -169 -145 -195 -152 -141 -167 -156 -147 -206 -211 -163 -188 -194 -199 -242";
encString = encString.split();

print(len(encString));
solution = bruteDecrypt(encString);
for key in solution:
	print solution[key];

