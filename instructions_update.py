if self.starting:# this ensures that the following code is run in the beginning of this cycle and not in every frame
    #if self.controller._currentCondition!=self.curCond:# if beginning a routine after another ended - changing condition
        #self.counter=0;
        #self.num_appearances=[0]*self.imagesL.totalNumImages;# creates of 0 with "totalNumImages" number of cells
        #self.condIndex=self.conds.index(self.controller._currentCondition);
    self.curCond=self.controller._currentCondition;
    if self.curCond != 'default':
        s=self.sex[self.s_sex];#subjects sex
        d=self.curCond[0:4];
        t=self.curCond[5:8];
        b=self.curCond[9:10];
        if d=='spac' and t=='ace':
            inst_index=int(self.inst_arrey[s][1][0][int(b)]);#M or F instruction
        else:
            inst_index=int(self.inst_arrey[0][self.dom[d]][self.task[t]][int(b)]);#unisex instruction
        self.itrial=self.itrial+1;
        self.imagesI.index=inst_index;
        self.inst_csv=inst_index;
        print self.inst_csv;
    print '--------------------';
    print 'ok inst_update';
    print '--------------------';