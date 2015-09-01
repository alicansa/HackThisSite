import HackThisSiteInterface as HTS

def reverseAsciiShift(encodedData,delimiter,shift):

	encodedDataArr = encodedData.split(delimiter);
	decodedString = "";
	for item in encodedDataArr:
		decodedString = decodedString + chr(int(item)-shift);

	return decodedString;

def downloadData():
	#login
	HTS.loginUserInput();
	#start mission and get the page
	response = HTS.getPage("https://www.hackthissite.org/missions/prog/11/");

	#parse content and get the data
	# we have to mine the code starting with Generated String and Shift;
	javascriptCode = response.content;
	mineStartIndex = javascriptCode.find("Generated String: ");

	#find the first non-numeric character which is used as the delimiter
	delimiter = "";
	mineEndIndex = javascriptCode.find("<",mineStartIndex);
	encodedData = javascriptCode[mineStartIndex + 18:mineEndIndex];

	encodedData = encodedData[0:len(encodedData)-1];
	for chars in encodedData:
		if (chars.isdigit() is False):
			delimiter = chars;
			break;

	mineStartIndex = javascriptCode.find("Shift: ");
	mineEndIndex = javascriptCode.find("<",mineStartIndex);
	shift = javascriptCode[mineStartIndex + 6:mineEndIndex];

	return [encodedData, delimiter, shift];

def sendSolution(solution):
	print("sending solution");
	payload = {'solution' : solution, 'submitbutton' : 'submit'};
	response = HTS.postPage("https://www.hackthissite.org/missions/prog/11/index.php",payload);
	print("solution response: \n");
	print(response.content);
	return;


data = downloadData();
solution = reverseAsciiShift(data[0],data[1],int(data[2]));
sendSolution(solution);