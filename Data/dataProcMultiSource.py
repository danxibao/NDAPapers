#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 16:58:10 2017

@author: Rao
"""

import pandas as pd
import numpy as np
import os
import pickle


Density="1.5"
EnergyType=1
multiSource=True
input_path="5plus5_MultiSource/"
dump_path = "CacheMulti/"
output_path="ans2.csv"
#detection type
dt=["SGS","STGS8EB","STGS8ER"]

def Import(DetectionType):
    fin=open(input_path+Density+"_"+DetectionType+".txt")
    try:
        all_lines = fin.readlines()
    finally:
        fin.close()

    df=pd.DataFrame(columns=("Density","DetectionType",
                             0,1,2,5,"total"))

    i=0
    for line in all_lines:
        line=line.split()
        nums=[float(Density),
        DetectionType,
        float(line[2]),
        float(line[3]),
        float(line[4]),
        float(line[5]),
        float(line[6])]
        df.loc[i]=pd.Series(nums,index=df.columns)
        i+=1
    
    if multiSource:
        fin=open(input_path+Density+"_"+DetectionType+"_0_Activity.txt")
        try:
            all_lines = fin.readlines()
        finally:
            fin.close()
        
        add=pd.DataFrame()
        add["RealActivity"]=None
        i=0
        for line in all_lines:
            add.loc[i]=float(line)
            i+=1
        df=df.join(add)

    return df

def get_df():
    frames=[Import(dt[0]),
        Import(dt[1]),
        Import(dt[2])]
    df=pd.concat(frames,ignore_index=True)#ignore_index or index will repeat
    return df


ans=pd.DataFrame(columns=("Density","EnergyType","Max.","Min.","RMS"))


def get_y(DetectionType):
    df=Import(DetectionType)
    #df[(df["Density"]==Density) & (df["DetectionType"]==DetectionType)][EnergyType]/10000000.0-1
    if multiSource:
        y=df[EnergyType]/df['RealActivity']*100-100#percent,%
    else:
        y=df[EnergyType]/100000-100#percent,%
    
    new=pd.DataFrame( {"Density":Density,"EnergyType":EnergyType,
            "Max.":"%.2f" % y.max(),
            "Min.":"%.2f" % y.min(),
            "RMS":"%.2f" % np.sqrt((y**2).mean()) },
        index=[0])
    global ans#change global variable need statement ahead
    ans=ans.append(new,ignore_index=True)

    return y

def get_all_y():
    return [get_y(dt[0]),get_y(dt[1]),get_y(dt[2])]



y=get_all_y()
print ans
pickle.dump(ans, open(dump_path+Density+"_"+str(EnergyType)+".pkl", 'w'))

def paint():
    import matplotlib.pyplot as plt
    x = 2.5*np.arange(14)

    ax = plt.subplot(111) #注意:一般都在ax中设置,不再plot中设置
    plt.plot(x,y[0],",-",label=dt[0])
    plt.plot(x,y[1],".-",label="STGS8EA")
    plt.plot(x,y[2],"s-",label=dt[2])

    plt.legend()
    plt.xlim(0,35)

    #y-axis format into percent(%) style
    import matplotlib.ticker as mtick
    fmt='%.0f%%'
    yticks = mtick.FormatStrFormatter(fmt)
    ax.yaxis.set_major_formatter(yticks)
    
    ax.yaxis.grid(True)
    ax.set_xlabel("r(cm)")
    ax.set_ylabel("Det")

    #plt.title("0.5")
    plt.show()



def output_all():
    result=pd.DataFrame(columns=("Density","EnergyType","Max.","Min.","RMS"))
    for parent,dirnames,filenames in os.walk(dump_path):
        #print filenames
        for index,item in enumerate(filenames):
            #print filenames[index]
            if filenames[index].endswith('.pkl'):
                result=result.append(pickle.load(open(dump_path+filenames[index])))
    result.to_csv(output_path,index=False,index_label=False)

output_all()