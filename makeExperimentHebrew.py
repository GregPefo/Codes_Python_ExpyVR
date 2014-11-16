# -*- coding: utf-8 -*-

# This script takes a list of words and creates the stimuli file (to be used in expyVR), the images and the questionnaires
# To make this work, you have to download the PIL library here: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil
#                                   and the xlrd library here: http://pypi.python.org/pypi/xlrd

import xlrd, xlwt, os, Image, ImageFont, ImageDraw, time, calendar;
from random import shuffle;
from datetime import datetime, timedelta;

def makeExperiment(filename):
    # this function receives a name of an excel file (stim_quest), reads the stimuli, chooses according to groups and makes a stimulus file out of them 
    
    [CurPath,filen]=os.path.split(filename); # splits full path into 2. the tail is the file name
    CurPrefix=filen[:-4]; # cuts the suffix 
    x=xlrd.open_workbook(filename); # x gets data of workbook
    xsheet=x.sheets()[0]; 
    #creating address lists for the names of different parameters
    dom=[];#domain
    cat=[];#category
    tru=[];#true/false
    sco=[];#score
    dom.extend('prsn spac time'.split());
    cat=[['f_name','l_name','occup','dad','mom','people'],['country','city','neighbor','hospit','floor'],['year','season','month','date','day','event']];#categories
    #cat=[['fnm','lnm','job','dad','mom','ppl'],['sta','cit','nei','hos','flr'],['yer','ssn','mnt','dat','day','evn']];#categories
    tru.extend('tr fl'.split());
    sco.extend('0 1 2 3 4 5 6 7 8 9 10 11 12'.split());#distance that include months
    sem_dic=[{'LD': 0, 'AC': 1},{'RL': 0,'AR': 1},{'WR': 0, 'TC': 1}];#semantic  dictionary
    sem_evnt_dic={'NWR': 0, 'NTC': 1};
    sem_rdic=[{0: 'LD',1: 'AC'},{0: 'RL',1: 'AR'},{0: 'WR',1: 'TC'}];#semantic reverse dictionary
    # reading the comprehended stimuli(marked 1) from the Excel file into lists
    stim_list=[[[[[] for s in range(13)] for t in range (2)] for c in range(6)] for d in range(3)];#we use the month's numeric value as score - that is why we use 13 for s - and we have 6 catgories in the temporal domain
    sem_list=[[[] for q in range(2)] for d in range(3)];#semantic control
    sem_evnt_cmp=[[],[]];# comparable events: the comparison between stimuli semantic control has to be clear so we are marking stimuli as NTC or NWR 
    prsn_quest=[]; #for person questionnaire
    spac_quest=[]; #for place questionnaire
    time_quest=[]; #for time questionnaire
    i=0; #index that is re-started and re-used
    r=1; #starting row
    st=0;#st is column number holding stimuli
    sc=1;#sc is column number holding score
    kn=2;#id is column number holding identification(0/1)
#parameters used to mark semantic control stimuli
    sq=0;#semantic question
    sm=3;#column 3 stores semantic referees
    nt=4#column marking stimuli as NTC=(not technology related)
    nw=5#column marking stimuli as NWR=(not war related)
#appending personal details to stim_list[0]
    while r<7:
        if r==3:
            sex=xsheet.cell_value(3,sc);
        else:
            stim_list[0][i][0][0].append(xsheet.cell_value(r,sc))# stim_list[0][i][0][0]:0-first name,1-last name,2-occupation, 3-father's name, 4-mother's name, 5-people
            i=i+1;
        r=r+1;
    r=r+2;#skiping a row carrying headline(excel row 7-8)
#appending spatial stimuli to stim_list[1]: 0-country, 1-city, 2-neighbourhood, 3-hospital;, 4-floor
    i=0;#re-starting i;
    stim_list[1][i][0][int(xsheet.cell_value(r,sc))].append(xsheet.cell_value(r,st));#getting 'ישראל' into stim_list[1][0][0][1]                                             
    r=r+1;
    while r<71:            
        if xsheet.cell_value(r,kn)==1:
            if r in (30, 54, 66):#the row numbers where we switch categories (country to city etc.)
                i=i+1;
                stim_list[1][i][0][int(xsheet.cell_value(r,sc))].append(xsheet.cell_value(r,st));                                       
            else:
                stim_list[1][i][1][int(xsheet.cell_value(r,sc))].append(xsheet.cell_value(r,st));#'xsheet.cell_value(r,sc)' represents the score
            if xsheet.cell_value(r,sm)=='AR'or xsheet.cell_value(r,sm)=='RL':
                sq=sem_dic[1][xsheet.cell_value(r,sm)];
                sem_list[1][sq].append(xsheet.cell_value(r,st));
            r=r+1;
    stim_list[1][4][0][0]=[u'\u05E7\u05D5\u05DE\u05D4'+' 1-'];#true floor;  stim_list[][][][0] means no score
    for f in range (8):
        stim_list[1][4][1][0].append(u'\u05E7\u05D5\u05DE\u05D4'+' '+str(f));
    r=r+2;#skipping a row carrying headline(excel row 71-72)
    
