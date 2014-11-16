# This is the verbal comparison paradigm for ExpyVR
# Use the makeImages.py script to prepare stimuli for the paradigm

from re import search;
from random import shuffle;
import xml.dom.minidom, xlrd, math, operator;
from itertools import permutations;

#('___') is a way to refer to specific properties of the components - you can reach some of them using rclick + edit on different components
self.imagesL=None; self.imagesR=None; #the following code makes sure all the components exist
if self.controller.gModuleList.has_key('ImagesListLeft'): 
    self.imagesL = self.controller.gModuleList['ImagesListLeft'];
if self.controller.gModuleList.has_key('ImagesListRight'):
    self.imagesR = self.controller.gModuleList['ImagesListRight'];
if self.controller.gModuleList.has_key('keyboard'):
    self.keyboard = self.controller.gModuleList['keyboard'];
if self.imagesL.initConf['files']!=self.imagesR.initConf['files']:# making sure the right image list file is the same as the left one
    raise NameError('Right image list file is different from the left!');
self.filename = self.imagesL.initConf['files'][:-5]+'.xls';#cuts 5 letters from the end (in this case "*.jpg") and adds .xls
#opens stimuli.xls which contains [index, stimuli, domain, category, tof, distance] 
x=xlrd.open_workbook(self.filename);
xsheet=x.sheets()[0];

#Create a CSV(comma-separated values) logger object saving to the default logger path for this experiment
self.csvLogger = csv.writer(open(os.path.join(self.controller.gLogger.Path, datetime.today().strftime('%y%m%d%H%M%S_') + 'output.csv') , 'w'), lineterminator = '\n');
#csv.writer creates a csv file. open is the preferable way to open files. open requires (full path, mode). mode is w(write) - meaning the file is created if it doesnt exist
#the result is (for example): "140424170811_output.csv" in log directory of ExpyVR
#Write the first (title / header) row to the output CSV file. 
self.csvLogger.writerow(['trial', 'absTime', 'indexR', 'indexL', 'instructions', 'Semantic orientation', self.filename]);

self.curCond=self.controller._currentCondition;
self.inst_csv=1;
self.trial=0;#trial counter

#creating the list we will be using:
self.stim_array=[[[[[] for s in range(13)] for t in range (2)] for c in range(6)] for d in range(3)];#s-score, t-tof, c-category, d-domain;
self.premut_lists=[[[[] for b in range(5)] for t in range(4)] for d in range(3)];#stores all relevant permutation from stim_array
self.premut_index=[[[0 for b in range(5)] for t in range(4)] for d in range(3)];#used as counter matrix that stores the number of times a pair from a specific self.premut_lists[d][s] has been picked
self.sem_altblock=[[[[] for a in range(2)] for q in range(2)]  for d in range (3)];#semantic alternative block: we want to switch the semantic stimuli (SN0&SN2 etc.) between the two repetitions in every block
self.premut_temp=[];#a list that will carry the distance comparison permutations
sem_temp=[[],[]];#a list that will carry the semantic control permutations
self.SBC=[[0 for q in range(2)] for d in range(3)];#semantic block counter: intended to check if the repartition of semantic control block is the 1st or 2nd

#creating dictionaries in order to append stimuli into a [domain][category][tof][score] matrix with ease
self.dom = {'prsn': 0, 'spac': 1, 'time': 2};#domain
self.cat = [{'f_name': 0,'l_name': 1,'occup': 2,'dad': 3,'mom': 4,'people': 5},{'country': 0,'city': 1,'neighbor': 2,'hospit': 3,'floor': 4},{'year': 0,'season': 1,'month': 2,'date': 3,'day': 4,'event': 5}];
self.tof = {'tr': 0, 'fl': 1};#tof - true or false
self.task = {'ace': 0, 'dst': 1, 'sem': 2, 'lex': 3};#type
self.sem_dic=[{'LD': 0, 'AC': 1},{'AR': 0,'RL': 1},{'WR': 0, 'TC': 1}];#semantic dictionary (LD-leader,AC-actor,RL-religious, AR-Arab, WR-war, TC-technology)
self.stime_dic={0: 'NWR', 1: 'NTC'};

