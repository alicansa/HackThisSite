import HackThisSiteInterface as HTS
from PIL import Image, ImageDraw
from StringIO import StringIO

#create a global hashmap for morse alphabet -> non ascii characters are not included 
morseAlphabet = {
					'.' : 'e',
					'..' : 'i',
					'...' : 's',
					'....' : 'h',
					'.....' : '5',
					'....-' : '4',
					'...-' : 'v',
					'...-.' : '',
					'...--' : '3',
					'..-' : 'u',
					'..-.' : 'f',
					'..-..' : '',
					'..--' : '',
					'..--.' : '',
					'..--..' : '?',
					'..--.-' : '_',
					'..---' : '2',
					'.-' : 'a',
					'.-.' : 'r',
					'.-..' : 'l',
					'.-..-' : '',
					'.-..-.' : '\"',
					'.-.-' : '',
					'.-.-.' : '+',
					'.-.-.-' : '.',
					'.--' : 'w',
					'.--.' : 'p',
					'.--..' : '',
					'.--.-' : '',
					'.--.-.' : '',
					'.---' : 'j',
					'.---.' : '',
					'.----' : '1',
					'.----.' : '\'',
					'-' : 't',
					'-.' : 'n',
					'-..' : 'd',
					'-...' : 'b',
					'-....' : '6',
					'-....-' : '-',
					'-...-' : '=',
					'-..-' : 'x',
					'-..-.' : '/',
					'-.-' : 'k',
					'-.-.' : 'c',
					'-.-..' : '',
					'-.--' : 'y',
					'-.--.' : '',
					'-.--.-' : '()',
					'--' : 'm',
					'--.' : 'g',
					'--..' : 'z',
					'--...' : '7',
					'--.-' : 'q',
					'--.-.' : '',
					'--.--' : '',
					'---' : 'o',
					'---.' : '',
					'---..' : '8',
					'---...' : ':',
					'----' : 'ch',
					'----.' : '9',
					'-----' : '0'
};

def getImage():

	#login to the site
	HTS.loginUserInput();
	#start the mission
	HTS.getPage("https://www.hackthissite.org/missions/prog/2/");
	#get the image
	im = Image.open(StringIO(HTS.getPage("https://www.hackthissite.org/missions/prog/2/PNG")));
	print("image downloaded \n")
	return im;

def analyseImage(image):
	print("analysing image \n");
	morseCode = "";
	pixelData = image.load();
	size = image.size;
	width = size[0]; #size[0] -> width
	height = size[1];
	prevx = 0;
	#iterate over the image and get the morse code
	for y in range(0,height):
		for x in range(0,width):
			print(x);
			if (pixelData[x,y] == 1): #white pixel
				morseCode = morseCode + chr((y*width+x)-prevx);
				prevx = (y*width+x);

	print(morseCode);

	return morseCode.split();

def decodeMorse(codeList):
	print("decoding morse \n");
	global morseAlphabet;
	decodedText = "";

	for code in codeList:
		decodedText = decodedText + morseAlphabet[code];

	return decodedText;

def sendResponse(decodedText):
	print(decodedText);
	print("sending solution")
	payload = {'solution' : decodedText, 'submitbutton' : 'submit'};
	return HTS.postPage("https://www.hackthissite.org/missions/prog/2/index.php",payload);
	



print(sendResponse(decodeMorse(analyseImage(getImage()))));