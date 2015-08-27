#	The solution to the programming mission 5 where you have to recover a corrupted .bz2 file   
#	Decompress it and obtain the password drawn on the image.
#
#	we need to get rid of 0d0a couples -> \r \n
#	\n are translated to \r \n in windows so we don't know which \r \n should be in the file
#	we have to brute force and try every combination. 
#	Yet when the file is analysed it can be seen there there is more than enough 0d0a couples and since 
#	there are 2^n (where n is the number of 0d0a couples) combinations, we have to consider a smarter brute force
#	algorithm.
#	The algorithm I've implemented, obtains combinations with specified group size. These addresses in these combinations
# 	are then altered from 0d0a to 0a. A useful technique is also starting from the largest group size and then decreasing
#	the size of the groups. 
#	Another feature I considered was to use a distance threshold where we take groups 0d0a couples which 
#	have a distance between each other greater than the threshold as \n isn't such a common character. However 
#	I didn't need to use this feature.
#
#
#
#	To use this module requests and xmltodict must be installed. 	
#	> pip install requests 
#
#
#	Author : Alican Salor
#	date : 27.09.2015


import HackThisSiteInterface as HTS 
import bz2
import binascii
import sys
import math
from PIL import Image
from StringIO import StringIO

processedBranches = 0;

def corruptFile(originalContent):
	#for testing 

	content = binascii.hexlify(bz2.compress(originalContent));
	address = content.find('0a',0);
	while(address >= 0):
		
		#change 
		if (content[address-2:address] != "0d" and (address % 2) == 0):
			print address;
			content = content[0:address] + "0d" + content[address:len(content)];

		#find next
		address = content.find('0a',address+4);


	return content;

def groupAddressesRecursive(addresses,allGroups,groupAddress,currentIndex,groupSize,distanceThreshold):
	#obtain all combinations with specified group size of the given addresses

	if ((groupAddress is not None and len(groupAddress) >= groupSize) or currentIndex >= len(addresses) or len(addresses)-currentIndex+len(groupAddress) < groupSize):
		return groupAddress;

  	else:
  		#nothing added
  		groupAddressesRecursive(addresses,allGroups,groupAddress,currentIndex+1,groupSize,distanceThreshold);
  		#address added
  		changedGroupAddress = [];
		changedGroupAddress = groupAddress + [addresses[currentIndex]];
		distance = abs(int(changedGroupAddress[len(changedGroupAddress)-1])-int(changedGroupAddress[len(changedGroupAddress)-2]));
		if  (len(changedGroupAddress) >= 2 and distance >= distanceThreshold):
			if (len(changedGroupAddress) >= groupSize):
				allGroups.append(changedGroupAddress);
			
			groupAddressesRecursive(addresses,allGroups,changedGroupAddress,currentIndex+1,groupSize,distanceThreshold);
		elif (len(changedGroupAddress) < 2):
			groupAddressesRecursive(addresses,allGroups,changedGroupAddress,currentIndex+1,groupSize,distanceThreshold);

  		return allGroups;



def getCorruptedByteAddresses(content):
	#get the starting index of all 0d0a pairs
	addresses = [];
	address = content.find('0d0a',0);
	while(address >= 0):
		addresses.append(address);
		address = content.find('0d0a',address+4);

	print addresses;
	return addresses;


def updateAddresses(addresses,updatedAddress):

	newAddresses = [];
	for address in addresses:
		if (address > updatedAddress):
			address = address - 2;

		newAddresses.append(address);

	return newAddresses;

#recursively construct the tree and check if crc holds
def recoverAllCombinations(addresses,currentAddress,data):

	# obtains all 2^n combinations and check if the the file is recovered. As anticipated 
	# this function won't be able to brute-force the solution under the time limit which is
	# 10 minutes
	#

	global processedBranches;
	
	if (currentAddress >= len(addresses)):
		processedBranches += 1;

		
		try:
  			dec = bz2.decompress(binascii.unhexlify(data));
  			print('\nrecovered @ recover.png\n');
  			pngRecFile = open('recover.png','wb');
  			pngRecFile.write(dec);
  			solution = raw_input("password: ");
			print("sending solution")
			payload = {'solution' : solution, 'submitbutton' : 'submit'};
			HTS.postPage("https://www.hackthissite.org/missions/prog/5/index.php",payload);

  			sys.exit(0);

		except IOError:
			return;

  	else:
  		constructTreeRecursive(addresses,currentAddress+1,data); #unchanged
  		#update the addresses
  		newData = data[0:addresses[currentAddress]]+data[addresses[currentAddress]+2:len(data)];
  		addresses = updateAddresses(addresses,addresses[currentAddress]);
  		constructTreeRecursive(addresses,currentAddress+1,newData); #changed
  		

def recoverGrouped(addresses,data):
	#change the given addresses -> 0d0a to 0a
	newData = "";
	lastIndex=0
	for index in xrange(0,len(addresses)):

		newData = newData + data[lastIndex:addresses[index]]+data[addresses[index]+2:addresses[index]+4];
		lastIndex = addresses[index]+4;


	newData = newData + data[lastIndex:len(data)];

	# bz2.decompress does the cyclic redundancy check first and throws an exception if the file 
	# doesn't pass the check. If it does pass the check then we have recovered the file
	try:
		dec = bz2.decompress(binascii.unhexlify(newData));
		print('\nRecovered the file. Check recovered.png and enter the password\n');
		pngRecFile = open('recovered.png','wb');
		pngRecFile.write(dec);
		pngRecFile.close();
		solution = raw_input("password: ");
		print("sending solution")
		payload = {'solution' : solution, 'submitbutton' : 'submit'};
		HTS.postPage("https://www.hackthissite.org/missions/prog/5/index.php",payload);

		sys.exit(0);

	except IOError:
		return;

def downloadFile():
	#login to the site
	HTS.loginUserInput();
	#start the mission
	HTS.getPage("https://www.hackthissite.org/missions/prog/5/");
	#get the compressed file
	print("downloading file...");
	response = HTS.getPage("https://www.hackthissite.org/missions/prog/5/corrupted.png.bz2");
	print("file downloaded..");
	return response;


response = downloadFile();
hexData = binascii.hexlify(response.content);
print("getting corrupted bytes");
addresses = getCorruptedByteAddresses(hexData);
print("starting recovering file");
for i in xrange(1,len(addresses)):
	print("\ngroups of " + str(len(addresses)-i));
	grouped = groupAddressesRecursive(addresses,[],[],0,len(addresses)-i,0);
	for itemIndex in xrange(0,len(grouped)):
		sys.stdout.write('\r{0}%'.format(float(100*itemIndex/len(grouped))));
		sys.stdout.flush();
		processedBranches = 0;
		recoverGrouped(grouped[itemIndex],hexData);