#appending index number of stimuli into appropriate cells in self.stim_array
for i in range(self.imagesL.totalNumImages): #self.imagesL.totalNumImages = the number of stimuli in stimuli.xls
    d=self.dom[xsheet.cell_value(i+1,2)];#domain self.stim_array; i+1 because row 0 caries headline
    c=self.cat[d][xsheet.cell_value(i+1,3)];#category
    t=self.tof[xsheet.cell_value(i+1,4)];#true/false
    s=int(xsheet.cell_value(i+1,5));#score
    self.stim_array[d][c][t][s].append(int(xsheet.cell_value(i+1,0)));#getting the index into self.stim_array[d][c][t][s]
    self.stim_array[1][5][1][s] = self.stim_array[1][1][1][s];#duplicating the city stimuli into self.stim_array[1][5][0][s]
    self.stim_array[0][3][1][s] = self.stim_array[0][5][1][s];#duplicating people stimuli to dad(fl)
    self.stim_array[0][4][1][s] = self.stim_array[0][5][1][s];#duplicating people stimuli to mom(fl)
#appending index numbers of semantic control stimuli directly into the relevant self.premut_lists[d][2][b]
    if xsheet.cell_value(i+1,6) !=0:#if the stimuli is semantic control
        sq=self.sem_dic[d][xsheet.cell_value(i+1,6)[0:2]];#sq uses semantic  dictionary to get the block number (0/1) 
        sa=int(xsheet.cell_value(i+1,6)[2:3]);#sa gets the '0' from 'WR0'
        self.sem_altblock[d][sq][sa]=[int(xsheet.cell_value(i+1,0))];
        self.premut_lists[d][2][sq]= self.sem_altblock[d][sq];#we don"t use "append" because we are only reading the first element
        #print d,sq;
        #print  self.sem_altblock[d][sq];
        self.premut_index[d][2][sq]=[0,0];
    #print d,c,t,s,len(self.stim_array[d][c][t][s]);
    
#appending stimuli index into  self.premut_lists 
for d in range(3):#domain
#appending ACE stimuli in all domains
    for b in range(5):#b refers to both block(in premut_lists) and cat(in stim_array); cat(5) is used in the orientation task so we are not reading it.
        self.premut_temp=[];
        for t in range(2):#tof
            for s in range(13):#score
                for e in range(len(self.stim_array[d][b][t][s])):#element in list
                    if self.stim_array[d][b][t][s] != []:
                        self.premut_lists[d][0][b].append(self.stim_array[d][b][t][s][e]);#premut_lists[d][0][b] stores ace tasks across stimuli
                        #print d,b,self.premut_lists[d][0][b];
        for i in range(len(self.premut_lists[d][0][b])):#setting the permutation(the function permutation inst useful);
            if self.premut_lists[d][0][b][0] != self.premut_lists[d][0][b][i]:
                self.premut_temp.append([self.premut_lists[d][0][b][0],self.premut_lists[d][0][b][i]]);#creating permutation of true stimuli(self.premut_lists[d][0][b][0]) with others
                shuffle(self.premut_temp[i-1]);
            shuffle(self.premut_temp);
        self.premut_lists[d][0][b]=self.premut_temp;
        for k in range(b):#shuffling self.premut_lists[d][1][b] a different num of time for each block to create diversity between blocks
            shuffle(self.premut_lists[d][0][b]);
        #if d==2:
            #print d,b,len(self.premut_lists[d][0][b]);
            #print b,self.premut_lists[d][0][b];
        
