# 	The solution to the HackThisSite programming mission 6 where you have write the text given as an image on the
# 	challenge page. The problem is that the text is pretty long. Thus we have to develop an OCR algorithm to analyze
# 	the image and find what letters are used. Two different methods can be used in this challenge. One is to use a
# 	real OCR algorithm and decide on the letters according to some heuristics measures by looking at each pixel.
# 	Another method that can be used is to mine the data that is used to draw the image that we have to analyze.
# 	This data can be found in the javascript code on the challenge page. This data has to be mined so that data
#   corresponding to each letter is grouped and isolated. Afterwards this isolated data can be analysed 
# 	further with heuristics measures and a decision can be made on what letter is used. 

#
#	To use this module requests must be installed. 	
#	> pip install requests 
#
#
#	Author : Alican Salor
#	date : 02.09.2015

import HackThisSiteInterface as HTS
import math


letterLookUp ={

	(2,2) : '0',
	(3,0) : ['1','4','7','A','F'],
	(2,1) : '2',
	(1,2) : '3',
	(3,1) : ['5','D'],
	(1,1) : ['6','9'],
	(0,2) : '8',
	(4,2) : 'B',
	(0,1) : 'C',
	(4,0) : 'E'
}


def organizeData(data):

	#this function is used to organize the image data obtained from the javascript code, according to whether the data corresponds to a line or arc

	dataArr = data.split(",");
	organizedData = [];
	index = 0;

	while (index < len(dataArr)):
		if (int(dataArr[index+2]) >= 10): #line
			organizedData.append([int(dataArr[index]),int(dataArr[index+1]),
								int(dataArr[index+2]),int(dataArr[index+3])]);
			index += 4;
		else: #arc
			organizedData.append([int(dataArr[index]),int(dataArr[index+1]),
							int(dataArr[index+2]),int(dataArr[index+3]),int(dataArr[index+4])]);
			index += 5;

	return organizedData;

def findMaxY(organizedData):

	#find the max y coordinate of a given data

	maxY = -10000000000;

	for item in organizedData:
		if (len(item) == 5): #arc
			if (item[1] + item[2] >= maxY):
				maxY = item[1] + item[2];

		else: #line

			if (item[1] >= maxY and item[1] >= item[3]):
				maxY = item[1];
			elif (item[3] >= maxY and item[3] >= item[1]):
				maxY = item[3];

	return maxY;

def findMinMax(organizedData):

	# this function is used to find the minimun and maximum x/y coordinates occuring in the
	# data that is used to draw the image 
	# Afterwards these max/min x/y coordinates are used for finding the center of the spiral

	minX = 1000000000;
	minY = minX;
	maxX = -100000000;
	maxY = maxX;

	for item in organizedData:
		#check if line or arc
		if (len(item) == 5): #arc
			if (item[0]+item[2] > maxX):
				maxX = item[0] + item[2];

			if (item[0] - item[2] < minX):
				minX = item[0] - item[2];

			if (item[1] + item[2] > maxY):
				maxY = item[1] + item[2];

			if (item[1] - item[2] < minY):
				minY = item[1] - item[2];

		else: #line

			if (item[0] <= minX and item[0] <= item[2]):
				minX = item[0];
			elif (item[2] <= minX and item[2] <= item[0]):
				minX = item[2];

			if (item[0] >= maxX and item[0] >= item[2]):
				maxX = item[0];
			elif (item[2] >= maxX and item[2] >= item[0]):
				maxX = item[2];

			if (item[1] <= minY and item[1] <= item[3]):
				minY = item[1];
			elif (item[3] <= minY and item[3] <= item[1]):
				minY = item[3];

			if (item[1] >= maxY and item[1] >= item[3]):
				maxY = item[1];
			elif (item[3] >= maxY and item[3] >= item[1]):
				maxY = item[3];


	return [maxX,minX,maxY,minY];

def findCenter(maxX,minX,maxY,minY):

	# this function is used to find the center of the spiral. This function is integral to grouping and isolating the 
	# letter data

	spiralUpDelta = 268;
	spiralDownDelta = 227;
	centerXShift = 15;
	centerYShift = 5;

	return [round((maxX+minX)/2)+centerXShift,round(((maxY-spiralDownDelta)+(minY+spiralUpDelta))/2)-centerYShift];

def reverseTranslateBoundingBox(center,boundingBoxData):

	# translate x/y coordinates of the given data which has the origin as center of the spiral back to the 
	# original origin 

	reversedData = [];
	for item in boundingBoxData:
		reversedData.append([item[0]+center[0],center[1]-item[1]]);


	return reversedData;

