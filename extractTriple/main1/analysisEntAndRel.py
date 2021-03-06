# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 09:18:36 2016

@author: DELL
"""
import codecs
import sys
sys.path.append('../utils')
#from getFreebaseType import FreebaseAPI
#from deleteEntStopWords import deleteEntStopW
from filterFreebaseFoodType import TypeDict

class proSeedTriple():
    def __init__(self,f_name,f_entHasName):
        self.f_name = f_name
        self.f_entHasName = f_entHasName
    
    def analyEnt(self,ent_name_type):
        ents = {}
        f_name = self.f_name
        with codecs.open(f_name,'r','utf-8') as file:
            for line in file:
                line = line.strip()
                items = line.split('\t')
                if len(items)==6:
                    ent = items[6]
                    if ents.get(ent)==None:
                        ents[ent] = ent_name_type[ent]
                        print ent
                else:
                    if len(items)==10:
                        ent1 = items[7]
                        ent2 = items[9]
                        #print ent1
                        #print ent2
                        if ents.get(ent1)==None:
                            if ent_name_type.get(ent1) != None:
                                ents[ent1] = ent_name_type[ent1]
                            else:
                                ents[ent1] = 'NIL'
                        if ents.get(ent2)==None:
                           if ent_name_type.get(ent2) != None:
                                ents[ent2] = ent_name_type[ent2]
                           else:
                                ents[ent2] = 'NIL'
                        #print ents
        return ents
    
    def analyRel(self):
        f_name = self.f_name
        #key is the relation, the value is the context which the relation is merged
        rels = {}
        rel2Num= {}
        with open(f_name,'r') as file:
            for line in file:
                #print 'line',line
                line = line.strip()
                items = line.split('\t')
                if len(items)==10:
                    ContextNo = items[0]
                    ent1 = items[7]
                    ent2 = items[9]
                    if int(ContextNo)==None:
                        print int(ContextNo)
                    rel = items[2].strip()
                    if rel =='staring':
                        print rel
                    sentence = items[5]
                    strs =ContextNo+'\t'+sentence+'\t'+ent1+'\t'+ent2
                    if rels.get(rel) ==None:
                        rel2Num[rel] = 1
                        rels[rel] = {strs}
                    else:
                        temps = rels[rel]
                        temps.add(strs) 
                        rels[rel] = temps
                        rel2Num[rel] +=1                      
        return rels,rel2Num
        
    def analyEntContext(self):
        f_name = self.f_name
        #key is the entity, the value is the context which the entity is merged
        ents = {}
        with codecs.open(f_name,'r','utf-8') as file:
            for line in file:
                #print 'line',line
                line = line.strip()
                items = line.split('\t')
                if len(items)==10:
                    ContextNo = items[0]
                    ent1 = items[7]
                    ent2 = items[9]
                    if int(ContextNo)==None:
                        print int(ContextNo)
                    rel = items[2]
                    sentence = items[5]
                    #head entity
                    strs1 =ContextNo+'\t'+sentence+'\t'+rel+'\t'+'t_'+ent2
                    if ents.get(ent1) ==None:
                        ents[ent1] = {strs1}
                    else:
                        temps = ents[ent1]
                        temps.add(strs1) 
                        ents[ent1] = temps 
                    #end entity
                    strs2 =ContextNo+'\t'+sentence+'\t'+'r_'+rel+'\t'+'h_'+ent1
                    if ents.get(ent2) ==None:
                        ents[ent2] = {strs2}
                    else:
                        temps = ents[ent2]
                        temps.add(strs2) 
                        ents[ent2] = temps 
        return ents
        
    def getentNameType(self):
        f_entHasName = self.f_entHasName
        ent_name_type = {}
        with codecs.open(f_entHasName,'r','utf-8') as file:
            for line in file:
                line = line.strip()
                items = line.split('\t')
                #pid = items[0]
                #a little different from the previous context
                name = items[0]
                types = ''
                for i in range(1,len(items)):
                    types = types + items[i] + '\t'
                types = types.strip()
                ent_name_type[name] = types
        return ent_name_type
        
if __name__=="__main__":
    if len(sys.argv) !=3:
        print 'usage: python pyfile dir_path domain'
        exit(1)
    dir_path = sys.argv[1]
    domain = sys.argv[2]
    f_name =dir_path+'ftri.txt'
    f_entHasName = dir_path+domain+'_enthasName_type.txt_new'
    
    pro = proSeedTriple(f_name,f_entHasName)
    ent_name_type = pro.getentNameType()
    
    ents = pro.analyEnt(ent_name_type)
    if domain == 'nyt':
        t=['/location/location', '/people/person', '/organization/organization']
    if domain == 'yelp':
        t=['/location/location', '/food/food', '/organization/organization']
    type2id = {}
    typefile = codecs.open(dir_path+'type2Num.txt','w','utf-8')
    i=0
    for item in t:
        typefile.write(item+'\t'+str(i)+'\n')
        type2id[item] =i
        i = i + 1
    typefile.close()
    
    f_ent = codecs.open(dir_path+"extract_ent_has_type.txt",'w','utf-8')
    
    for key in ents:
        print 'ent key',key
        types = ents[key]
        print types
        if  types!='NIL':
            items = types.split('\t')
            typenolist=''
            for typei in items:
                typenolist = typenolist + str(type2id[typei])+'\t'
            f_ent.write(key+'\t'+typenolist.strip()+'\n')
    f_ent.close()