#appending distance comparison permutation in all domains. the distance between each pair>1
#appending permutation for semantic control
        self.premut_temp=[];
        for s in range(13):#score
            for e in range(len(self.stim_array[d][5][1][s])):#cat(5) in every domain store the stimuli used for the dist_compairison task
                if self.stim_array[d][5][1][s] !=[]:#so that we wouldn't append empty cells
                    self.premut_lists[d][1][b].append(self.stim_array[d][5][1][s][e]);
                    if b in range(2):#spending stimuli for semantic control permutations; semantic control in every domain has only 2 blocks
                        if self.stim_array[d][5][1][s][e] != self.premut_lists[d][2][b][0][0] and self.stim_array[d][5][1][s][e] != self.premut_lists[d][2][b][1][0]:#preventing the possibility of pairing semantic control stimuli with itself or with the other semantic control
                            if self.stim_array[d][5][1][s][e] !=[]:
                                if d==2:
                                    cur_r=self.stim_array[d][5][1][s][e]+1;#the row number in stimuli.xls is the index number (which is also the stimuli itself)+1
                                    clmn=7+b;#the NWR and NTC stimuli are in rows 7 and 8
                                    print self.stime_dic[b];
                                    if xsheet.cell_value(cur_r,clmn)==self.stime_dic[b]:#in the time domain we need to make sure the stimuli are NWR or NTC
                                        self.premut_lists[d][2][b][0].append(self.stim_array[d][5][1][s][e]);
                                        self.premut_lists[d][2][b][1].append(self.stim_array[d][5][1][s][e]);
                                else:
                                    self.premut_lists[d][2][b][0].append(self.stim_array[d][5][1][s][e]);
                                    self.premut_lists[d][2][b][1].append(self.stim_array[d][5][1][s][e]);

#shuffling and selecting permutation with score difference>1 for distance comparison task
        for k in range (b):#shuffling self.premut_lists[d][1][b] a different num of time for each block to creates diversity between blocks
            shuffle(self.premut_lists[d][1][b]);
        self.premut_temp=list(permutations(self.premut_lists[d][1][b],2));
        self.premut_lists[d][1][b]=[];
        shuffle(self.premut_temp); shuffle(self.premut_temp); shuffle(self.premut_temp);
        for p in range(len(self.premut_temp)):
            r0=int(self.premut_temp[p][0])+1;#row in stimuli.xls of the element stored in temp_list[p][0] = the index number (the element itself)+1;
            r1=int(self.premut_temp[p][1])+1;
            s_d=int(math.fabs(operator.__sub__(int(xsheet.cell_value(r0,5)),int(xsheet.cell_value(r1,5)))));#sufficient distance
            if s_d > 1:#checking if the difference in scores of the pair>1
                self.premut_lists[d][1][b].append(self.premut_temp[p]);
#appending lexical control  in all domains.
            if b in range(2):
                l_d=int(math.fabs(operator.__sub__(len(xsheet.cell_value(r0,1)),len(xsheet.cell_value(r1,1)))));#len distance
                if l_d>2:
                    self.premut_lists[d][3][0].append(self.premut_temp[p]);
                    self.premut_lists[d][3][1].append(self.premut_temp[p]);
                shuffle( self.premut_lists[d][3][1]);shuffle( self.premut_lists[d][3][1]);
                shuffle( self.premut_lists[d][3][0]);shuffle( self.premut_lists[d][3][0]);shuffle( self.premut_lists[d][3][0]);
        #if d==2: print self.premut_lists[d][3][0];
        #if d==2: print b, self.premut_lists[d][1][b];
#creating the semantic permutations:
        if b in range(2):
            for i in range(len(self.premut_lists[d][2][b][0])-1):#len(self.premut_lists[d][2][b][0])=len(self.premut_lists[d][2][b][1])
                sem_temp[0].append([self.premut_lists[d][2][b][0][0],self.premut_lists[d][2][b][0][i+1]]);
                sem_temp[1].append([self.premut_lists[d][2][b][1][0],self.premut_lists[d][2][b][1][i+1]]);
                shuffle(sem_temp[0][i]);shuffle(sem_temp[1][i]);shuffle(sem_temp[1][i]);
            shuffle(sem_temp[0]);shuffle(sem_temp[0]);
            shuffle(sem_temp[1]);shuffle(sem_temp[1]);shuffle(sem_temp[1]);
            #print'----------------------------------------';
            #print d,b;
            #print sem_temp[0];
            #print'----------------------------------------';
            #print sem_temp[1];
            #print'----------------------------------------';
            self.premut_lists[d][2][b][0]=sem_temp[0];
            self.premut_lists[d][2][b][1]=sem_temp[1];
            #if d==2:
                #print '0',self.premut_lists[d][2][b][0];
                #print '1',self.premut_lists[d][2][b][1];
            sem_temp=[[],[]];

print '--------------------';
print 'ok comp_init';
print '--------------------';

