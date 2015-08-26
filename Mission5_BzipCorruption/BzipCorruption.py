import HackThisSiteInterface as HTS 
import bz2
import binascii
import sys
import itertools
import math
from PIL import Image
from StringIO import StringIO


#we need to get rid of 0d0a couples -> \r \n
#\n are translated to \r \n in windows so we don't know which \r \n should be in the file
#we have to brute force and try every combination -> use a tree structure

processedBranches = 0;

def corruptFile(originalContent):


	content = binascii.hexlify(bz2.compress(originalContent));
	# print(bz2.decompress(binascii.unhexlify(content)));

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

	if ((groupAddress is not None and len(groupAddress) >= groupSize) or currentIndex >= len(addresses) or len(addresses)-currentIndex+len(groupAddress) < groupSize):
		# print(groupAddress);
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
def constructTreeRecursive(addresses,currentAddress,data):
	global processedBranches;
	#if end of file check crc and return
	
	if (currentAddress >= len(addresses)):
		processedBranches += 1;

		
		try:
  			dec = bz2.decompress(binascii.unhexlify(data));
  			print('\nrecovered\n');
  			pngRecFile = open('test_rec.png','wb');
  			pngRecFile.write(dec);


  			sys.exit(0);

		except IOError:
			return;

  	else:
  		# print("go left");
  		constructTreeRecursive(addresses,currentAddress+1,data); #unchanged
  		# print("go right");
  		#update the addresses
  		newData = data[0:addresses[currentAddress]]+data[addresses[currentAddress]+2:len(data)];
  		addresses = updateAddresses(addresses,addresses[currentAddress]);
  		constructTreeRecursive(addresses,currentAddress+1,newData); #changed
  		

def recover(addresses,data):
	#change the given addresses -> 0d0a to 0a
	newData = "";
	lastIndex=0
	for index in xrange(0,len(addresses)):

		newData = newData + data[lastIndex:addresses[index]]+data[addresses[index]+2:addresses[index]+4];
		lastIndex = addresses[index]+4;


	newData = newData + data[lastIndex:len(data)];

	try:
		dec = bz2.decompress(binascii.unhexlify(newData));
		print('\nrecovered\n');
		pngRecFile = open('recovered.png','wb');
		pngRecFile.write(dec);
		pngRecFile.close();
		# image = Image.open('recovered.png');
		# image.show();
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

# omitAddresses([4,12],"12130d0a12350d0a12");

# f = open('test.png','r');
# content = f.read();
# hexData = corruptFile(content);
response = downloadFile();
hexData = binascii.hexlify(response.content);


print("getting corrupted bytes");
addresses = getCorruptedByteAddresses(hexData);
# constructTreeRecursive(addresses,0,hexData);
print("starting recovering file");
for i in xrange(1,len(addresses)):
	print("\ngroups of " + str(len(addresses)-i));
	grouped = groupAddressesRecursive(addresses,[],[],0,len(addresses)-i,0);
	for itemIndex in xrange(0,len(grouped)):
		sys.stdout.write('\r{0}%'.format(float(100*itemIndex/len(grouped))));
		sys.stdout.flush();
		processedBranches = 0;
		recover(grouped[itemIndex],hexData);




