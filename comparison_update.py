if self.starting:# this ensures that the following code is run in the beginning of this cycle and not in every frame
    #if self.controller._currentCondition!=self.curCond:# if beginning a routine after another ended - changing condition
        #self.counter=0;
        #self.num_appearances=[0]*self.imagesL.totalNumImages;# creates of 0 with "totalNumImages" number of cells
        #self.condIndex=self.conds.index(self.controller._currentCondition);
    self.curCond=self.controller._currentCondition;
    if self.curCond != 'default':
        d=int(self.dom[self.curCond[0:4]]);
        t=int(self.task[self.curCond[5:8]]);
        b=int(self.curCond[9:10]);
        if t==2:#semantic comparison
            tSBC=self.SBC[d][b];
            i=self.premut_index[d][t][b][tSBC];
            self.imagesL.index = self.premut_lists[d][t][b][tSBC][i][0];
            self.imagesR.index = self.premut_lists[d][t][b][tSBC][i][1];
            self.premut_index[d][t][b][tSBC]=self.premut_index[d][t][b][tSBC]+1;
#since we have only two options, self.SBC[d][b] can be only 1 or 0
            if self.SBC[d][b]==0:
                self.SBC[d][b]=1;
            elif self.SBC[d][b]==1:
                self.SBC[d][b]=0;
        else:
            i=self.premut_index[d][t][b];
            self.premut_index[d][t][b] = self.premut_index[d][t][b]+1;#progressing the counter
            self.imagesL.index = self.premut_lists[d][t][b][i][0];
            self.imagesR.index = self.premut_lists[d][t][b][i][1];
        #print '--------------';
        #print '[d][t][b][i]';
        #print d,t,b,i;
        #print '--------------';
        print self.inst_csv;
        self.csvLogger.writerow([str("%d"%self.trial), str("%0.4f"%self.controller.gLogger._gTimeManager.absoluteTime()), str("%d"%self.imagesR.index), str("%d"%self.imagesL.index), str("%d"%self.inst_csv)]);
        self.trial=self.trial+1;
        print '--------------------';
        print 'ok comp_update';
        print '--------------------';
		