#appending temporal stimuli into stim_list[2]: 0-year, 1-season, 2-month, 3-date, 4-week day, 5-events.
#appending events to stim_list[2][4][1]
#appending semantic control into 
    while r<101:
        if xsheet.cell_value(r,kn)==1:
            stim_list[2][5][1][int(xsheet.cell_value(r,sc))].append(xsheet.cell_value(r,st));#events are appended into stim_list[2][5][1]; stim_list[2][4][1] is weekday
            if xsheet.cell_value(r,sm)=='WR' or xsheet.cell_value(r,sm)=='TC':
                sq=sem_dic[2][xsheet.cell_value(r,sm)];
                sem_list[2][sq].append(xsheet.cell_value(r,st));
            if xsheet.cell_value(r,nw)=='NWR':
                sem_evnt_cmp[sem_evnt_dic[xsheet.cell_value(r,nw)]].append(xsheet.cell_value(r,st));
            if xsheet.cell_value(r,nt)=='NTC':
                sem_evnt_cmp[sem_evnt_dic[xsheet.cell_value(r,nt)]].append(xsheet.cell_value(r,st));
        r=r+1;
    r=r+2;#skipping a row carrying headline(excel row 113-114)
#appending people stimuli to stim_list[0][0][1]
    while r<128:
       print xsheet.cell_value(r,sc);
       stim_list[0][5][1][int(xsheet.cell_value(r,sc))].append(xsheet.cell_value(r,st));
       if xsheet.cell_value(r,sm)=='LD' or xsheet.cell_value(r,sm)=='AC':
            sq=sem_dic[0][xsheet.cell_value(r,sm)];
            sem_list[0][sq].append(xsheet.cell_value(r,st)); 
       r=r+1;
#appending year to stim_list[2][0][0]     
    stim_list[2][0][0][0]=[time.strftime("%Y")];
    stim_list[2][0][1][0]=range(1980,2015);
#appending the season
#switching the source file
    datafile=os.path.join(CurPath,'stimuli_data.xlsx');
#loading stimuli_data.xlsx into xsheet
    x=xlrd.open_workbook(datafile);
    xsheet=x.sheets()[0];
    s=0;#season index
    doy=int(time.strftime("%j"));#day of year
    su = "21062013";#summer
    au = "21092013";#autumn
    wi = "21122013";#winter
    sp = "21042013";#spring                               
    su_doy = datetime(int(su[4:8]),int(su[2:4]),int(su[0:2]));
    au_doy = datetime(int(au[4:8]),int(au[2:4]),int(au[0:2]));
    wi_doy = datetime(int(wi[4:8]),int(wi[2:4]),int(wi[0:2]));
    sp_doy = datetime(int(sp[4:8]),int(sp[2:4]),int(sp[0:2]));
    su=int(su_doy.strftime("%j"));
    au=int(au_doy.strftime("%j"));
    wi=int(wi_doy.strftime("%j"));
    sp=int(sp_doy.strftime("%j"));
    if doy in range(su,au):
        s=1;
    elif doy in range(au,wi):
        s=2;
    elif doy in range(wi,sp):    
        s=3;
    elif doy in range(sp,su):
        s=4;
    r=1;
    while r<5:
        if xsheet.cell_value(r,5)==s:
            stim_list[2][1][0][int(xsheet.cell_value(r,5))]=[xsheet.cell_value(r,4)];#notice we appended to num of season as score
        elif xsheet.cell_value(r,5)!=s:
            stim_list[2][1][1][int(xsheet.cell_value(r,5))].append(xsheet.cell_value(r,4));
        r=r+1;
#appending month
    r=1;
    while r<13:
        if xsheet.cell_value(r,3)==time.strftime("%m"):
            stim_list[2][2][0][int(xsheet.cell_value(r,3))]=[xsheet.cell_value(r,2)];
        elif xsheet.cell_value(r,3)!=time.strftime("%m"):   
            stim_list[2][2][1][int(xsheet.cell_value(r,3))].append(xsheet.cell_value(r,2));
        r=r+1;
#appending day of month
    stim_list[2][3][0][0]=[int(time.strftime("%d"))];
    dim=calendar.monthrange(int(time.strftime("%Y")), int(time.strftime("%m")));#dim:day in month
    temp=range(dim[1]);#dim gets two values and we need only the 1st(day in month)
    stim_list[2][3][1][0]=[x+1 for x in temp];#turning range from 0,1,2... to 1,2,3...
    stim_list[2][3][1][0].remove(int(time.strftime("%d")));#removes current day from list