def reverseTranlateBoundedData(center,boundedData):

	# translate x/y coordinates of the given data which has the origin as center of the spiral back to the 
	# original origin 

	reversedData=[];

	for item in boundedData:
		if (len(item) == 5): #arc
			reversedData.append([item[0]+center[0],center[1]-item[1],item[2],item[3],item[4]]);
		else: #line
			reversedData.append([item[0]+center[0],center[1]-item[1],item[2]+center[0],center[1]-item[3]]);

	return reversedData;

def translateBoundingBox(center,boundingBoxData):

	# translate x/y coordinates of the given data which has the original origin to the 
	# center of spiral as the new origin

	translatedData = [];
	for item in boundingBoxData:
		translatedData.append([item[0]-center[0],center[1]-item[1]]);
			
	return translatedData;

def translateBoundedData(center,boundedData):

	# translate x/y coordinates of the given data which has the original origin to the 
	# center of spiral as the new origin

	translatedData=[];

	for item in boundedData:
		if (len(item) == 5): #arc
			translatedData.append([item[0]-center[0],center[1]-item[1],item[2],item[3],item[4]]);
		else: #line
			translatedData.append([item[0]-center[0],center[1]-item[1],item[2]-center[0],center[1]-item[3]]);

	return translatedData;

def rotateBoundingBox(deg,boundingBoxData):
	#rotate the given data around the center of the spiral
	#use a rotation matrix
	rad = -1*(math.pi*deg)/180;
	rotatedData = [];
	for item in boundingBoxData:
			newX = math.cos(rad)*item[0] - math.sin(rad)*item[1];
			newY = math.sin(rad)*item[0] + math.cos(rad)*item[1];

			rotatedData.append([round(newX),round(newY)]);

	return rotatedData;

def rotateBoundedData(deg,boundedData):
	#rotate the given data around the center of the spiral
	#use a rotation matrix

	rotatedData=[];
	rad = -1*(math.pi*deg)/180;
	for item in boundedData:
		if (len(item) == 5): #arc
			newX = math.cos(rad)*item[0] - math.sin(rad)*item[1];
			newY = math.sin(rad)*item[0] + math.cos(rad)*item[1];

			rotatedData.append([round(newX),round(newY),item[2],item[3]-deg,item[4]]);
		else: #line
			newX1 = math.cos(rad)*item[0] - math.sin(rad)*item[1];
			newY1 = math.sin(rad)*item[0] + math.cos(rad)*item[1];
			newX2 = math.cos(rad)*item[2] - math.sin(rad)*item[3];
			newY2 = math.sin(rad)*item[2] + math.cos(rad)*item[3];

			rotatedData.append([round(newX1),round(newY1),round(newX2),round(newY2)]);

	return rotatedData;

def getBoundingBoxData(center,minY,width):

	# return the coordinates of the bounding box that is used to isolate the letter data at a given rotation
	# degree


	return [[center[0]-width/2,minY-10],
			[center[0]+width/2,minY-10],
			[center[0]-width/2,center[1]],
			[center[0]+width/2,center[1]]];

def getLineFunctionCoeff(x1,x2,y1,y2):

	# we have an analytic model for the box bounding the letters
	# y = a + bx -> we return [a b]

	b = (y2-y1)/(x2-x1);
	a = y1-b*x1;

	return [a ,b];

def data2TextDistance(boundedLetter):
	#get the distance between each point and sum it
	sum=0;
	for itemIndex1 in xrange(0,len(boundedLetter)):
		for itemIndex2 in xrange(itemIndex1,len(boundedLetter)):
			if (len(boundedLetter[itemIndex1])==5):
				if (len(boundedLetter[itemIndex2])==5):
					sum = sum + math.sqrt(math.pow(boundedLetter[itemIndex1][0]-boundedLetter[itemIndex2][0],2)+ math.pow(boundedLetter[itemIndex1][1]-boundedLetter[itemIndex2][1],2));
				else:
					sum = sum + math.sqrt(math.pow(boundedLetter[itemIndex1][0]-boundedLetter[itemIndex2][0],2)+ math.pow(boundedLetter[itemIndex1][1]-boundedLetter[itemIndex2][1],2)) + math.sqrt(math.pow(boundedLetter[itemIndex1][0]-boundedLetter[itemIndex2][2],2)+ math.pow(boundedLetter[itemIndex1][1]-boundedLetter[itemIndex2][3],2));
			else:
				if (len(boundedLetter[itemIndex2])==5):
					sum = sum + math.sqrt(math.pow(boundedLetter[itemIndex1][0]-boundedLetter[itemIndex2][0],2)+ math.pow(boundedLetter[itemIndex1][1]-boundedLetter[itemIndex2][1],2)) + math.sqrt(math.pow(boundedLetter[itemIndex1][2]-boundedLetter[itemIndex2][0],2)+ math.pow(boundedLetter[itemIndex1][3]-boundedLetter[itemIndex2][1],2));
				else:
					sum = sum + math.sqrt(math.pow(boundedLetter[itemIndex1][0]-boundedLetter[itemIndex2][0],2)+ math.pow(boundedLetter[itemIndex1][1]-boundedLetter[itemIndex2][1],2)) + math.sqrt(math.pow(boundedLetter[itemIndex1][0]-boundedLetter[itemIndex2][2],2)+ math.pow(boundedLetter[itemIndex1][1]-boundedLetter[itemIndex2][3],2))+ math.sqrt(math.pow(boundedLetter[itemIndex1][2]-boundedLetter[itemIndex2][0],2)+ math.pow(boundedLetter[itemIndex1][3]-boundedLetter[itemIndex2][1],2));
	return int(sum);

