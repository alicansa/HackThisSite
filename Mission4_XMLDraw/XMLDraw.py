#	The solution to the programming mission 4 where you have to parse an xml file that 
#	defines specifications to draw lines and arcs and draw this image which
#	contains a text.  
#
#	To use this module requests and xmltodict must be installed. 	
#	> pip install requests 
#	> pip install xmltodict
#
#
#	Author : Alican Salor
#	date : 27.08.2015

import HackThisSiteInterface as HTS 
import xmltodict
import bz2
from PIL import Image, ImageDraw


def sendResponse(solution):
	print("sending solution")
	payload = {'solution' : solution, 'submitbutton' : 'submit'};
	return HTS.postPage("https://www.hackthissite.org/missions/prog/4/index.php",payload);


def parseXML(xmlContent):

	#hashmap for colors 
	colors = {
		'yellow' : '#ffff00',
		'blue' : '#0000ff',
		'green' : '#00ff00',
		'red' : '#ff0000',
		'white' : '#ffffff'
	}


	#parse the xml file
	xmlDict = xmltodict.parse(xmlContent);
	width = 1000;
	height = 1000;
	
	img = Image.new('RGB', (width, height));
	draw = ImageDraw.Draw(img);

	#root is ppcPlot 
	#first parse the lines and draw those lines
	#the trick here is to tranform the axis used by python to cartesian axis

	for item in xmlDict['ppcPlot']['Line']:
		if(item.has_key("Color")):
			draw.line((float(item['XStart']),height-float(item['YStart']),float(item['XEnd']),height-float(item['YEnd'])),fill=colors[item['Color']]);
		else:
			draw.line((float(item['XStart']),height-float(item['YStart']),float(item['XEnd']),height-float(item['YEnd'])),fill=colors['white']);
	
	#then parse the arcs
	#the trick here is to again cartesian axis tranformation and furthermore transform the angle from clockwise
	#counterclockwise

	for item in xmlDict['ppcPlot']['Arc']:
		if(item.has_key("Color")):
			draw.arc((float(item['XCenter'])-float(item['Radius']),
					height-(float(item['YCenter'])+float(item['Radius'])),
					float(item['XCenter'])+float(item['Radius']),
					height-(float(item['YCenter'])-float(item['Radius']))
				),
				-1*(int(item['ArcStart']) + int(item['ArcExtend'])),-1*int(item['ArcStart']),fill=colors[item['Color']]);
		else:
			draw.arc((float(item['XCenter'])-float(item['Radius']),
					height-(float(item['YCenter'])+float(item['Radius'])),
					float(item['XCenter'])+float(item['Radius']),
					height-(float(item['YCenter'])-float(item['Radius']))	
				),
				-1*(int(item['ArcStart']) + int(item['ArcExtend'])),-1*int(item['ArcStart']),fill=colors['white']);


	del draw
	img.show();
	solution = raw_input("blue,green,red,yellow,white: ");
	return sendResponse(solution);

def downloadXML():
	#login to the site
	HTS.loginUserInput();
	#start the mission
	HTS.getPage("https://www.hackthissite.org/missions/prog/4/");
	#get the xml 
	response = HTS.getPage("https://www.hackthissite.org/missions/prog/4/XML");
	#uncompress downloaded content
	xmlContent = bz2.decompress(response.content);

	return xmlContent;

print(parseXML(downloadXML()));



