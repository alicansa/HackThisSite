import HackThisSiteInterface as HTS


def downloadData():
	#login
	HTS.login("alicansa","06rjp71CAR45SER4KJL2K");
	#start mission
	HTS.getPage("https://www.hackthissite.org/missions/prog/6/");
	#get url 
	response = HTS.getPage("https://www.hackthissite.org/missions/prog/6/image");
	#parse content and get the data
	print(response.content);


downloadData();