def data2TextQuadrantPointCount(boundedLetter,center,maxY):
	#check the number of points a letter has in each quadrant
	q1Count=0;
	q2Count=0;
	q3Count=0;
	q4Count=0;
	maxY += 5;

	boxHeight=20;
	boxWidth=30;
	for item in boundedLetter:
		if (len(item) == 5):
			if (item[0] >= center[0]-boxWidth/2 and item[0] < center[0] and
				item[1] >= maxY-boxHeight and item[1] < maxY-boxHeight/2): #Q1

				q1Count += 1;

			elif (item[0] >= center[0] and item[0] <= center[0]+boxWidth/2 and
				item[1] >= maxY-boxHeight and item[1] < maxY-boxHeight/2): #Q2

				q2Count += 1;

			elif (item[0] >= center[0]-boxWidth/2 and item[0] < center[0] and
				item[1] >= maxY-boxHeight/2 and item[1] <= maxY): #Q3

				q3Count += 1;

			elif (item[0] >= center[0] and item[0] <= center[0]+boxWidth/2 and
				item[1] >= maxY-boxHeight/2 and item[1] <= maxY): #Q4

				q4Count += 1;
		else:

			if (item[0] >= center[0]-boxWidth/2 and item[0] < center[0] and
				item[1] >= maxY-boxHeight and item[1] < maxY-boxHeight/2):

				q1Count += 1;

			elif (item[0] >= center[0] and item[0] <= center[0]+boxWidth/2 and
				item[1] >= maxY-boxHeight and item[1] < maxY-boxHeight/2): #Q2

				q2Count += 1;

			elif (item[0] >= center[0]-boxWidth/2 and item[0] < center[0] and
				item[1] >= maxY-boxHeight/2 and item[1] <= maxY):
				 #Q3

				q3Count += 1;

			elif (item[0] >= center[0] and item[0] <= center[0]+boxWidth/2 and
				item[1] >= maxY-boxHeight/2 and item[1] <= maxY): #Q4

				q4Count += 1;

			if (item[2] >= center[0]-boxWidth/2 and item[2] < center[0] and
				item[3] >= maxY-boxHeight and item[3] < maxY-boxHeight/2):

				q1Count += 1;

			elif (item[2] >= center[0] and item[2] <= center[0]+boxWidth/2 and
				item[3] >= maxY-boxHeight and item[3] < maxY-boxHeight/2): #Q2

				q2Count += 1;

			elif (item[2] >= center[0]-boxWidth/2 and item[2] < center[0] and
				item[3] >= maxY-boxHeight/2 and item[3] <= maxY):
				 #Q3

				q3Count += 1;

			elif (item[2] >= center[0] and item[2] <= center[0]+boxWidth/2 and
				item[3] >= maxY-boxHeight/2 and item[3] <= maxY): #Q4

				q4Count += 1;




	return [q1Count, q2Count, q3Count, q4Count]

