# This is the verbal comparison paradigm for ExpyVR
# Use the makeImages.py script to prepare stimuli for the paradigm
import xlrd;
from re import search;
from random import shuffle;
import xml.dom.minidom, math, operator;
from itertools import permutations;

self.imagesI=None;
self.itrial=0;

if self.controller.gModuleList.has_key('ImagesListInstructions'): 
	self.imagesI = self.controller.gModuleList['ImagesListInstructions'];
	
self.ifilename = self.imagesI.initConf['files'][:-5]+'ions.xlsx';#opens instruction.xlsx;ifilename=instructions filename
x=xlrd.open_workbook(self.ifilename);
xsheet=x.sheets()[0];

self.sex = {'U': 0, 'M': 1, 'F': 2};#sex
self.dom = {'prsn': 0, 'spac': 1, 'time': 2};#domain
self.task = {'ace': 0, 'dst': 1, 'sem': 2, 'lex': 3};#task

self.inst_arrey=[[[[[] for b in range(5)] for t in range(4)] for d in range(3)]for s in range(3)];

r=1;#row (in instruction.xlsx)
while len(str(xsheet.cell_value(r,0))) != 0:
	s=str(xsheet.cell_value(r,2));#sex
	d=str(xsheet.cell_value(r,3));#domain
	t=str(xsheet.cell_value(r,4));#type
	b=int(xsheet.cell_value(r,5));#block
	i=int(xsheet.cell_value(r,0));#index
	self.inst_arrey[self.sex[s]][self.dom[d]][self.task[t]][b]=i;
	r=r+1; 
	
#getting the subjects sex stimuli_quest for sex apropreate instructions
self.sourse = self.imagesI.initConf['files'][:-26]+'stimuli_quest.xlsx';#opens stimuli_quest
x=xlrd.open_workbook(self.sourse);
xsheet=x.sheets()[0];
self.s_sex=xsheet.cell_value(3,1);#subjects sex


print '--------------------';
print 'ok inst_init';
print '--------------------';
