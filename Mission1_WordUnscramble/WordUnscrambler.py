#	solution to the programming mission 1 of hackthissite.org
#	where we have to unscramble the scrambled words given from
#	a wordlist.
#
#
#	Author : Alican Salor
#	date : 26.09.2015


import HackThisSiteInterface as HTS 

def wordCompress(word):

	# words from the wordlist are compressed into a form where a letter and a number correspoding to how many times 
	# that letter appears in the given word  
	# hello -> h1e1l2o1

	compressed = [];
	pointer1=0;
	pointer2=0;
	letterCount = 0;
	while(len(word) > 0):
		
		removeIndex = [];
		letterCount = 0;
		index=word.find(word[0]);
		while(index >= 0):
			letterCount += 1;
			removeIndex.append(index);
			index=word.find(word[0],index+1);


		compressed.append(word[0] + str(letterCount));
		removeIndex.sort(reverse=True)
		for index in removeIndex:
			if (index == 0):
				word = word[1:len(word)];
			elif (index == (len(word)-1)):
				word = word[0:len(word)-1];
			else:
				word = word[0:index] + word[index+1:len(word)]; 

	return compressed;

def buildDict(fileName):
	#build a dictionary of each compressed word item (such as a1) mapping to the words that contain the key letter
	#in the given wordlist

	wordListDictionary = {};
	wordListFile = open(fileName,'r');

	for word in wordListFile:
		#loop over each letter and add the word to each letter in the dictionary
		#compress word as shown i.e alican -> a2 l1 i1 c1 n1
		compressed = wordCompress(word[0:len(word)-2]);
		for code in compressed:
			if (wordListDictionary.has_key(code) is False):
				wordListDictionary[code] = [];

			wordListDictionary[code].append(word[0:len(word)-2]);

	return wordListDictionary;

def unscrambleWords(scrambledWordFileName,wordListDictionary):
	# unscramble the words using the dictionary built
	# each scrambled word is compressed and then for each item of the compressed word 
	# words that contain these items in the wordlist are fetch (using a hashmap) into sets.
	# These sets are then intersected until there is only one element which is the unscrambled word

	wordListFile = open(scrambledWordFileName,'r');

	unscrambledWords = [];
	for scrambledWord in wordListFile:
		#parse through the letter until there is only one word left
		scrambledWord = scrambledWord[0:len(scrambledWord)-1];
		compresssedScrambled = wordCompress(scrambledWord);
		currentList = [];
		filteredList = [];
		for code in compresssedScrambled:
			currentList = wordListDictionary[code];
			#get the intersection of two lists
			if (len(filteredList) == 0):
				#first iteration
				filteredList = currentList;
			elif (len(filteredList) == 1):
				break;
			else:
				#get the intersection of lists;
				setCur = set(currentList);
				setFilt = set(filteredList);
				filteredList = list(setCur.intersection(setFilt));

		if (len(filteredList) > 1):
			for word in filteredList:
				if (len(word) != len(scrambledWord)):
					filteredList.remove(word);

		unscrambledWords.append(filteredList[0]);
		unscrambledWholeString = "";

		for index in range(0,len(unscrambledWords)):
			if (index == 0):
				unscrambledWholeString = unscrambledWords[index];
			else:
				unscrambledWholeString = unscrambledWholeString + "," + unscrambledWords[index];

	return unscrambledWholeString;


#build dictionary
wordListDictionary = buildDict("wordlist.txt");
#start mission and write the words into the words.txt file
unscrambledWords = unscrambleWords("words.txt",wordListDictionary);
print("unscrambled words are: ");
print(unscrambledWords);