def data2Text(boundedLetter,center,maxY):
	# this function first counts how many arcs and lines the letter is formed of and tries to make a decision on which letter is used
	# Only some letters can be distinguished by this function. these letters are 0,2,3,8,B,C,E
	#Afterwards if the letter can not be distinguished by counting the number of arcs and lines 
	# other methods are used for 5 and D the sum of distances between each point is used to distinguish.
	# For 6 and 9  whether the center of arc is below or above the center of line is checked to distinguish.
	# For A,1,F,4,7 the number of points in each quadrant of the bounding box of the letter is counted and 
	# used to distinguish the letters from each other

	arcCount = 0;
	lineCount = 0;
	for item in boundedLetter:
		if (len(item)==5):
			arcCount+=1;
		else:
			lineCount+=1;

	possibleLetters = letterLookUp[(lineCount,arcCount)];
	foundLetter = " ";
	if (len(possibleLetters)>1):

		if (possibleLetters == ['5','D']):
			dist = data2TextDistance(boundedLetter);
			if (dist > 150):
				foundLetter = 'D';
			else:
				foundLetter = '5';

		elif (possibleLetters == ['6','9']):
			#compare the line center and arc center
			arcCenterY = 0;
			lineCenterY = 0;
			for item in boundedLetter:
				if (len(item) == 5):
					arcCenterY = item[1];
				else:
					lineCenterY = (item[1] + item[3])/2;

			if (arcCenterY > lineCenterY):
				foundLetter = '6';
			else:
				foundLetter = '9';
		else:
			
			pointCount = data2TextQuadrantPointCount(boundedLetter,center,maxY);
			if (pointCount == [1,3,1,1] or pointCount == [3,1,1,1]):
				foundLetter = 'A';
			elif (pointCount == [1,2,1,2] or pointCount == [3,0,1,2] or pointCount == [3,0,2,1]
					or pointCount == [1,2,2,1]):
				foundLetter = '1';
			elif (pointCount == [3,2,1,0]):
				foundLetter = 'F';
			elif (pointCount == [3,1,0,2] or pointCount == [3,2,0,1] or pointCount == [4,1,0,1] 
					or pointCount == [4,1,1,0]):
				foundLetter = '4';
			elif (pointCount == [2,3,1,0] or pointCount == [2,3,0,1]):
				foundLetter = '7';
			else:
				print(pointCount);
				print(possibleLetters);

	else:
		foundLetter = possibleLetters;

	return foundLetter;

def getBoundedLetters(boundedData,center):

	#this function retrieves each letter from the group of letters that were obtained previously

	boxHeight = 18;
	index = 0;
	letterData = [];
	while(len(boundedData)>0):
		#find min y
		maxY = findMaxY(boundedData);
		currentLetterData = [];
		#get bounded letter
		for item in boundedData:
			if (len(item) == 5): #arc
				if (item[1]+item[2] <= maxY+5 and item[1]-item[2] <= maxY+5 and
					item[1]+item[2] >= maxY-boxHeight and item[1]-item[2] >= maxY-boxHeight):
					currentLetterData.append(item);
			else: #line
				if (item[1] <= maxY+5 and item[3] <= maxY+5 and
					item[1] >= (maxY-boxHeight) and item[3] >= (maxY-boxHeight)):
					currentLetterData.append(item);
					
		#check if current letter data has recurring stuff

		currentLetterDataNoRec = [];
		for item in currentLetterData:
			exists = False;
			for noRecItem in currentLetterDataNoRec:
				if (len(item)==5):
					if (item[0] == noRecItem[0] and 
						item[1] == noRecItem[1] and
						item[2] == noRecItem[2] and
						item[3] == noRecItem[3] and
						item[4] == noRecItem[4]):
						exists = True;
						break;
				else:
					if (item[0] == noRecItem[0] and 
						item[1] == noRecItem[1] and
						item[2] == noRecItem[2] and
						item[3] == noRecItem[3]):
						exists = True;
						break;

			if (exists is False):
				currentLetterDataNoRec.append(item);

		letterData.append(data2Text(currentLetterDataNoRec,center,maxY));

		for item in currentLetterData:
			boundedData.remove(item);

	return letterData;

