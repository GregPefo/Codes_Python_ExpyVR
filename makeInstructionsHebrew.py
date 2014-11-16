# -*- coding: utf-8 -*-

# This script takes a list of words and creates the stimuli file (to be used in expyVR), the images and the questionnaires
# To make this work, you have to download the PIL library here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil
#                                   and the xlrd library here: http://pypi.python.org/pypi/xlrd

import xlrd, xlwt, os, Image, ImageFont, ImageDraw, time, calendar;
from random import shuffle;
from datetime import datetime, timedelta;

def makeInstructions(filename):
#pre-required definition to make images
#image and font specifications
	font="Arial";
	fontsize=50;
	sizepic=(500,350);
	f = ImageFont.truetype(font+".ttf", fontsize, encoding="UTF-8");# create a font object
# this function receives a name of an excel file (instructions), reads the instructions into inst_arrey
	x=xlrd.open_workbook(filename); # x gets data of workbook
	xsheet=x.sheets()[0];
	[CurPath,filen]=os.path.split(filename); # splits full path into 2. the tail is the file name
	CurPrefix=filen[:-9]; # cuts 'ions.xls'
#deleting existing stimuli with the same name
	l=len(CurPrefix);
	files=os.listdir(CurPath); #The method listdir() returns a list containing the names of the entries in the directory given by path. 
	for i in files:
		if (i[:l]==CurPrefix and i[-3:]=='jpg'):
			os.remove(os.path.join(CurPath, i));
#creates a dictionary to translate dimensions of the matrix to its categories
	sex={'U': 0,'M': 1,'F': 2};
	dom={'prsn': 0, 'spac': 1, 'time': 2};#domain
	task={'ace': 0, 'dst': 1, 'sem': 2, 'lex': 3};#type of task
#creating address lists for the names of different parameters
	inst_arrey=[[[[[] for b in range(5)] for t in range(4)] for d in range(3)]for s in range(3)];
	r=1;
	while len(str(xsheet.cell_value(r,0))) != 0:
		s=str(xsheet.cell_value(r,2));#sex
		d=str(xsheet.cell_value(r,3));#domain
		t=str(xsheet.cell_value(r,4));#task
		b=int(xsheet.cell_value(r,5));#block
		q=xsheet.cell_value(r,1);#question
		i=xsheet.cell_value(r,0);
		#print sex[s],dom[d],task[t];
		inst_arrey[sex[s]][dom[d]][task[t]][b].extend(q);
		r=r+1; 
#saving each stimulus as a separate picture
#this part checks if we need multiple lines for the text
		cur_inst=inst_arrey[sex[s]][dom[d]][task[t]][b];
		w = u''.join(cur_inst);
		w=w.rsplit(' ');
		current_line=0;
		lines=[w[0]];
		for current_word_num in range(1,len(w)):
			if f.getsize(lines[current_line]+' '+w[current_word_num])[0]<=sizepic[0]:#f.getsize(string) returns the string's length in this font and size
				lines[current_line]=lines[current_line]+' '+w[current_word_num];
			else:
				current_line=current_line+1;
				lines.append(w[current_word_num]);
		num_lines=len(lines);

#saving each image
		im = Image.new("RGB", sizepic);              # create an image
		dr = ImageDraw.Draw(im);                      # create an object for drawing inside the image
		for j in range(num_lines):
			if any(ord(char) >= 220 for char in cur_inst):
				lines[j]=lines[j][::-1];                    # reverse the order of hebrew strings
				for letter in range(len(lines[j])-1):
					if (lines[j][letter] in ['0','1','2','3','4','5','6','7','8','9']):
						if (lines[j][letter+1] in ['0','1','2','3','4','5','6','7','8','9']):
							l1=lines[j][letter]; l2=lines[j][letter+1]; 
							lines[j]=lines[j].replace(l1,u'ttttt'); lines[j]=lines[j].replace(l2,l1); lines[j]=lines[j].replace(u'ttttt',l2);     # reverse numbers again
			posX = (sizepic[0]-f.getsize(lines[j])[0])/2;#find the middle position of the picture
			posY = (sizepic[1]-f.getsize(unicode(cur_inst))[1]*num_lines)/2+f.getsize(lines[j])[1]*j;                   
			dr.text((posX,posY), lines[j], font=f);#enter text into the ImageDraw object
		im.save(open(CurPath+'\\'+CurPrefix+str(int(i))+".jpg", "wb"), "JPEG");  
	return;