#appending weekday
    r=1;
    while r<8:
        if xsheet.cell_value(r,8)==time.strftime("%a"):
            stim_list[2][4][0][int(xsheet.cell_value(r,7))]=[xsheet.cell_value(r,6)];#the day number is represented in distance
        elif xsheet.cell_value(r,3)!=time.strftime("%m"):   
            stim_list[2][4][1][int(xsheet.cell_value(r,7))].append(xsheet.cell_value(r,6));
        r=r+1;
#appending additional person stimuli from stimuli_data
#appending false first and last names
    for i in range(2):
        r=1;
        while r<11:   
            if xsheet.cell_value(r,i) != stim_list[0][i][0][0]:
                stim_list[0][i][1][0].append(xsheet.cell_value(r,i));
            r=r+1;
#appending false occupations:
    i=0;
    r=1;
    if sex==xsheet.cell_value(0,9):
        i=9;
    elif sex==xsheet.cell_value(0,10):
        i=10;
    while r<11:
        if xsheet.cell_value(r,i) != stim_list[0][2][0][0]:
             stim_list[0][2][1][0].append(xsheet.cell_value(r,i));
        r=r+1;
#all data to stim_list appended
#writing data from stim list into stimuli.xls
    a=[['index'],['stimulus'],['doamin'],['category'],['true'],['distance'],['semantic'],['NWR'],['NTC']]; 
    print a[8];
    counter=0;
    for d in range(3):
        for c in range(6):
            for t in range(len(stim_list[d][c])):
                for s in range(len(stim_list[d][c][t])):
                    for i in range(len(stim_list[d][c][t][s])):
                        a[0].append(counter);
                        a[1].append(stim_list[d][c][t][s][i]); 
                        a[2].append(dom[d]);
                        a[3].append(cat[d][c]);
                        a[4].append(tru[t]);
                        a[5].append(sco[s]);
                        a[6].append(0);
                        a[7].append(0);
                        a[8].append(0);
                        for q in range(2):#adding tags relevant for semantic control
                            for j in range(len(sem_list[d][q])):
                                if a[1][counter]==sem_list[d][q][j]:
                                    a[6][counter]=sem_rdic[d][q]+str(j);
                            for z in range(len(sem_evnt_cmp[0])):#NWR list
                                if a[1][counter]==sem_evnt_cmp[0][z]:
                                    a[7][counter]='NWR';
                            for w in range(len(sem_evnt_cmp[1])):#NTC list
                                if a[1][counter]==sem_evnt_cmp[1][w]:
                                    a[8][counter]='NTC';
                        if cat[d][c]=='people':
                            prsn_quest.append([counter,stim_list[d][c][t][s][i]]);
                            #print prsn_quest;
                        elif dom[d]=='spac':
                            spac_quest.append([counter,stim_list[d][c][t][s][i]]);
                        elif cat[d][c]=='event':
                            time_quest.append([counter,stim_list[d][c][t][s][i]]);
                        counter=counter+1;
    wbk = xlwt.Workbook();
    sheet = wbk.add_sheet('sheet 1');
    for q in range(9):
        for i in range(len(a[q])):
            sheet.write(i,q,a[q][i]);        
    wbk.save(CurPath+'\\stimuli.xls');
	
    # writing the space questionnaire
    header=[u'index', u'\u05de\u05e7\u05d5\u05dd', u'\u05e8\u05d2\u05e9 \u05dc\u05de\u05e7\u05d5\u05dd (1-10)', u'\u05d4\u05d9\u05d9\u05ea\u05d9 \u05d1\u05de\u05e7\u05d5\u05dd (1\\0)', u'\u05db\u05de\u05d4 \u05e4\u05e2\u05de\u05d9\u05dd \u05d4\u05d9\u05d9\u05ea\u05d9', u'\u05d9\u05d5\u05d3\u05e2 \u05dc\u05d4\u05d2\u05d9\u05e2 \u05dc\u05de\u05e7\u05d5\u05dd (1\\0)'];
    wbk = xlwt.Workbook();
    sheet = wbk.add_sheet('sheet 1');
    for i in range(len(header)):
        sheet.write(0,i,header[i]); # adding the header
    for i in range(len(spac_quest)):
        #print spac_quest[i][0];
        #print spac_quest[i][1];
        sheet.write(i+1,0,spac_quest[i][0]);
        sheet.write(i+1,1,spac_quest[i][1]);
    wbk.save(CurPath+'\\space_questionnaire.xls');
    
    # writing the time questionnaire
    header=[u'index', u'\u05d0\u05d9\u05e8\u05d5\u05e2', u'\u05e8\u05d2\u05e9 \u05dc\u05d0\u05d9\u05e8\u05d5\u05e2 (1-10)', u'\u05e2\u05d1\u05e8\\\u05e2\u05ea\u05d9\u05d3 (1-\\1)', u'\u05d2\u05d9\u05dc \u05d1\u05d6\u05de\u05df \u05d4\u05d0\u05d9\u05e8\u05d5\u05e2'];
    wbk = xlwt.Workbook();
    sheet = wbk.add_sheet('sheet 1');
    for i in range(len(header)):
        sheet.write(0,i,header[i]);
    for i in range(len(time_quest)):
        sheet.write(i+1,0,time_quest[i][0]);
        sheet.write(i+1,1,time_quest[i][1]);
    wbk.save(CurPath+'\\time_questionnaire.xls');
    
    # writing the person questionnaire
    header=[u'index', u'\u05d0\u05d3\u05dd', u'\u05e8\u05d2\u05e9 \u05dc\u05d0\u05d3\u05dd (1-10)', u'\u05de\u05db\u05d9\u05e8 \u05d0\u05ea \u05d4\u05d0\u05d3\u05dd \u05d0\u05d9\u05e9\u05d9\u05ea (0\\1)', u'\u05e1\u05d5\u05d2 \u05e7\u05e8\u05d1\u05d4 (\u05de\u05e9\u05e4\u05d7\u05d4\\\u05d7\u05d1\u05e8\\\u05de\u05db\u05e8\\\u05e1\u05dc\u05d1\u05e8\u05d9\u05d8\u05d9)'];
    wbk = xlwt.Workbook();
    sheet = wbk.add_sheet('sheet 1');
    for i in range(len(header)):
        sheet.write(0,i,header[i]);
    for i in range(len(prsn_quest)):
        sheet.write(i+1,0,prsn_quest[i][0]);
        sheet.write(i+1,1,prsn_quest[i][1]);
    wbk.save(CurPath+'\\person_questionnaire.xls');
	