def getBoundedData(organizedData,boundingBoxData,rotationDegree):

	#this function bounds and retrieves data used for letters that are at the same rotation degree around the spiral center

	boundedData = [];
	coeffLeftSide = [];
	coeffRightSide = [];
	coeffTop = [];
	coeffBottom = [];

	if (rotationDegree != 0 and rotationDegree != 90 and rotationDegree != 180 and rotationDegree != 270):
		coeffLeftSide = getLineFunctionCoeff(boundingBoxData[0][0],boundingBoxData[2][0],
											boundingBoxData[0][1],boundingBoxData[2][1]);

		coeffRightSide = getLineFunctionCoeff(boundingBoxData[1][0],boundingBoxData[3][0],
											boundingBoxData[1][1],boundingBoxData[3][1]);

		coeffTop = getLineFunctionCoeff(boundingBoxData[0][0],boundingBoxData[1][0],
											boundingBoxData[0][1],boundingBoxData[1][1]);

		coeffBottom = getLineFunctionCoeff(boundingBoxData[2][0],boundingBoxData[3][0],
											boundingBoxData[2][1],boundingBoxData[3][1]);


	for item in organizedData:
		if (len(item) == 5): #arc

			if (rotationDegree == 0): #vertical
				if (item[0]+item[2] > boundingBoxData[0][0] and
					item[0]+item[2] < boundingBoxData[1][0] and
					item[1]+item[2] < boundingBoxData[2][1] and
					item[1]+item[2] > boundingBoxData[0][1] and
					item[0]-item[2] > boundingBoxData[0][0] and
					item[0]-item[2] < boundingBoxData[1][0] and
					item[1]-item[2] < boundingBoxData[2][1] and
					item[1]-item[2] > boundingBoxData[0][1]):

					boundedData.append(item);

			elif (rotationDegree == 90):#horizontal

				if (item[0]+item[2] < boundingBoxData[0][0] and
					item[0]+item[2] > boundingBoxData[2][0] and
					item[1]+item[2] > boundingBoxData[2][1] and
					item[1]+item[2] < boundingBoxData[1][1] and
					item[0]-item[2] < boundingBoxData[0][0] and
					item[0]-item[2] > boundingBoxData[2][0] and
					item[1]-item[2] > boundingBoxData[2][1] and
					item[1]-item[2] < boundingBoxData[1][1]):

					boundedData.append(item);

			elif (rotationDegree == 180):

				if (item[0]+item[2] < boundingBoxData[0][0] and
					item[0]+item[2] > boundingBoxData[1][0] and
					item[1]+item[2] > boundingBoxData[2][1] and
					item[1]+item[2] < boundingBoxData[0][1] and
					item[0]-item[2] < boundingBoxData[0][0] and
					item[0]-item[2] > boundingBoxData[1][0] and
					item[1]-item[2] > boundingBoxData[2][1] and
					item[1]-item[2] < boundingBoxData[0][1]):

					boundedData.append(item);

			elif (rotationDegree == 270):

				if (item[0]+item[2] > boundingBoxData[0][0] and
					item[0]+item[2] < boundingBoxData[2][0] and
					item[1]+item[2] < boundingBoxData[2][1] and
					item[1]+item[2] > boundingBoxData[1][1] and
					item[0]-item[2] > boundingBoxData[0][0] and
					item[0]-item[2] < boundingBoxData[2][0] and
					item[1]-item[2] < boundingBoxData[2][1] and
					item[1]-item[2] > boundingBoxData[1][1]):

					boundedData.append(item);

			elif (rotationDegree > 0 and rotationDegree < 90):
				if (item[0]+item[2] > (item[1]+item[2]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0]+item[2] <  (item[1]+item[2]-coeffRightSide[0])/coeffRightSide[1] and
					item[0]+item[2] <  (item[1]+item[2]-coeffTop[0])/coeffTop[1] and
					item[0]+item[2] >  (item[1]+item[2]-coeffBottom[0])/coeffBottom[1] and
					item[0]-item[2] > (item[1]-item[2]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0]-item[2] <  (item[1]-item[2]-coeffRightSide[0])/coeffRightSide[1] and
					item[0]-item[2] <  (item[1]-item[2]-coeffTop[0])/coeffTop[1] and
					item[0]-item[2] >  (item[1]-item[2]-coeffBottom[0])/coeffBottom[1] and
					item[1]+item[2] > coeffLeftSide[0] + coeffLeftSide[1]*(item[0]+item[2]) and
					item[1]+item[2] < coeffRightSide[0] + coeffRightSide[1]*(item[0]+item[2]) and
					item[1]+item[2] > coeffTop[0] + coeffTop[1]*(item[0]+item[2]) and
					item[1]+item[2] < coeffBottom[0] + coeffBottom[1]*(item[0]+item[2]) and
					item[1]-item[2] > coeffLeftSide[0] + coeffLeftSide[1]*(item[0]-item[2]) and
					item[1]-item[2] < coeffRightSide[0] + coeffRightSide[1]*(item[0]-item[2]) and
					item[1]-item[2] > coeffTop[0] + coeffTop[1]*(item[0]-item[2]) and
					item[1]-item[2] < coeffBottom[0] + coeffBottom[1]*(item[0]-item[2])):

					boundedData.append(item);

			elif (rotationDegree > 90 and rotationDegree < 180):
				if (item[0]+item[2] < (item[1]+item[2]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0]+item[2] >  (item[1]+item[2]-coeffRightSide[0])/coeffRightSide[1] and
					item[0]+item[2] <  (item[1]+item[2]-coeffTop[0])/coeffTop[1] and
					item[0]+item[2] >  (item[1]+item[2]-coeffBottom[0])/coeffBottom[1] and
					item[0]-item[2] < (item[1]-item[2]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0]-item[2] >  (item[1]-item[2]-coeffRightSide[0])/coeffRightSide[1] and
					item[0]-item[2] <  (item[1]-item[2]-coeffTop[0])/coeffTop[1] and
					item[0]-item[2] >  (item[1]-item[2]-coeffBottom[0])/coeffBottom[1] and
					item[1]+item[2] > coeffLeftSide[0] + coeffLeftSide[1]*(item[0]+item[2]) and
					item[1]+item[2] < coeffRightSide[0] + coeffRightSide[1]*(item[0]+item[2]) and
					item[1]+item[2] < coeffTop[0] + coeffTop[1]*(item[0]+item[2]) and
					item[1]+item[2] > coeffBottom[0] + coeffBottom[1]*(item[0]+item[2]) and
					item[1]-item[2] > coeffLeftSide[0] + coeffLeftSide[1]*(item[0]-item[2]) and
					item[1]-item[2] < coeffRightSide[0] + coeffRightSide[1]*(item[0]-item[2]) and
					item[1]-item[2] < coeffTop[0] + coeffTop[1]*(item[0]-item[2]) and
					item[1]-item[2] > coeffBottom[0] + coeffBottom[1]*(item[0]-item[2])):

					boundedData.append(item);


			elif (rotationDegree > 180 and rotationDegree < 270):
				if (item[0]+item[2] < (item[1]+item[2]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0]+item[2] >  (item[1]+item[2]-coeffRightSide[0])/coeffRightSide[1] and
					item[0]+item[2] >  (item[1]+item[2]-coeffTop[0])/coeffTop[1] and
					item[0]+item[2] <  (item[1]+item[2]-coeffBottom[0])/coeffBottom[1] and
					item[0]-item[2] < (item[1]-item[2]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0]-item[2] >  (item[1]-item[2]-coeffRightSide[0])/coeffRightSide[1] and
					item[0]-item[2] >  (item[1]-item[2]-coeffTop[0])/coeffTop[1] and
					item[0]-item[2] <  (item[1]-item[2]-coeffBottom[0])/coeffBottom[1] and
					item[1]+item[2] < coeffLeftSide[0] + coeffLeftSide[1]*(item[0]+item[2]) and
					item[1]+item[2] > coeffRightSide[0] + coeffRightSide[1]*(item[0]+item[2]) and
					item[1]+item[2] < coeffTop[0] + coeffTop[1]*(item[0]+item[2]) and
					item[1]+item[2] > coeffBottom[0] + coeffBottom[1]*(item[0]+item[2]) and
					item[1]-item[2] < coeffLeftSide[0] + coeffLeftSide[1]*(item[0]-item[2]) and
					item[1]-item[2] > coeffRightSide[0] + coeffRightSide[1]*(item[0]-item[2]) and
					item[1]-item[2] < coeffTop[0] + coeffTop[1]*(item[0]-item[2]) and
					item[1]-item[2] > coeffBottom[0] + coeffBottom[1]*(item[0]-item[2])):

					boundedData.append(item);

			elif (rotationDegree > 270 and rotationDegree < 360):
				if (item[0]+item[2] > (item[1]+item[2]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0]+item[2] <  (item[1]+item[2]-coeffRightSide[0])/coeffRightSide[1] and
					item[0]+item[2] >  (item[1]+item[2]-coeffTop[0])/coeffTop[1] and
					item[0]+item[2] <  (item[1]+item[2]-coeffBottom[0])/coeffBottom[1] and
					item[0]-item[2] > (item[1]-item[2]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0]-item[2] <  (item[1]-item[2]-coeffRightSide[0])/coeffRightSide[1] and
					item[0]-item[2] >  (item[1]-item[2]-coeffTop[0])/coeffTop[1] and
					item[0]-item[2] <  (item[1]-item[2]-coeffBottom[0])/coeffBottom[1] and
					item[1]+item[2] < coeffLeftSide[0] + coeffLeftSide[1]*(item[0]+item[2]) and
					item[1]+item[2] > coeffRightSide[0] + coeffRightSide[1]*(item[0]+item[2]) and
					item[1]+item[2] > coeffTop[0] + coeffTop[1]*(item[0]+item[2]) and
					item[1]+item[2] < coeffBottom[0] + coeffBottom[1]*(item[0]+item[2]) and
					item[1]-item[2] < coeffLeftSide[0] + coeffLeftSide[1]*(item[0]-item[2]) and
					item[1]-item[2] > coeffRightSide[0] + coeffRightSide[1]*(item[0]-item[2]) and
					item[1]-item[2] > coeffTop[0] + coeffTop[1]*(item[0]-item[2]) and
					item[1]-item[2] < coeffBottom[0] + coeffBottom[1]*(item[0]-item[2])):

					boundedData.append(item);

		else: #line

			if (rotationDegree == 0): #vertical
				if (item[0] > boundingBoxData[0][0] and
					item[0] < boundingBoxData[1][0] and
					item[1] < boundingBoxData[2][1] and
					item[1] > boundingBoxData[0][1] and
					item[2] > boundingBoxData[0][0] and
					item[2] < boundingBoxData[1][0] and
					item[3] < boundingBoxData[2][1] and
					item[3] > boundingBoxData[0][1]):

					boundedData.append(item);

			elif (rotationDegree == 90):#horizontal

				if (item[0] < boundingBoxData[0][0] and
					item[0] > boundingBoxData[2][0] and
					item[1] > boundingBoxData[2][1] and
					item[1] < boundingBoxData[1][1] and
					item[2] < boundingBoxData[0][0] and
					item[2] > boundingBoxData[2][0] and
					item[3] > boundingBoxData[2][1] and
					item[3] < boundingBoxData[1][1]):

					boundedData.append(item);

			elif (rotationDegree == 180):

				if (item[0] < boundingBoxData[0][0] and
					item[0] > boundingBoxData[1][0] and
					item[1] > boundingBoxData[2][1] and
					item[1] < boundingBoxData[0][1] and
					item[2] < boundingBoxData[0][0] and
					item[2] > boundingBoxData[1][0] and
					item[3] > boundingBoxData[2][1] and
					item[3] < boundingBoxData[0][1]):

					boundedData.append(item);

			elif (rotationDegree == 270):

				if (item[0] > boundingBoxData[0][0] and
					item[0] < boundingBoxData[2][0] and
					item[1] < boundingBoxData[2][1] and
					item[1] > boundingBoxData[1][1] and
					item[2] > boundingBoxData[0][0] and
					item[2] < boundingBoxData[2][0] and
					item[3] < boundingBoxData[2][1] and
					item[3] > boundingBoxData[1][1]):

					boundedData.append(item);

			elif (rotationDegree > 0 and rotationDegree < 90):

				if (item[0] > (item[1]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0] <  (item[1]-coeffRightSide[0])/coeffRightSide[1] and
					item[0] <  (item[1]-coeffTop[0])/coeffTop[1] and
					item[0] >  (item[1]-coeffBottom[0])/coeffBottom[1] and
					item[2] > (item[3]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[2] <  (item[3]-coeffRightSide[0])/coeffRightSide[1] and
					item[2] <  (item[3]-coeffTop[0])/coeffTop[1] and
					item[2] >  (item[3]-coeffBottom[0])/coeffBottom[1] and
					item[1] > coeffLeftSide[0] + coeffLeftSide[1]*item[0] and
					item[1] < coeffRightSide[0] + coeffRightSide[1]*item[0] and
					item[1] > coeffTop[0] + coeffTop[1]*item[0] and
					item[1] < coeffBottom[0] + coeffBottom[1]*item[0] and
					item[3] > coeffLeftSide[0] + coeffLeftSide[1]*item[2] and
					item[3] < coeffRightSide[0] + coeffRightSide[1]*item[2] and
					item[3] > coeffTop[0] + coeffTop[1]*item[2] and
					item[3] < coeffBottom[0] + coeffBottom[1]*item[2]):

					boundedData.append(item);

			elif (rotationDegree > 90 and rotationDegree < 180):

				if (item[0] < (item[1]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0] >  (item[1]-coeffRightSide[0])/coeffRightSide[1] and
					item[0] <  (item[1]-coeffTop[0])/coeffTop[1] and
					item[0] >  (item[1]-coeffBottom[0])/coeffBottom[1] and
					item[2] < (item[3]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[2] >  (item[3]-coeffRightSide[0])/coeffRightSide[1] and
					item[2] <  (item[3]-coeffTop[0])/coeffTop[1] and
					item[2] >  (item[3]-coeffBottom[0])/coeffBottom[1] and
					item[1] > coeffLeftSide[0] + coeffLeftSide[1]*item[0] and
					item[1] < coeffRightSide[0] + coeffRightSide[1]*item[0] and
					item[1] < coeffTop[0] + coeffTop[1]*item[0] and
					item[1] > coeffBottom[0] + coeffBottom[1]*item[0] and
					item[3] > coeffLeftSide[0] + coeffLeftSide[1]*item[2] and
					item[3] < coeffRightSide[0] + coeffRightSide[1]*item[2] and
					item[3] < coeffTop[0] + coeffTop[1]*item[2] and
					item[3] > coeffBottom[0] + coeffBottom[1]*item[2]):

					boundedData.append(item);

			elif (rotationDegree > 180 and rotationDegree < 270):

				if (item[0] < (item[1]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0] >  (item[1]-coeffRightSide[0])/coeffRightSide[1] and
					item[0] >  (item[1]-coeffTop[0])/coeffTop[1] and
					item[0] <  (item[1]-coeffBottom[0])/coeffBottom[1] and
					item[2] < (item[3]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[2] >  (item[3]-coeffRightSide[0])/coeffRightSide[1] and
					item[2] >  (item[3]-coeffTop[0])/coeffTop[1] and
					item[2] <  (item[3]-coeffBottom[0])/coeffBottom[1] and
					item[1] < coeffLeftSide[0] + coeffLeftSide[1]*item[0] and
					item[1] > coeffRightSide[0] + coeffRightSide[1]*item[0] and
					item[1] < coeffTop[0] + coeffTop[1]*item[0] and
					item[1] > coeffBottom[0] + coeffBottom[1]*item[0] and
					item[3] < coeffLeftSide[0] + coeffLeftSide[1]*item[2] and
					item[3] > coeffRightSide[0] + coeffRightSide[1]*item[2] and
					item[3] < coeffTop[0] + coeffTop[1]*item[2] and
					item[3] > coeffBottom[0] + coeffBottom[1]*item[2]):

					boundedData.append(item);

			elif (rotationDegree > 270 and rotationDegree < 360):

				if (item[0] > (item[1]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[0] <  (item[1]-coeffRightSide[0])/coeffRightSide[1] and
					item[0] >  (item[1]-coeffTop[0])/coeffTop[1] and
					item[0] <  (item[1]-coeffBottom[0])/coeffBottom[1] and
					item[2] > (item[3]-coeffLeftSide[0])/coeffLeftSide[1] and 
					item[2] <  (item[3]-coeffRightSide[0])/coeffRightSide[1] and
					item[2] >  (item[3]-coeffTop[0])/coeffTop[1] and
					item[2] <  (item[3]-coeffBottom[0])/coeffBottom[1] and
					item[1] < coeffLeftSide[0] + coeffLeftSide[1]*item[0] and
					item[1] > coeffRightSide[0] + coeffRightSide[1]*item[0] and
					item[1] > coeffTop[0] + coeffTop[1]*item[0] and
					item[1] < coeffBottom[0] + coeffBottom[1]*item[0] and
					item[3] < coeffLeftSide[0] + coeffLeftSide[1]*item[2] and
					item[3] > coeffRightSide[0] + coeffRightSide[1]*item[2] and
					item[3] > coeffTop[0] + coeffTop[1]*item[2] and
					item[3] < coeffBottom[0] + coeffBottom[1]*item[2]):

					boundedData.append(item);


	return boundedData;

def processData(organizedData):
	print("processing data");

	finalTextArray = [None]*253;
	#find min max points of the spiral
	minMax = findMinMax(organizedData);
	maxX = minMax[0];
	minX = minMax[1];
	maxY = minMax[2];
	minY = minMax[3];
	# find the center of the spiral
	center = findCenter(maxX,minX,maxY,minY);
	#get bounding box
	boundingBoxData = getBoundingBoxData(center,minY,24); 
	translatedBoundingBoxData = translateBoundingBox(center,boundingBoxData);
	rotationDegree = 0;
	while (rotationDegree < 360):
		#rotate
		rotatedData = rotateBoundingBox(rotationDegree,translatedBoundingBoxData);
		#reverse translate
		reversedData = reverseTranslateBoundingBox(center,rotatedData);
		#process the bounded letters
		boundedData = getBoundedData(organizedData,reversedData,rotationDegree);
		#translate bounded data according to center
		translatedBoundedData = translateBoundedData(center,boundedData);
		#rotate bounded data to vertical position 0 degrees
		rotatedBoundedData = rotateBoundedData(-1*rotationDegree,translatedBoundedData);
		#reverse translate 
		reversedBoundedData = reverseTranlateBoundedData(center,rotatedBoundedData);
		#process the letters
		letters = getBoundedLetters(reversedBoundedData,center);

		for letterIndex in xrange(0,len(letters)):

			finalTextArray[int(rotationDegree/10)+letterIndex*36] = letters[letterIndex];

		rotationDegree += 10;

	return finalTextArray;

def downloadData():
	#login
	HTS.loginUserInput();
	#start mission
	HTS.getPage("https://www.hackthissite.org/missions/prog/6/");
	#get url 
	print("downloading data");
	response = HTS.getPage("https://www.hackthissite.org/missions/prog/6/image");
	#parse content and get the data
	# we have to mine the code starting with new Array(...);
	javascriptCode = response.content;
	mineStartIndex = javascriptCode.find("new Array(");
	mineEndIndex = javascriptCode.find(");",mineStartIndex);
	data = javascriptCode[mineStartIndex + 10:mineEndIndex]
	return data;

def sendSolution(solution):
	print("sending solution");
	payload = {'solution' : solution, 'submitbutton' : 'submit'};
	response = HTS.postPage("https://www.hackthissite.org/missions/prog/6/index.php",payload);
	print("solution response: \n");
	print(response.content);

data = downloadData();
print(data);
#organize the data
print("organizing data");
organizedData = organizeData(data);
#process the data -> groups of 4
solutionText = ''.join(processData(organizedData));
print("image analyzed and text found:")
print(solutionText);
sendSolution(solutionText);
