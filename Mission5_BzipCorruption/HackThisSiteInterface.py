#	a simple interface to login and send get and post request to hackthissite.org
#
#	To use this module requests must be installed. 	
#	> pip install requests 
#
#
#	Author : Alican Salor
#	date : 26.09.2015

import requests
import json

cookies = {};

def loginUserInput():

	global cookies;
	username = raw_input("username:");
	password = raw_input("password:");

	session = requests.session();
	headers = {"Referer" : "https://www.hackthissite.org/" , "Accept-Encoding" : "gzip,deflate"};
	payload = {"btn_submit" : "Login","password" : password, "username" : username};

	response = session.post("https://www.hackthissite.org/user/login",data=payload,headers=headers);
	cookies = requests.utils.dict_from_cookiejar(session.cookies);
	if (response.status_code == 200):
		if (cookies == {}):
			print("not authenticated");
		else:
			print("authenticated");
			return response;
	else:
		print("something went wrong (code: " + str(response.status_code) + ")");


def login(username,password):
	#function logs user in hackthissite

	global cookies;

	session = requests.session();
	headers = {"Referer" : "https://www.hackthissite.org/" , "Accept-Encoding" : "gzip,deflate"};
	payload = {"btn_submit" : "Login","password" : password, "username" : username};

	response = session.post("https://www.hackthissite.org/user/login",data=payload,headers=headers);
	cookies = requests.utils.dict_from_cookiejar(session.cookies);
	if (response.status_code == 200):
		if (cookies == {}):
			print("not authenticated");
		else:
			print("authenticated");
			return response;
	else:
		print("something went wrong (code: " + str(response.status_code) + ")");

def getPage(url):
	#get request sent to the website. its important that the user logs in the site first

	global cookies;

	headers = {"Referer" : "https://www.hackthissite.org/" , "Accept-Encoding" : "gzip,deflate"};
	response = requests.get(url,headers=headers,cookies=cookies);

	if (response.status_code == 200):
		return response;
	else:
		print("something went wrong (code: " + str(response.status_code) + ")");

def postPage(url,payload):
	#post request sent to the website. its important that the user logs in the site first

	global cookies;

	headers = {"Referer" : "https://www.hackthissite.org/" , "Accept-Encoding" : "gzip,deflate"};
	response = requests.post(url,headers=headers,cookies=cookies,data=payload);

	if (response.status_code == 200):
		return response;
	else:
		print("something went wrong (code: " + str(response.status_code) + ")");