#making the images
#converting all stimuli to str
    for i in range(len(a[1])):
        if a[1][i] in range(-3,2016):
            a[1][i]=str(a[1][i]);          
        i=i+1;
        
    wordlist=a[1][1:]; 
#image and font specifications
    font="Arial";
    fontsize=50;
    sizepic=(350,350);
    f = ImageFont.truetype(font+".ttf", fontsize, encoding="UTF-8");          # create a font object   
#deleting existing stimuli with the same name
    CurPrefix='stimuli';
    l=len(CurPrefix);
    files=os.listdir(CurPath); #The method listdir() returns a list containing the names of the entries in the directory given by path. 
    for i in files:
        if (i[:l]==CurPrefix and i[-3:]=='jpg'):
            os.remove(os.path.join(CurPath, i))
    
#saving each stimulus as a separate picture
    for i in range(len(wordlist)):
#this part checks if we need multiple lines for the text
        w=wordlist[i].rsplit(' ');
        current_line=0;
        lines=[w[0]];
        for current_word_num in range(1,len(w)):
            if f.getsize(lines[current_line]+' '+w[current_word_num])[0]<=sizepic[0]:       # f.getsize(string) returns the string's length in this font and size
                lines[current_line]=lines[current_line]+' '+w[current_word_num];
            else:
                current_line=current_line+1;
                lines.append(w[current_word_num]);
        num_lines=len(lines);
        
#saving each image    
        im = Image.new("RGB", sizepic);              # create an image
        d = ImageDraw.Draw(im);                      # create an object for drawing inside the image
        for j in range(num_lines):
            if any(ord(char) >= 220 for char in wordlist[i]):
                lines[j]=lines[j][::-1];                    # reverse the order of hebrew strings
                for letter in range(len(lines[j])-1):
                    if (lines[j][letter] in ['0','1','2','3','4','5','6','7','8','9']):
                        if (lines[j][letter+1] in ['0','1','2','3','4','5','6','7','8','9']):
                            l1=lines[j][letter]; l2=lines[j][letter+1]; 
                            lines[j]=lines[j].replace(l1,u'ttttt'); lines[j]=lines[j].replace(l2,l1); lines[j]=lines[j].replace(u'ttttt',l2);     # reverse numbers again
            posX = (sizepic[0]-f.getsize(lines[j])[0])/2;                       # find the middle position of the picture
            posY = (sizepic[1] - f.getsize(wordlist[i])[1]*num_lines)/2+f.getsize(lines[j])[1]*j;                   
            d.text((posX,posY), lines[j], font=f);                              # enter text into the ImageDraw object
        im.save(open(CurPath+'\\'+CurPrefix+str(i)+".jpg", "wb"), "JPEG");  
    return;

    

